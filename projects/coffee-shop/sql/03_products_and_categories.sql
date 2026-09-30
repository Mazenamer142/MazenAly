-- 03 what do they buy

-- category
select
  category,
  round(sum(revenue)) as revenue,
  round(100.0 * sum(revenue) / (select sum(revenue) from fact_sales), 1) as share_pct
from fact_sales
group by category
order by revenue desc;

-- product type, top 8
select product_type, round(sum(revenue)) as revenue
from fact_sales
group by product_type
order by revenue desc
limit 8;

-- top 10 single products (name + size)
select product, round(sum(revenue)) as revenue, sum(qty) as units
from fact_sales
group by product
order by revenue desc
limit 10;

-- drink sizes (only drinks have a size)
select
  size,
  count(*) as lines,
  round(100.0 * count(*) / (select count(*) from fact_sales where size <> 'No size'), 1) as share_pct
from fact_sales
where size <> 'No size'
group by size
order by lines desc;
