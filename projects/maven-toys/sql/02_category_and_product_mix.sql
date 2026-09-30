-- =====================================================================
-- 02 | WHERE DOES THE MONEY (AND THE PROFIT) COME FROM?
-- =====================================================================

-- Category: revenue share vs profit share (window function for the shares)
SELECT p.category,
       ROUND(SUM(f.revenue), 0)                                                    AS revenue,
       ROUND(SUM(f.profit), 0)                                                     AS profit,
       ROUND(100.0 * SUM(f.profit) / SUM(f.revenue), 1)                            AS margin_pct,
       ROUND(100.0 * SUM(f.revenue) / SUM(SUM(f.revenue)) OVER (), 1)              AS revenue_share_pct,
       ROUND(100.0 * SUM(f.profit)  / SUM(SUM(f.profit))  OVER (), 1)              AS profit_share_pct
FROM fact_sales f
JOIN dim_product p ON p.product_id = f.product_id
GROUP BY p.category
ORDER BY profit DESC;

-- Product: ranked by profit, with margin and cumulative profit share (Pareto)
SELECT p.product_name,
       p.category,
       ROUND(SUM(f.revenue), 0)                                                    AS revenue,
       ROUND(SUM(f.profit), 0)                                                     AS profit,
       ROUND(100.0 * SUM(f.profit) / SUM(f.revenue), 1)                            AS margin_pct,
       ROUND(100.0 * SUM(f.profit) / SUM(SUM(f.profit)) OVER (), 1)                AS profit_share_pct,
       ROUND(100.0 * SUM(SUM(f.profit)) OVER (ORDER BY SUM(f.profit) DESC)
                   / SUM(SUM(f.profit)) OVER (), 1)                                AS cumulative_profit_pct
FROM fact_sales f
JOIN dim_product p ON p.product_id = f.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY profit DESC;
