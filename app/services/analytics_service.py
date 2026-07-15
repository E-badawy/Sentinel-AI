import json
import os
from datetime import datetime


class AnalyticsService:

    def __init__(self):

        self.filepath = "app/data/visitors.json"

        os.makedirs(
            os.path.dirname(self.filepath),
            exist_ok=True
        )

        if not os.path.exists(self.filepath):

            with open(self.filepath, "w") as f:
                json.dump([], f)

    def log_visit(
        self,
        data: dict
    ):

        with open(
            self.filepath,
            "r",
            encoding="utf-8"
        ) as f:

            visitors = json.load(f)

        data["timestamp"] = datetime.utcnow().isoformat()

        visitors.append(data)

        with open(
            self.filepath,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                visitors,
                f,
                indent=4
            )

    def summary(self):

        with open(
            self.filepath,
            "r",
            encoding="utf-8"
        ) as f:

            visitors = json.load(f)

        return {
            "total_visits": len(visitors),
            "visitors": visitors[-20:]
        }


analytics_service = AnalyticsService()