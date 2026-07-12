SELECT
  (SELECT COUNT(*) FROM stg_machines) AS machines,
  (SELECT COUNT(*) FROM stg_production) AS production,
  (SELECT COUNT(*) FROM stg_sales) AS sales,
  (SELECT COUNT(*) FROM stg_finance) AS finance;




  SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS;
  