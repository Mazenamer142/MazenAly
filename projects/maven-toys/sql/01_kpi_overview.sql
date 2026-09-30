-- 01 overall numbers

select count(*) as sale_lines,
  min(sale_date) as first_day,
  max(sale_date) as last_day,
  sum(units) as units,
  round(sum(revenue)) as revenue,
  round(sum(cost)) as cost,
  round(sum(profit)) as profit,
  round(sum(profit) * 100.0 / sum(revenue), 1) as margin_pct
from fact_sales;

-- by month
select year_month,
  round(sum(revenue)) as revenue,
  round(sum(profit)) as profit,
  round(sum(profit) * 100.0 / sum(revenue), 1) as margin_pct
from fact_sales
group by year_month
order by year_month;
