import os
import re

from databricks import sql
from databricks.sdk.core import Config

_TABLE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+\.[A-Za-z0-9_]+\.[A-Za-z0-9_]+$")


class DatabricksCustomerRepository:
    def list_customers(self) -> list[dict]:
        warehouse_id = os.environ["DATABRICKS_WAREHOUSE_ID"]
        table_name = os.environ["CUSTOMER_TABLE_NAME"]

        # Table names are SQL identifiers, so validate them before putting
        # the configured name into the query.
        if not _TABLE_NAME_PATTERN.fullmatch(table_name):
            raise ValueError("CUSTOMER_TABLE_NAME must be catalog.schema.table")

        config = Config()

        with sql.connect(
            server_hostname=config.host,
            http_path=f"/sql/1.0/warehouses/{warehouse_id}",
            credentials_provider=lambda: config.authenticate,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT customerID, first_name, last_name, city, state
                    FROM {table_name}
                    LIMIT 20
                    """
                )

                columns = [column[0] for column in cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]