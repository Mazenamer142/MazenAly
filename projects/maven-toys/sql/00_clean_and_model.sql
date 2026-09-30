-- =====================================================================
-- 00 | CLEAN + MODEL
-- Source: Maven Analytics "Maven Toys" (Mexico toy store chain) - public dataset
-- Assumes the 4 CSVs were imported as tables named: products, stores, inventory, sales
-- Dialect: written for SQLite; notes flag what to change for MySQL / PostgreSQL / SQL Server.
-- =====================================================================

-- ---- Data quality checks (all should return 0 unless noted) ----------
SELECT 'sales rows'                     AS check_name, COUNT(*)                                        AS result FROM sales
UNION ALL SELECT 'duplicate sale_id',        COUNT(*) - COUNT(DISTINCT Sale_ID)                          FROM sales
UNION ALL SELECT 'null units',               COUNT(*)                                                    FROM sales WHERE Units IS NULL
UNION ALL SELECT 'orphan product_id',        COUNT(*)                                                    FROM sales WHERE Product_ID NOT IN (SELECT Product_ID FROM products)
UNION ALL SELECT 'orphan store_id',          COUNT(*)                                                    FROM sales WHERE Store_ID   NOT IN (SELECT Store_ID   FROM stores)
UNION ALL SELECT 'inventory rows (of 1750 possible store x product pairs)', COUNT(*)                     FROM inventory;

-- ---- Dimensions ------------------------------------------------------
-- Cost and price arrive as text like '$9.99 ' (dollar sign + trailing space) -> cast to numbers.
DROP TABLE IF EXISTS dim_product;
CREATE TABLE dim_product AS
SELECT Product_ID                                                        AS product_id,
       Product_Name                                                      AS product_name,
       Product_Category                                                  AS category,
       CAST(REPLACE(REPLACE(TRIM(Product_Cost),  '$', ''), ',', '') AS REAL) AS unit_cost,
       CAST(REPLACE(REPLACE(TRIM(Product_Price), '$', ''), ',', '') AS REAL) AS unit_price
FROM products;

-- The source spells the capital 'Cuidad de Mexico' in Store_City but 'Ciudad de Mexico' in Store_Name -> standardise.
DROP TABLE IF EXISTS dim_store;
CREATE TABLE dim_store AS
SELECT Store_ID        AS store_id,
       Store_Name      AS store_name,
       CASE WHEN Store_City = 'Cuidad de Mexico' THEN 'Ciudad de Mexico' ELSE Store_City END AS city,
       Store_Location  AS location_type,
       Store_Open_Date AS open_date
FROM stores;

-- ---- Fact table: one row per sale line, with money columns pre-computed ---
-- Dates are ISO text (YYYY-MM-DD). SUBSTR(...) works in SQLite/MySQL/PostgreSQL; use SUBSTRING(...) in SQL Server.
DROP TABLE IF EXISTS fact_sales;
CREATE TABLE fact_sales AS
SELECT s.Sale_ID                                   AS sale_id,
       s.Date                                      AS sale_date,
       SUBSTR(s.Date, 1, 7)                        AS year_month,
       CAST(SUBSTR(s.Date, 1, 4) AS INTEGER)       AS year,
       CAST(SUBSTR(s.Date, 6, 2) AS INTEGER)       AS month_num,
       s.Store_ID                                  AS store_id,
       s.Product_ID                                AS product_id,
       s.Units                                     AS units,
       s.Units * p.unit_price                      AS revenue,
       s.Units * p.unit_cost                       AS cost,
       s.Units * (p.unit_price - p.unit_cost)      AS profit
FROM sales s
JOIN dim_product p ON p.product_id = s.Product_ID;

CREATE INDEX idx_fact_store   ON fact_sales(store_id);
CREATE INDEX idx_fact_product ON fact_sales(product_id);
CREATE INDEX idx_fact_month   ON fact_sales(year_month);

DROP TABLE IF EXISTS fact_inventory;
CREATE TABLE fact_inventory AS
SELECT Store_ID AS store_id, Product_ID AS product_id, Stock_On_Hand AS stock_on_hand FROM inventory;
