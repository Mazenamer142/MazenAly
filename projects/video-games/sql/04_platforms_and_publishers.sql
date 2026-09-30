-- 04 platforms and publishers

select console, count(*) as games, round(sum(sales), 1) as sales_m
from fact_games
group by console
order by sales_m desc
limit 10;

select platform_family, round(sum(sales), 1) as sales_m,
  round(100.0 * sum(sales) / (select sum(sales) from fact_games), 1) as share_pct
from fact_games
group by platform_family
order by sales_m desc;

-- top 10 publishers after cleaning the names
select publisher, count(*) as games, round(sum(sales), 1) as sales_m
from fact_games
group by publisher
order by sales_m desc
limit 10;

-- how much of the market do the top 10 publishers hold?
select round(100.0 * sum(sales_m) / (select sum(sales) from fact_games), 1) as top_10_share_pct
from (
  select sum(sales) as sales_m from fact_games group by publisher order by sales_m desc limit 10
);
