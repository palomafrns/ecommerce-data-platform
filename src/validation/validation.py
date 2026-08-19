import json
from pathlib import Path


STAGING_DIR = Path("data/staging/products")


def load_json(file_name):
    file_path = STAGING_DIR / file_name

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_product_ids(products):
    ids = [product["product_id"] for product in products]

    return {
        "records": len(ids),
        "unique_ids": len(set(ids)),
        "duplicates": len(ids) - len(set(ids)),
    }


def validate_foreign_keys(products, child_records, field="product_id"):
    product_ids = {
        product["product_id"]
        for product in products
    }

    invalid = [
        record
        for record in child_records
        if record[field] not in product_ids
    ]

    return len(invalid)


def validate_products(products):
    errors = []

    for product in products:

        if product.get("product_id") is None:
            errors.append("product_id ausente")

        if not product.get("title"):
            errors.append(
                f"title ausente: product_id={product.get('product_id')}"
            )

        price = product.get("price")

        if price is not None and price < 0:
            errors.append(
                f"price inválido: product_id={product.get('product_id')}"
            )

        stock = product.get("stock")

        if stock is not None and stock < 0:
            errors.append(
                f"stock inválido: product_id={product.get('product_id')}"
            )

        rating = product.get("rating")

        if rating is not None and not 0 <= rating <= 5:
            errors.append(
                f"rating inválido: product_id={product.get('product_id')}"
            )

    return errors


def main():

    products = load_json("products.json")
    dimensions = load_json("dimensions.json")
    reviews = load_json("reviews.json")
    images = load_json("images.json")
    tags = load_json("tags.json")
    metadata = load_json("metadata.json")

    print("=" * 50)
    print("STAGING DATA VALIDATION")
    print("=" * 50)

    print("\nRECORD COUNTS")
    print(f"Products:    {len(products)}")
    print(f"Dimensions:  {len(dimensions)}")
    print(f"Reviews:     {len(reviews)}")
    print(f"Images:      {len(images)}")
    print(f"Tags:        {len(tags)}")
    print(f"Metadata:    {len(metadata)}")

    print("\nPRODUCT ID")

    product_id_validation = validate_product_ids(products)

    print(f"Total IDs:       {product_id_validation['records']}")
    print(f"Unique IDs:      {product_id_validation['unique_ids']}")
    print(f"Duplicate IDs:   {product_id_validation['duplicates']}")

    print("\nFOREIGN KEYS")

    relationships = {
        "dimensions": dimensions,
        "reviews": reviews,
        "images": images,
        "tags": tags,
        "metadata": metadata,
    }

    for table_name, records in relationships.items():

        invalid = validate_foreign_keys(
            products,
            records
        )

        print(
            f"{table_name}: "
            f"{invalid} product_id(s) invalido(s)"
        )

    print("\nBUSINESS RULES")

    errors = validate_products(products)

    if errors:
        print(f"Erros encontrados: {len(errors)}")

        for error in errors:
            print(f"- {error}")

    else:
        print("Nenhum erro encontrado.")

    print("\nVALIDATION FINISHED")


if __name__ == "__main__":
    main()