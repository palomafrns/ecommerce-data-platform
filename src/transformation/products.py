import json
import re
from pathlib import Path


def load_raw(file_path):
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def to_snake_case(text):
    return re.sub(
        r"(?<!^)(?=[A-Z])",
        "_",
        text
    ).lower()

def transform_products(raw_data):

    products = raw_data["data"]

    transformed_products = []
    transformed_dimensions = []
    transformed_reviews = []
    transformed_images = []
    transformed_tags = []
    transformed_metadata = []

    for product in products:

        # PRODUCTS

        transformed_product = {
            to_snake_case(key): value
            for key, value in product.items()
            if not isinstance(value, (dict, list))
        }
        
        transformed_product["product_id"] = transformed_product.pop("id")

        transformed_products.append(transformed_product)

        # IMAGES

        images = product.get("images") or []

        for position, image_url in enumerate(images):

            transformed_images.append({
                "product_id": product["id"],
                "position": position,
                "image_url": image_url,
            })


        # TAGS

        tags = product.get("tags") or []

        for tag in tags:

            transformed_tags.append({
                "product_id": product["id"],
                "tag": tag,
            })
        
        # METADATA
        metadata = product.get("meta") or {}

        transformed_metadata.append({
        "product_id": product["id"],
        "created_at": metadata.get("createdAt"),
        "updated_at": metadata.get("updatedAt"),
        "barcode": metadata.get("barcode"),
        "qr_code": metadata.get("qrCode"),
        })

        # DIMENSIONS

        dimensions = product.get("dimensions")

        if dimensions:
            transformed_dimensions.append({
                "product_id": product["id"],
                "width": dimensions.get("width"),
                "height": dimensions.get("height"),
                "depth": dimensions.get("depth"),
            })
            

        # REVIEWS


        reviews = product.get("reviews") or []

        for review in reviews:

            transformed_reviews.append({
                "product_id": product["id"],
                "rating": review.get("rating"),
                "comment": review.get("comment"),
                "date": review.get("date"),
                "reviewer_name": review.get("reviewerName"),
                "reviewer_email": review.get("reviewerEmail"),
            })
            

    return {
        "products": transformed_products,
        "dimensions": transformed_dimensions,
        "reviews": transformed_reviews,
        "images": transformed_images,
        "tags": transformed_tags,
        "metadata": transformed_metadata,
    }


def save_products(products, output_file):

    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            products,
            file,
            ensure_ascii=False,
            indent=2
        )


if __name__ == "__main__":

    raw_dir = Path("data/raw/products")
    raw_files = sorted(raw_dir.glob("products_*.json"))

    if not raw_files:
        raise FileNotFoundError(
            "Nenhum arquivo RAW encontrado em data/raw/products."
        )

    raw_file = raw_files[-1]

    raw_data = load_raw(raw_file)

    products = transform_products(raw_data)

save_products(
    products["products"],
    "data/staging/products/products.json"
)

save_products(
    products["dimensions"],
    "data/staging/products/dimensions.json"
)

save_products(
    products["reviews"],
    "data/staging/products/reviews.json"
)

save_products(
    products["images"],
    "data/staging/products/images.json"
)

save_products(
    products["tags"],
    "data/staging/products/tags.json"
    
)

save_products(
    products["metadata"],
    "data/staging/products/metadata.json"
)

print(f"Metadata transformada: {len(products['metadata'])}")
print(f"Tags transformadas: {len(products['tags'])}")
print(f"Imagens transformadas: {len(products['images'])}")
print(f"Produtos transformados: {len(products['products'])}")
print(f"Dimensoes transformadas: {len(products['dimensions'])}")
print(f"Reviews transformadas: {len(products['reviews'])}")