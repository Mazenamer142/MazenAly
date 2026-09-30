-- =====================================================================
-- 01 | HEADLINE KPIs
-- Question: how big is the business, and how profitable?
-- =====================================================================
SELECT COUNT(*)                                        AS sale_lines,
       MIN(sale_date)                                  AS first_day,
       MAX(sale_date)                                  AS last_day,
       SUM(units)                                      AS units,
       ROUND(SUM(revenue), 0)                          AS revenue,
       ROUND(SUM(cost), 0)                             AS cost,
       ROUND(SUM(profit), 0)                           AS profit,
       ROUND(100.0 * SUM(profit) / SUM(revenue), 1)    AS margin_pct
FROM fact_sales;

-- Monthly trend: revenue, profit and margin (margin is kept on its own chart, never on a dual axis)
SELECT year_month,
       ROUND(SUM(revenue), 0)                          AS revenue,
       ROUND(SUM(profit), 0)                           AS profit,
       ROUND(100.0 * SUM(profit) / SUM(revenue), 1)    AS margin_pct
FROM fact_sales
GROUP BY year_month
ORDER BY year_month;
