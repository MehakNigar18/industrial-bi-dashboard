-- ============================================
-- View 1: Daily OEE by Machine
-- Pre-aggregates production data for fast OEE dashboard queries
-- ============================================
CREATE VIEW vw_daily_oee AS
SELECT
    p.date_id,
    p.machine_id,
    m.machine_name,
    m.plant,
    SUM(p.units_produced) AS total_units_produced,
    SUM(p.units_defect) AS total_units_defect,
    SUM(p.downtime_mins) AS total_downtime_mins,
    SUM(p.capacity_available) AS total_capacity_available,
    CAST(SUM(p.units_produced) AS FLOAT) / NULLIF(SUM(p.capacity_available), 0) AS performance_rate,
    CAST(SUM(p.units_produced) - SUM(p.units_defect) AS FLOAT) / NULLIF(SUM(p.units_produced), 0) AS quality_rate
FROM stg_production p
JOIN stg_machines m ON p.machine_id = m.machine_id
GROUP BY p.date_id, p.machine_id, m.machine_name, m.plant;
GO

-- ============================================
-- View 2: Sales Summary by Product & Channel
-- Pre-aggregates revenue/margin for fast Deckungsbeitrag queries
-- ============================================
CREATE VIEW vw_sales_summary AS
SELECT
    s.date_id,
    s.product_id,
    s.channel,
    SUM(s.units_sold) AS total_units_sold,
    SUM(s.revenue) AS total_revenue,
    SUM(s.cost_of_goods) AS total_cogs,
    SUM(s.gross_margin) AS total_gross_margin,
    AVG(s.discount_pct) AS avg_discount_pct
FROM stg_sales s
GROUP BY s.date_id, s.product_id, s.channel;
GO

-- ============================================
-- View 3: Budget vs Actual Variance by Cost Centre
-- Pre-calculates variance % for fast RAG-flag dashboard queries
-- ============================================
CREATE VIEW vw_budget_variance AS
SELECT
    f.date_id,
    f.cc_id,
    f.product_id,
    f.budget_revenue,
    f.budget_cost,
    f.forecast_revenue,
    f.forecast_cost,
    (f.forecast_cost - f.budget_cost) AS cost_variance,
    CAST((f.forecast_cost - f.budget_cost) AS FLOAT) / NULLIF(f.budget_cost, 0) AS cost_variance_pct
FROM stg_finance f;
GO