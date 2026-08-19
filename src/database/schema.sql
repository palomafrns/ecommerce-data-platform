CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    price NUMERIC(12, 2),
    discount_percentage NUMERIC(6, 2),
    rating NUMERIC(4, 2),
    stock INTEGER,
    brand TEXT,
    sku TEXT,
    weight INTEGER,
    warranty_information TEXT,
    shipping_information TEXT,
    availability_status TEXT,
    return_policy TEXT,
    minimum_order_quantity INTEGER,
    thumbnail TEXTz

CREATE TABLE IF NOT EXISTS product_dimensions (
    product_id INTEGER PRIMARY KEY REFERENCES products(product_id),
    width NUMERIC,
    height NUMERIC,
    depth NUMERIC
);

CREATE TABLE IF NOT EXISTS product_images (
    product_id INTEGER REFERENCES products(product_id),
    position INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    PRIMARY KEY (product_id, position)
);

CREATE TABLE IF NOT EXISTS product_tags (
    product_id INTEGER REFERENCES products(product_id),
    tag TEXT NOT NULL,
    PRIMARY KEY (product_id, tag)
);

CREATE TABLE IF NOT EXISTS product_reviews (
    review_id BIGSERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    rating INTEGER,
    comment TEXT,
    review_date TIMESTAMP,
    reviewer_name TEXT,
    reviewer_email TEXT
);

CREATE TABLE IF NOT EXISTS product_metadata (
    product_id INTEGER PRIMARY KEY REFERENCES products(product_id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    barcode TEXT,
    qr_code TEXT
);

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON product_reviews(product_id);
