-- 02 where the revenue and profit come from

-- by category
select p.category,
  round(sum(f.revenue)) as revenue,
  round(sum(f.profit)) as profit,
  round(sum(f.profit) * 100.0 / sum(f.revenue), 1) as margin_pct,
  round(sum(f.revenue) * 100.0 / (select sum(revenue) from fact_sales), 1) as revenue_share_pct,
  round(sum(f.profit) * 100.0 / (select sum(profit) from fact_sales), 1) as profit_share_pct
from fact_sales f
join dim_product p on p.product_id = f.product_id
group by p.category
order by profit desc;

-- by product, biggest profit first
select p.product_name,
  p.category,
  round(sum(f.revenue)) as revenue,
  round(sum(f.profit)) as profit,
  round(sum(f.profit) * 100.0 / sum(f.revenue), 1) as margin_pct,
  round(sum(f.profit) * 100.0 / (select sum(profit) from fact_sales), 1) as profit_share_pct
from fact_sales f
join dim_product p on p.product_id = f.product_id
group by p.product_id, p.product_name, p.category
order by profit desc;
