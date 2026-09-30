-- 04 comparing the three stores

select
  store_location,
  round(sum(revenue)) as revenue,
  count(*) as sale_lines,
  round(sum(revenue) / count(distinct sale_date)) as revenue_per_day
from fact_sales
group by store_location
order by revenue desc;

-- monthly revenue per store
select month, store_location, round(sum(revenue)) as revenue
from fact_sales
group by month, store_location
order by month, store_location;

-- first and last hour with a sale in each store
select store_location, min(hour) as first_hour, max(hour) as last_hour
from fact_sales
group by store_location;
