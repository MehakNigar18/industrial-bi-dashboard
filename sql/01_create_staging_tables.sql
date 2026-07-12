USE industrial_bi_db;
GO

CREATE TABLE stg_machines (
    machine_id INT,
    machine_name VARCHAR(50),
    plant VARCHAR(50),
    production_line INT,
    machine_type VARCHAR(50),
    capacity_per_hour INT
);

CREATE TABLE stg_production (
    production_id INT,
    date_id DATE,
    machine_id INT,
    shift_id INT,
    product_id INT,
    units_produced INT,
    units_defect INT,
    downtime_mins INT,
    cost_actual DECIMAL(18,2),
    capacity_available INT
);

CREATE TABLE stg_sales (
    sale_id INT,
    date_id DATE,
    product_id INT,
    cc_id INT,
    channel VARCHAR(50),
    units_sold INT,
    revenue DECIMAL(18,2),
    discount_pct DECIMAL(5,3),
    cost_of_goods DECIMAL(18,2),
    gross_margin DECIMAL(18,2)
);

CREATE TABLE stg_finance (
    budget_id INT,
    date_id DATE,
    cc_id INT,
    product_id INT,
    budget_revenue DECIMAL(18,2),
    budget_cost DECIMAL(18,2),
    forecast_revenue DECIMAL(18,2),
    forecast_cost DECIMAL(18,2),
    scenario VARCHAR(20)
);


SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';