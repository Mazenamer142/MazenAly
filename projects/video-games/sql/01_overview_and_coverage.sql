-- 01 headline numbers and how much data there really is

select
  count(*) as titles_on_a_console,
  count(distinct title) as unique_titles,
  round(sum(sales), 1) as total_sales_m
from fact_games;

-- sales by release year
select release_year, count(*) as games, round(sum(sales), 1) as sales_m
from fact_games
where release_year is not null
group by release_year
order by release_year;

-- how many of ALL rows have sales, by release year. this is why i stop at 2018
select
  cast(substr(release_date, 1, 4) as integer) as release_year,
  count(*) as all_rows,
  count(total_sales) as rows_with_sales,
  round(100.0 * count(total_sales) / count(*)) as pct_with_sales
from games
where release_date is not null and substr(release_date, 1, 4) between '2012' and '2024'
group by release_year
order by release_year;
