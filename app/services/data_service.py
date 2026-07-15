import pandas as pd


class DataService:

    def load(
        self,
        filepath: str
    ):

        if filepath.lower().endswith(".csv"):

            return pd.read_csv(filepath)

        return pd.read_excel(filepath)

    def summarize(
        self,
        dataframe
    ):

        return {
            "rows": len(dataframe),
            "columns": len(dataframe.columns),
            "column_names": list(dataframe.columns),
            "missing_values": dataframe.isnull().sum().to_dict(),

            # Only first 5 rows
            "preview": dataframe.head(5).to_markdown(index=False),

            # Numeric columns only
            "statistics": dataframe.describe(
                include="number"
            ).round(2).to_markdown()
        }


data_service = DataService()