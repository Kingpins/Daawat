CREATE TABLE IF NOT EXISTS users (
    first_name text,
    last_name text,
    phone text,
    email text,
    password text,
    PRIMARY KEY (email)
);

CREATE TABLE IF NOT EXISTS hotels (
    hotel_id text,
    hotel_name text,
    hotel_bio text,
    hotel_address text,
    hotel_phone text,
    hotel_tables text,
    hotel_logo text,
    useremail text,
    PRIMARY KEY (hotel_id)
);

CREATE TABLE IF NOT EXISTS foods (
    food_id text,
    food_name text,
    food_price int,
    food_description text,
    food_img text,
    useremail text,
    hotel_id text,
    category_name text,
    PRIMARY KEY (food_id,category_name)
) WITH CLUSTERING ORDER BY (category_name ASC);

CREATE TABLE IF NOT EXISTS categorys (
    category_id text,
    category_name text,
    category_img text,
    useremail text,
    hotel_id text,
    PRIMARY KEY (hotel_id,category_name)
) WITH CLUSTERING ORDER BY (category_name ASC);

CREATE TABLE IF NOT EXISTS generate_qr (
    hotel_name text,
    hotel_id text,
    useremail text,
    qr_image text,
    table_no text,
    PRIMARY KEY (qr_image)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id text,
    customer_name text,
    status boolean,
    hotel_id text,
    table_no text,
    PRIMARY KEY (customer_id)
);

CREATE TABLE IF NOT EXISTS orders (
    hotel_id text,
    customer_id text,
    order_id text,
    product text,
    time_of_order float,
    price int,
    quantity text,
    status boolean,
    PRIMARY KEY ((hotel_id, customer_id,order_id),time_of_order)
) WITH CLUSTERING ORDER BY (time_of_order DESC);


CREATE TABLE IF NOT EXISTS invoices (
    hotel_id text,
    customer_id text,
    order_id text,
    invoice_id text,
    product text,
    time_of_invoice float,
    price text,
    quantity text,
    grand_total text,
    PRIMARY KEY ((hotel_id, customer_id,order_id),time_of_invoice)
) WITH CLUSTERING ORDER BY (time_of_invoice DESC);

CREATE TABLE IF NOT EXISTS feedbacks (
    hotel_id text,
    customer_id text,
    customer_name text,
    ratings text,
    feedback_comment text,
    time_of_feedback float,
    PRIMARY KEY (hotel_id,time_of_feedback)
) WITH CLUSTERING ORDER BY (time_of_feedback DESC);