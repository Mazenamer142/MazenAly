-- =====================================================================
-- 05 | INVENTORY: stockouts and slow stock
-- The inventory table is a single snapshot (stock on hand today), not a history.
-- So the "lost profit" below is an ESTIMATE: a stocked-out product is assumed to keep selling at
-- the store's average daily profit for that product over the last 90 days of the data.
-- =====================================================================

-- 5a. Snapshot KPIs
SELECT ROUND(SUM(i.stock_on_hand * p.unit_cost), 0)                                   AS stock_value_at_cost,
       SUM(CASE WHEN i.stock_on_hand = 0 THEN 1 ELSE 0 END)                           AS stockout_pairs,
       COUNT(*)                                                                       AS store_product_pairs,
       ROUND(100.0 * SUM(CASE WHEN i.stock_on_hand = 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS stockout_rate_pct
FROM fact_inventory i
JOIN dim_product p ON p.product_id = i.product_id;

-- 5b. Recent daily sales rate per store x product (last 90 days of data: 2023-07-03 .. 2023-09-30)
DROP TABLE IF EXISTS recent_rate;
CREATE TABLE recent_rate AS
SELECT store_id, product_id,
       SUM(profit) / 90.0 AS daily_profit,
       SUM(units)  / 90.0 AS daily_units
FROM fact_sales
WHERE sale_date >= '2023-07-03'
GROUP BY store_id, product_id;

-- 5c. Which products are out of stock, and what is that likely costing per 30 days?
SELECT p.product_name,
       p.category,
       COUNT(*)                                                    AS stores_out_of_stock,
       ROUND(SUM(COALESCE(r.daily_profit, 0)) * 30, 0)             AS est_profit_at_risk_per_30d,
       ROUND(100.0 * (p.unit_price - p.unit_cost) / p.unit_price, 0) AS margin_pct
FROM fact_inventory i
JOIN dim_product p ON p.product_id = i.product_id
LEFT JOIN recent_rate r ON r.store_id = i.store_id AND r.product_id = i.product_id
WHERE i.stock_on_hand = 0
GROUP BY p.product_id, p.product_name, p.category, p.unit_price, p.unit_cost
ORDER BY est_profit_at_risk_per_30d DESC;

-- 5d. Slow stock: more than 180 days of cover at the recent selling rate
SELECT COUNT(*)                                            AS slow_pairs,
       ROUND(SUM(i.stock_on_hand * p.unit_cost), 0)        AS capital_tied_up
FROM fact_inventory i
JOIN dim_product p ON p.product_id = i.product_id
JOIN recent_rate r ON r.store_id = i.store_id AND r.product_id = i.product_id
WHERE r.daily_units > 0 AND i.stock_on_hand / r.daily_units > 180;

-- 5e. Coverage gap: store x product pairs missing from the inventory table
SELECT COUNT(*) AS pairs_missing_from_inventory,
       SUM(CASE WHEN EXISTS (SELECT 1 FROM fact_sales f WHERE f.store_id = st.store_id AND f.product_id = pr.product_id) THEN 1 ELSE 0 END) AS of_which_have_sales
FROM dim_store st
CROSS JOIN dim_product pr
WHERE NOT EXISTS (SELECT 1 FROM fact_inventory i WHERE i.store_id = st.store_id AND i.product_id = pr.product_id);
