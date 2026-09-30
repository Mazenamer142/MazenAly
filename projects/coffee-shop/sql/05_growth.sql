-- 05 growth from january to june
-- i use revenue per day because the months have different lengths

select
  category,
  round(sum(case when month = '2023-01' then revenue end) / 31) as jan_per_day,
  round(sum(case when month = '2023-06' then revenue end) / 30) as jun_per_day,
  round(100.0 * ((sum(case when month = '2023-06' then revenue end) / 30) /
                 (sum(case when month = '2023-01' then revenue end) / 31) - 1)) as growth_pct
from fact_sales
group by category
order by jun_per_day desc;

-- did the number of lines grow, or the value of each line?
select
  month,
  count(*) as sale_lines,
  round(sum(revenue) / count(*), 2) as revenue_per_line
from fact_sales
group by month
order by month;
