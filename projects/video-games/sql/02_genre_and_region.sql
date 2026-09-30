-- 02 genres and regions

select
  genre,
  count(*) as games,
  round(sum(sales), 1) as sales_m,
  round(sum(sales) / count(*), 2) as avg_per_game_m,
  round(100.0 * sum(sales) / (select sum(sales) from fact_games), 1) as share_pct
from fact_games
group by genre
order by sales_m desc;

-- what share of each region's sales does each genre have?
select
  genre,
  round(100.0 * sum(na_sales) / (select sum(na_sales) from fact_games), 1) as north_america,
  round(100.0 * sum(pal_sales) / (select sum(pal_sales) from fact_games), 1) as europe_africa,
  round(100.0 * sum(jp_sales) / (select sum(jp_sales) from fact_games), 1) as japan,
  round(100.0 * sum(other_sales) / (select sum(other_sales) from fact_games), 1) as other
from fact_games
group by genre
order by sum(sales) desc;

-- region totals
select
  round(sum(na_sales)) as north_america,
  round(sum(pal_sales)) as europe_africa,
  round(sum(jp_sales)) as japan,
  round(sum(other_sales)) as other
from fact_games;
