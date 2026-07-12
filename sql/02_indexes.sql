-- Indexes on date_id (used heavily in filtering/joining by date)
CREATE INDEX IX_stg_production_date_id ON stg_production(date_id);
CREATE INDEX IX_stg_sales_date_id ON stg_sales(date_id);
CREATE INDEX IX_stg_finance_date_id ON stg_finance(date_id);

-- Indexes on product_id (used in joins to products/SKU-level KPIs)
CREATE INDEX IX_stg_production_product_id ON stg_production(product_id);
CREATE INDEX IX_stg_sales_product_id ON stg_sales(product_id);
CREATE INDEX IX_stg_finance_product_id ON stg_finance(product_id);

-- Index on machine_id (used in OEE/downtime queries by machine)
CREATE INDEX IX_stg_production_machine_id ON stg_production(machine_id);

-- Index on cc_id (used in cost centre / controlling queries)
CREATE INDEX IX_stg_sales_cc_id ON stg_sales(cc_id);
CREATE INDEX IX_stg_finance_cc_id ON stg_finance(cc_id);

-- Covering index example: OEE queries typically filter by date+machine and need units/downtime
CREATE INDEX IX_production_oee_covering
ON stg_production(date_id, machine_id)
INCLUDE (units_produced, units_defect, downtime_mins, capacity_available);