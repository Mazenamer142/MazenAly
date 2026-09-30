-- =====================================================================
-- 04 | STORES AND LOCATION TYPES
-- Question: is "Downtown = 56% of profit" a location effect, or just "29 of the 50 stores"?
-- =====================================================================

-- Profit per store by location type (normalises for how many stores each type has)
SELECT s.location_type,
       COUNT(DISTINCT s.store_id)                                         AS stores,
       ROUND(SUM(f.revenue), 0)                                           AS revenue,
       ROUND(SUM(f.profit), 0)                                            AS profit,
       ROUND(SUM(f.profit)  / COUNT(DISTINCT s.store_id), 0)              AS profit_per_store,
       ROUND(SUM(f.revenue) / COUNT(DISTINCT s.store_id), 0)              AS revenue_per_store,
       ROUND(100.0 * SUM(f.profit) / SUM(SUM(f.profit)) OVER (), 1)       AS profit_share_pct
FROM fact_sales f
JOIN dim_store s ON s.store_id = f.store_id
GROUP BY s.location_type
ORDER BY profit_per_store DESC;

-- Top and bottom 5 stores by profit
WITH store_profit AS (
    SELECT s.store_name, s.city, s.location_type,
           ROUND(SUM(f.revenue), 0) AS revenue, ROUND(SUM(f.profit), 0) AS profit,
           ROW_NUMBER() OVER (ORDER BY SUM(f.profit) DESC) AS rank_desc,
           ROW_NUMBER() OVER (ORDER BY SUM(f.profit) ASC)  AS rank_asc
    FROM fact_sales f JOIN dim_store s ON s.store_id = f.store_id
    GROUP BY s.store_id, s.store_name, s.city, s.location_type
)
SELECT store_name, city, location_type, revenue, profit
FROM store_profit
WHERE rank_desc <= 5 OR rank_asc <= 5
ORDER BY profit DESC;

-- Weekday pattern (0 = Sunday in SQLite's strftime('%w'); use DAYOFWEEK() in MySQL, EXTRACT(DOW ...) in PostgreSQL)
SELECT CASE CAST(strftime('%w', sale_date) AS INTEGER)
            WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed'
            WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri' ELSE 'Sat' END      AS weekday,
       ROUND(SUM(revenue), 0)                                       AS revenue
FROM fact_sales
GROUP BY strftime('%w', sale_date)
ORDER BY strftime('%w', sale_date);
