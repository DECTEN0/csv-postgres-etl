from io import StringIO
from dotenv import load_dotenv
import os
import psycopg2


def load(df):

    conn = None

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cur = conn.cursor()

        columns = [
            "order_id",
            "customer_name",
            "product",
            "quantity",
            "price",
            "total_amount",
            "order_date"
        ]

        # Clear staging table
        cur.execute("TRUNCATE TABLE sales_staging;")

        # Create in-memory CSV
        buffer = StringIO()

        df[columns].to_csv(
            buffer,
            index=False,
            header=False
        )

        buffer.seek(0)

        # Fast bulk load into staging
        cur.copy_expert(
            """
            COPY sales_staging (
                order_id,
                customer_name,
                product,
                quantity,
                price,
                total_amount,
                order_date
            )
            FROM STDIN WITH CSV
            """,
            buffer
        )

        # Merge into final table
        cur.execute(
            """
            INSERT INTO sales (
                order_id,
                customer_name,
                product,
                quantity,
                price,
                total_amount,
                order_date
            )
            SELECT
                order_id,
                customer_name,
                product,
                quantity,
                price,
                total_amount,
                order_date
            FROM sales_staging
            ON CONFLICT (order_id)
            DO NOTHING;
            """
        )

        rows_loaded = cur.rowcount

        conn.commit()

        print(f"Successfully loaded {rows_loaded} new records.")

    except Exception as e:

        if conn:
            conn.rollback()

        print(f"Load failed: {e}")
        raise

    finally:

        if conn:
            cur.close()
            conn.close()