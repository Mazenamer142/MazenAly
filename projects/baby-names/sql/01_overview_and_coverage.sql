-- 01 headline numbers and what the data can and cannot see

select
  count(*) as rows_used,
  sum(births) as births,
  count(distinct name) as unique_names,
  count(distinct state) as states
from fact_names;

select year, sum(births) as births, count(distinct name) as unique_names
from nat_names
group by year
order by year;

select gender, count(distinct name) as unique_names, sum(births) as births
from nat_names
group by gender;

-- names with fewer than 5 babies in a state are not in the file at all.
-- how much of the file is made of small counts?
select
  round(100.0 * sum(case when births < 10 then 1 else 0 end) / count(*), 1) as pct_rows_under_10,
  round(100.0 * sum(case when births < 10 then births else 0 end) / sum(births), 1) as pct_of_births_in_those_rows
from fact_names;

-- births by state size: smallest and biggest states
select state, sum(births) as births from fact_names group by state order by births limit 3;
select state, sum(births) as births from fact_names group by state order by births desc limit 3;
