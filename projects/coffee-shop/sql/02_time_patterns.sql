-- 02 when do people buy

-- revenue by hour
select hour, round(sum(revenue)) as revenue
from fact_sales
group by hour
order by hour;

-- revenue by hour for each store, per day so the numbers are easy to read
select
  store_location,
  hour,
  round(sum(revenue) / count(distinct sale_date), 1) as revenue_per_day
from fact_sales
group by store_location, hour
order by store_location, hour;

-- share of each store's revenue that comes in the morning rush (7 to 10), and after 5pm
select
  store_location,
  round(100.0 * sum(case when hour between 7 and 10 then revenue else 0 end) / sum(revenue), 1) as morning_rush_pct,
  round(100.0 * sum(case when hour >= 17 then revenue else 0 end) / sum(revenue), 1) as evening_pct
from fact_sales
group by store_location
order by store_location;

-- weekday (0 = sunday)
select weekday_num, round(sum(revenue)) as revenue
from fact_sales
group by weekday_num
order by weekday_num;
