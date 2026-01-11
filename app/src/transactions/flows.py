from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.transactions.exceptions import TransactionAlreadyRollbackedException, TransactionDoesNotBelongToUserException, UpdateTransactionForBlockedUserException
from app.src.transactions.schemas import RequestTransactionModel, TransactionModel, TransactionStatusEnum
from app.src.transactions.service import TransactionService
from app.src.users.exceptions import NegativeBalanceException
from app.src.users.service import UserService


class CreateTransactionUseCase:
    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__transaction_service = TransactionService(session=self.__session)
        self.__user_service = UserService(session=self.__session)

    async def execute(self, user_id: int, request: RequestTransactionModel) -> TransactionModel:
        '''
        Execute a transaction for a user and update their balance.  

        :param user_id: The unique identifier of the user for whom the transaction is executed.
        :type user_id: int
        :param request: he transaction request object containing:
            - currency (str): The currency in which the transaction is made.
            - amount (Decimal): The transaction amount (positive for credit, negative for debit).
        :type request: RequestTransactionModel
        :return: A validated transaction model
        :rtype: TransactionModel
        :raises CreateTransactionForBlockedUserException: Try to create transaction for blocked user
        :raises UserBalanceNotFound: If no user's balance in database
        :raises UserNotExistsException: If the user does not exist in the system.
        :raises NegativeBalanceException: If the resulting balance after the transaction would be negative.
        '''
        user_balance = await self.__user_service.get_user_balance_by_currency(
            user_id=user_id, currency=request.currency
        )
        new_balance_amount = self.__calculate_new_balance(user_balance.amount, request_amount=request.amount)
        user_balance = await self.__user_service.update_balance(user_balance, amount=new_balance_amount)

        transaction = await self.__transaction_service.create_transaction(user_id=user_id, obj=request)

        await self.__session.commit()

        return TransactionModel.model_validate(transaction)
    
    def __calculate_new_balance(self, current_balance_amount: Decimal, request_amount: Decimal) -> Decimal:
        return current_balance_amount + request_amount


class TransactionRollBackUseCase:
    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__transaction_service = TransactionService(session=self.__session)
        self.__user_service = UserService(session=self.__session)

    def __calculate_new_balance(self, balance_amount: Decimal, transaction_amount: Decimal) -> Decimal:
        new_amount = balance_amount

        if transaction_amount < 0:
            new_amount += abs(transaction_amount)
        else: 
            new_amount -= transaction_amount

        return new_amount
        
    async def execute(self, user_id: int, transaction_id: int) -> TransactionModel:
        '''
        Roll back a transaction for a user and update their balance accordingly.    
            
        :param user_id: The unique identifier of the user whose transaction is being rolled back.
        :type user_id: int
        :param transaction_id: The unique identifier of the transaction to be rolled back.
        :type transaction_id: int
        :return: A validated transaction model
        :rtype: TransactionModel
        :raises UserAlreadyBlockedException: If user is blocked.
        :raises TransactionNotExistsException: If no such transaction in database.
        :raises CreateTransactionForBlockedUserException: Try to create transaction for blocked user
        :raises UserBalanceNotFound: If no user's balance in database
        :raises UserNotExistsException: If the user does not exist.
        :raises TransactionDoesNotBelongToUserException: If the transaction does not belong to the specified user.
        :raises TransactionAlreadyRollbackedException: If the transaction has already been rolled back.
        :raises NegativeBalanceException: If rolling back the transaction would result in a negative balance.
        '''
        user = await self.__user_service.get_active_user(user_id=user_id)

        user_transacrion = await self.__transaction_service.get_one(transaction_id=transaction_id)

        if user_transacrion.user_id != user.id:
            raise TransactionDoesNotBelongToUserException
        
        if user_transacrion.status == TransactionStatusEnum.roll_backed:
            raise TransactionAlreadyRollbackedException
        
        user_balance = await self.__user_service.get_user_balance_by_currency(user.id, user_transacrion.currency)

        new_balance_amount: Decimal = self.__calculate_new_balance(user_balance.amount, user_transacrion.amount)
        if new_balance_amount < 0:
            raise NegativeBalanceException
        await self.__user_service.update_balance(user_balance, amount=new_balance_amount)

        transaction = await self.__transaction_service.set_transaction_rollback(transaction=user_transacrion)
        await self.__session.commit()

        return TransactionModel.model_validate(transaction)


    