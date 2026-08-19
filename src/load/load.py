import json
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values


STAGING_DIR = Path("data/staging/products")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ecommerce",
    "user": "ecommerce_user",
    "password": "ecommerce_password",
}


TABLES = [
    ("products", "products.json"),
    ("product_dimensions", "dimensions.json"),
    ("product_metadata", "metadata.json"),
    ("product_reviews", "reviews.json"),
    ("product_images", "images.json"),
    ("product_tags", "tags.json"),
]


def read_json(file_name):
    with (STAGING_DIR / file_name).open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def load_table(cursor, table_name, records):

    if not records:
        return 0

    # Corrige o nome do campo vindo da API
    if table_name == "product_reviews":
        for record in records:
            if "date" in record:
                record["review_date"] = record.pop("date")

    columns = list(records[0].keys())
    columns = sorted({
        key
        for record in records
        for key in record.keys()
    })

    values = [
        tuple(record.get(column) for column in columns)
        for record in records
    ]

    column_list = ", ".join(columns)

    query = f"""
        INSERT INTO {table_name} ({column_list})
        VALUES %s
        ON CONFLICT DO NOTHING;
    """

    execute_values(
        cursor,
        query,
        values
    )

    return len(records)


def main():

    connection = psycopg2.connect(**DB_CONFIG)

    try:

        cursor = connection.cursor()

        for table_name, file_name in TABLES:

            records = read_json(file_name)

            count = load_table(
                cursor,
                table_name,
                records
            )

            print(
                f"{table_name}: "
                f"{count} registros processados"
            )

        connection.commit()

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()