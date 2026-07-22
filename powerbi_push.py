"""
powerbi_push.py
===============
Helper for pushing the current CardsDataset to a Power BI push dataset.

Requires an Azure AD App Registration (service principal) that has been
added as a Contributor/Admin to the target Power BI workspace, and a push
dataset with a matching table schema.

Configuration is read from environment variables:
    POWERBI_TENANT_ID
    POWERBI_CLIENT_ID
    POWERBI_CLIENT_SECRET
    POWERBI_WORKSPACE_ID
    POWERBI_DATASET_ID
    POWERBI_TABLE_NAME        (optional, default "CardsDataset")
"""

import json
import math
import time

import pandas as pd
import requests


class PowerBIPushError(Exception):
    """Raised when a Power BI push operation fails."""


class PowerBIPusher:
    """Authenticate to Azure AD and push rows to a Power BI push dataset."""

    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        workspace_id: str,
        dataset_id: str | None = None,
        table_name: str = "CardsDataset",
    ):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.workspace_id = workspace_id
        self.dataset_id = dataset_id
        self.table_name = table_name
        self._token: str | None = None

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    def _get_access_token(self) -> str:
        """Obtain a Bearer token from Azure AD using client credentials."""
        if self._token:
            return self._token

        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://analysis.windows.net/powerbi/api/.default",
        }

        try:
            resp = requests.post(url, data=data, timeout=20)
            resp.raise_for_status()
        except requests.RequestException as exc:
            raise PowerBIPushError(f"Azure AD authentication failed: {exc}") from exc

        payload = resp.json()
        token = payload.get("access_token")
        if not token:
            raise PowerBIPushError("Azure AD did not return an access token.")
        self._token = token
        return token

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json",
        }

    # ------------------------------------------------------------------
    # API helpers
    # ------------------------------------------------------------------
    def _rows_url(self) -> str:
        return (
            "https://api.powerbi.com/v1.0/myorg/"
            f"groups/{self.workspace_id}/datasets/{self.dataset_id}/"
            f"tables/{self.table_name}/rows"
        )

    # ------------------------------------------------------------------
    # Dataset creation
    # ------------------------------------------------------------------
    @staticmethod
    def infer_schema(data: pd.DataFrame) -> list[dict[str, str]]:
        """Infer Power BI table columns from a pandas DataFrame."""
        columns = []
        for col in data.columns:
            dtype = data[col].dtype
            if pd.api.types.is_integer_dtype(dtype):
                powerbi_type = "Int64"
            elif pd.api.types.is_float_dtype(dtype):
                powerbi_type = "Double"
            elif pd.api.types.is_bool_dtype(dtype):
                powerbi_type = "Boolean"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                powerbi_type = "DateTime"
            else:
                # Object / string / list / dict -> store as string
                powerbi_type = "String"
            columns.append({"name": col, "dataType": powerbi_type})
        return columns

    def create_dataset(self, data: pd.DataFrame, dataset_name: str | None = None) -> str:
        """
        Create a Power BI push dataset from a pandas DataFrame.

        Returns the new dataset ID.
        """
        if data is None or data.empty:
            raise PowerBIPushError("No data to create dataset from.")

        name = dataset_name or self.table_name or "CardsDataset"
        columns = self.infer_schema(data)

        url = (
            "https://api.powerbi.com/v1.0/myorg/"
            f"groups/{self.workspace_id}/datasets?defaultRetentionPolicy=None"
        )
        payload = {
            "name": name,
            "tables": [
                {
                    "name": self.table_name or "CardsDataset",
                    "columns": columns,
                }
            ],
        }

        try:
            resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as exc:
            try:
                detail = exc.response.json() if exc.response is not None else str(exc)
            except Exception:
                detail = str(exc)
            raise PowerBIPushError(f"Failed to create Power BI dataset: {detail}") from exc

        result = resp.json()
        dataset_id = result.get("id")
        if not dataset_id:
            raise PowerBIPushError(f"Power BI did not return a dataset id: {result}")
        return dataset_id

    # ------------------------------------------------------------------
    # Row operations
    # ------------------------------------------------------------------
    def clear_table(self) -> None:
        """Delete all existing rows from the push dataset table."""
        headers = {"Authorization": f"Bearer {self._get_access_token()}"}
        resp = requests.delete(self._rows_url(), headers=headers, timeout=30)
        # A 404 simply means there were no rows / table didn't exist yet.
        if resp.status_code not in (200, 202, 204, 404):
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            raise PowerBIPushError(f"Could not clear Power BI table: {resp.status_code} {detail}")

    def push_dataframe(
        self,
        data: pd.DataFrame,
        *,
        clear_first: bool = True,
        chunk_size: int = 10000,
    ) -> int:
        """
        Push a pandas DataFrame to the configured Power BI push dataset.

        Returns the number of rows pushed.
        """
        if data is None or data.empty:
            raise PowerBIPushError("No data to push to Power BI.")

        if clear_first:
            self.clear_table()

        # Convert NaN/NaT to None so JSON serialisation works cleanly.
        export_df = data.copy()
        export_df = export_df.where(pd.notnull(export_df), None)

        # Power BI push datasets only accept scalar cells. Convert any
        # list/dict/tuple columns to JSON strings.
        for col in export_df.columns:
            if export_df[col].dtype == object:
                try:
                    sample = export_df[col].dropna().iloc[0]
                    if isinstance(sample, (list, dict, tuple)):
                        export_df[col] = export_df[col].apply(
                            lambda x: json.dumps(x) if x is not None else None
                        )
                except IndexError:
                    pass

        records = export_df.to_dict(orient="records")
        total = len(records)

        headers = self._headers()
        url = self._rows_url()
        pushed = 0
        for i in range(0, total, chunk_size):
            chunk = records[i : i + chunk_size]
            payload = {"rows": chunk}
            resp = requests.post(url, headers=headers, json=payload, timeout=60)

            # Basic rate-limit backoff.
            if resp.status_code == 429:
                time.sleep(2)
                resp = requests.post(url, headers=headers, json=payload, timeout=60)

            if resp.status_code not in (200, 202):
                try:
                    detail = resp.json()
                except Exception:
                    detail = resp.text
                raise PowerBIPushError(
                    f"Push failed at row {i}: {resp.status_code} {detail}"
                )

            pushed += len(chunk)

        return pushed
