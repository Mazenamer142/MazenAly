-- 01 headline numbers

select
  count(*) as sale_lines,
  sum(qty) as units,
  round(sum(revenue)) as revenue,
  round(sum(revenue) / count(distinct sale_date)) as revenue_per_day,
  round(sum(revenue) / count(*), 2) as revenue_per_line
from fact_sales;

-- revenue per month. february is shorter so i also divide by the days in the data
select
  month,
  count(distinct sale_date) as days,
  round(sum(revenue)) as revenue,
  round(sum(revenue) / count(distinct sale_date)) as revenue_per_day
from fact_sales
group by month
order by month;

-- how many units per line
select qty, count(*) as lines
from fact_sales
group by qty
order by qty;
