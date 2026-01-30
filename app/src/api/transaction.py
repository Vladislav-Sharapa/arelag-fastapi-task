from typing import Optional, List
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.api.depedencies.transaction_dependencies import (
    get_transaction_create_use_case,
    get_transaction_roll_back_use_case,
    get_transaction_service,
)
from app.src.core.database import get_async_session
from app.src.schemas.transaction_schemas import (
    RequestTransactionModel,
    TransactionModel,
)
from app.src.services.flows.transaction_flows import (
    CreateTransactionUseCase,
    TransactionRollBackUseCase,
)
from app.src.services.transaction import (
    TransactionService,
    get_not_rollbacked_deposit_amount,
    get_not_rollbacked_transactions_count,
    get_not_rollbacked_withdraw_amount,
    get_registered_and_deposit_users_count,
    get_registered_and_not_rollbacked_deposit_users_count,
    get_transactions_count,
)
from app.src.services.user import get_registered_users_count

router = APIRouter()


@router.get("/transactions", status_code=status.HTTP_200_OK)
async def get_transactions(
    user_id: Optional[int] = None,
    service: TransactionService = Depends(get_transaction_service),
) -> List[TransactionModel] | None:
    return await service.get_all(user_id=user_id)


@router.post(
    "/{user_id}/transactions",
    status_code=status.HTTP_200_OK,
)
async def post_transaction(
    request: RequestTransactionModel,
    user_id: int = Path(ge=0, description="User ID must be positive integer"),
    transaction_use_case: CreateTransactionUseCase = Depends(
        get_transaction_create_use_case
    ),
) -> TransactionModel | None:
    transaction = await transaction_use_case.execute(user_id=user_id, request=request)

    return transaction


@router.patch("/{user_id}/transactions/{transaction_id}")
async def patch_rollback_transaction(
    user_id: int = Path(ge=0, description="User ID must be positive integer"),
    transaction_id: int = Path(
        ge=0, description="Transaction ID must be positive integer"
    ),
    transaction_use_case: TransactionRollBackUseCase = Depends(
        get_transaction_roll_back_use_case
    ),
) -> TransactionModel | None:
    transaction = await transaction_use_case.execute(
        user_id=user_id, transaction_id=transaction_id
    )
    return transaction


@router.get(
    "/transactions/analysis",
    response_model=Optional[list] | None,
    status_code=status.HTTP_200_OK,
)
async def get_transaction_analysis(
    session: AsyncSession = Depends(get_async_session),
) -> List[dict]:
    dt_gt = datetime.utcnow().date() - timedelta(weeks=1) + timedelta(days=1)
    dt_lt = datetime.utcnow().date()
    results = []
    for i in range(52):
        registered_users_count = await get_registered_users_count(
            session, dt_gt=dt_gt, dt_lt=dt_lt
        )
        registered_and_deposit_users_count = (
            await get_registered_and_deposit_users_count(
                session, dt_gt=dt_gt, dt_lt=dt_lt
            )
        )
        registered_and_not_rollbacked_deposit_users_count = (
            await get_registered_and_not_rollbacked_deposit_users_count(
                session, dt_gt=dt_gt, dt_lt=dt_lt
            )
        )
        not_rollbacked_deposit_amount = await get_not_rollbacked_deposit_amount(
            session, dt_gt=dt_gt, dt_lt=dt_lt
        )
        not_rollbacked_withdraw_amount = await get_not_rollbacked_withdraw_amount(
            session, dt_gt=dt_gt, dt_lt=dt_lt
        )
        transactions_count = await get_transactions_count(
            session, dt_gt=dt_gt, dt_lt=dt_lt
        )
        not_rollbacked_transactions_count = await get_not_rollbacked_transactions_count(
            session, dt_gt=dt_gt, dt_lt=dt_lt
        )
        result = {
            "start_date": dt_gt,
            "end_date": dt_lt,
            "registered_users_count": registered_users_count,
            "registered_and_deposit_users_count": registered_and_deposit_users_count,
            "registered_and_not_rollbacked_deposit_users_count": registered_and_not_rollbacked_deposit_users_count,
            "not_rollbacked_deposit_amount": not_rollbacked_deposit_amount,
            "not_rollbacked_withdraw_amount": not_rollbacked_withdraw_amount,
            "transactions_count": transactions_count,
            "not_rollbacked_transactions_count": not_rollbacked_transactions_count,
        }
        for field in (
            "registered_users_count",
            "registered_and_deposit_users_count",
            "registered_and_not_rollbacked_deposit_users_count",
            "not_rollbacked_deposit_amount",
            "not_rollbacked_withdraw_amount",
            "transactions_count",
            "not_rollbacked_transactions_count",
        ):
            if result[field] > 0:
                results.append(result)
                break
        dt_gt -= timedelta(weeks=1)
        dt_lt -= timedelta(weeks=1)
    return results
