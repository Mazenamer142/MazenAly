-- 03 are sales spread out or in a few hits? and do critic scores matter?

-- rank every game by sales, then see how much the top ones make
with ranked as (
  select sales, row_number() over (order by sales desc) as rnk from fact_games
)
select
  round(100.0 * sum(case when rnk <= 10 then sales end) / sum(sales), 1) as top_10_pct,
  round(100.0 * sum(case when rnk <= 100 then sales end) / sum(sales), 1) as top_100_pct,
  round(100.0 * sum(case when rnk <= 1000 then sales end) / sum(sales), 1) as top_1000_pct
from ranked;

-- how many games sold over 1 million, and how many under 100k
select
  sum(case when sales >= 1 then 1 else 0 end) as million_sellers,
  sum(case when sales < 0.1 then 1 else 0 end) as under_100k,
  count(*) as all_games
from fact_games;

-- critic score bands (only games that have a score)
select
  case when critic_score <= 6 then '6 or less'
       when critic_score <= 7 then '6 to 7'
       when critic_score <= 8 then '7 to 8'
       when critic_score <= 9 then '8 to 9'
       else 'over 9' end as score_band,
  count(*) as games,
  round(avg(sales), 2) as avg_sales_m
from fact_games
where critic_score is not null
group by score_band
order by min(critic_score);
