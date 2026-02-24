from datetime import datetime, timedelta, timezone
from typing import List

from app.src.analytics.transaction_metrics import MetricsProvider
from app.src.schemas.transaction_schemas import WeekTransactionAnalyticsModel


class MetricsService:
    def __init__(self, metrics_provider: MetricsProvider):
        self.__provider = metrics_provider
        self.weeks = 52

    async def get_metrics(self) -> List[dict]:
        date_end = datetime.now(timezone.utc).date()
        date_start = date_end - timedelta(days=7)

        result_metrics = []
        for _ in range(self.weeks):
            metrics = await self.__provider.calculate_metrics(date_start, date_end)
            if self.__validate_metrics(metrics):
                result_metrics.append(
                    {
                        "start_date": date_start,
                        "end_date": date_end,
                        "metrics": metrics.model_dump(),
                    }
                )
            date_end -= timedelta(weeks=1)
            date_start -= timedelta(weeks=1)
        return result_metrics

    def __validate_metrics(self, metrics: WeekTransactionAnalyticsModel):
        for value in metrics.model_dump().values():
            if isinstance(value, (int, float)) and value > 0:
                return True
        return False
