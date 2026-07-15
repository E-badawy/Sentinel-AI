from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    Dimension,
    Metric
)

from google.oauth2 import service_account


class GA4Service:

    def __init__(self):

        credentials = service_account.Credentials.from_service_account_file(
            "credentials/ga4.json"
        )

        self.client = BetaAnalyticsDataClient(
            credentials=credentials
        )

        # GA4 Property ID
        self.property_id = "514291784"

    def visitors_last_7_days(self):

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[
                Dimension(name="country")
            ],
            metrics=[
                Metric(name="activeUsers")
            ],
            date_ranges=[
                {
                    "start_date": "7daysAgo",
                    "end_date": "today"
                }
            ]
        )

        response = self.client.run_report(request)

        results = []

        for row in response.rows:

            results.append({
                "country": row.dimension_values[0].value,
                "users": row.metric_values[0].value
            })

        return results


ga4_service = GA4Service()