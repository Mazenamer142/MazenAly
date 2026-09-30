-- 04 stores and location types
-- downtown has the most profit but it also has 29 of the 50 stores, so look at profit per store

select s.location_type,
  count(distinct s.store_id) as stores,
  round(sum(f.revenue)) as revenue,
  round(sum(f.profit)) as profit,
  round(sum(f.profit) / count(distinct s.store_id)) as profit_per_store,
  round(sum(f.revenue) / count(distinct s.store_id)) as revenue_per_store,
  round(sum(f.profit) * 100.0 / (select sum(profit) from fact_sales), 1) as profit_share_pct
from fact_sales f
join dim_store s on s.store_id = f.store_id
group by s.location_type
order by profit_per_store desc;

-- top 5 stores
select s.store_name, s.city, s.location_type, round(sum(f.profit)) as profit
from fact_sales f
join dim_store s on s.store_id = f.store_id
group by s.store_id, s.store_name, s.city, s.location_type
order by profit desc
limit 5;

-- bottom 5 stores
select s.store_name, s.city, s.location_type, round(sum(f.profit)) as profit
from fact_sales f
join dim_store s on s.store_id = f.store_id
group by s.store_id, s.store_name, s.city, s.location_type
order by profit asc
limit 5;

-- revenue by weekday (strftime is sqlite, in mysql use dayofweek())
select case cast(strftime('%w', sale_date) as integer)
    when 0 then 'Sun' when 1 then 'Mon' when 2 then 'Tue' when 3 then 'Wed'
    when 4 then 'Thu' when 5 then 'Fri' else 'Sat' end as weekday,
  round(sum(revenue)) as revenue
from fact_sales
group by strftime('%w', sale_date)
order by strftime('%w', sale_date);
