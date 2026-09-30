-- =====================================================================
-- 03 | GROWTH WITHOUT PROFIT: like-for-like Jan-Sep 2023 vs Jan-Sep 2022
-- The data ends 30 Sep 2023, so we compare the same nine months of each year.
-- =====================================================================

-- 3a. Like-for-like totals
SELECT year,
       ROUND(SUM(revenue), 0)                          AS revenue,
       ROUND(SUM(profit), 0)                           AS profit,
       ROUND(100.0 * SUM(profit) / SUM(revenue), 1)    AS margin_pct
FROM fact_sales
WHERE month_num <= 9
GROUP BY year
ORDER BY year;

-- 3b. Product-level change in profit (dollars), Jan-Sep 2022 -> Jan-Sep 2023
SELECT p.product_name,
       p.category,
       ROUND(SUM(CASE WHEN f.year = 2022 THEN f.profit ELSE 0 END), 0)             AS profit_2022,
       ROUND(SUM(CASE WHEN f.year = 2023 THEN f.profit ELSE 0 END), 0)             AS profit_2023,
       ROUND(SUM(CASE WHEN f.year = 2023 THEN f.profit ELSE 0 END)
           - SUM(CASE WHEN f.year = 2022 THEN f.profit ELSE 0 END), 0)             AS profit_change,
       SUM(CASE WHEN f.year = 2022 THEN f.units ELSE 0 END)                        AS units_2022,
       SUM(CASE WHEN f.year = 2023 THEN f.units ELSE 0 END)                        AS units_2023
FROM fact_sales f
JOIN dim_product p ON p.product_id = f.product_id
WHERE f.month_num <= 9
GROUP BY p.product_id, p.product_name, p.category
ORDER BY profit_change;

-- 3c. Margin bridge (mix effect). Prices and costs are single fixed values per product in this data,
-- so every product's margin is constant - the blended margin can ONLY move because the sales MIX moved.
--   contribution_pp = (revenue share 2023 - revenue share 2022) x (product margin - blended margin 2022)
-- and the contributions add up exactly to the change in blended margin (percentage points).
WITH by_product AS (
    SELECT f.product_id,
           SUM(CASE WHEN f.year = 2022 THEN f.revenue ELSE 0 END) AS rev22,
           SUM(CASE WHEN f.year = 2023 THEN f.revenue ELSE 0 END) AS rev23,
           SUM(CASE WHEN f.year = 2022 THEN f.profit  ELSE 0 END) AS prof22
    FROM fact_sales f
    WHERE f.month_num <= 9
    GROUP BY f.product_id
), totals AS (
    SELECT SUM(rev22) AS t22, SUM(rev23) AS t23, SUM(prof22) / SUM(rev22) AS blended22 FROM by_product
)
SELECT p.product_name,
       ROUND(100.0 * b.rev22 / t.t22, 2)                                                        AS rev_share_2022_pct,
       ROUND(100.0 * b.rev23 / t.t23, 2)                                                        AS rev_share_2023_pct,
       ROUND(100.0 * (p.unit_price - p.unit_cost) / p.unit_price, 1)                            AS product_margin_pct,
       ROUND(100.0 * (b.rev23 / t.t23 - b.rev22 / t.t22)
                   * ((p.unit_price - p.unit_cost) / p.unit_price - t.blended22), 2)            AS contribution_pp
FROM by_product b
CROSS JOIN totals t
JOIN dim_product p ON p.product_id = b.product_id
ORDER BY contribution_pp;
