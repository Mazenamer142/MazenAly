-- 00 checks and clean tables
-- raw table is called games. one row = one game on one console

select count(*) as rows_in_file from games;

-- only some rows have sales numbers, how many?
select
  count(*) as all_rows,
  count(total_sales) as rows_with_sales,
  round(100.0 * count(total_sales) / count(*), 1) as pct_with_sales
from games;

-- do the four regions add up to the total? (empty region = no sales recorded)
select count(*) as rows_where_regions_dont_add_up
from games
where total_sales is not null
  and abs(coalesce(na_sales, 0) + coalesce(jp_sales, 0) + coalesce(pal_sales, 0) + coalesce(other_sales, 0) - total_sales) > 0.05;

-- same title + console twice?
select count(*) as repeated_title_console
from (select title, console from games where total_sales is not null group by title, console having count(*) > 1);

-- rows with sales but no release date
select count(*) as sales_rows_without_date
from games
where total_sales is not null and release_date is null;

-- publisher names that mean the same company. i checked the top publishers by hand
drop table if exists publisher_map;
create table publisher_map as
select distinct publisher as raw_name,
  case
    when publisher in ('EA Sports', 'EA Sports BIG') then 'Electronic Arts'
    when publisher in ('Namco', 'Namco Bandai', 'Namco Bandai Games', 'Bandai') then 'Bandai Namco'
    when publisher in ('Warner Bros. Interactive', 'Warner Bros. Interactive Entertainment') then 'Warner Bros'
    when publisher in ('2K Sports', '2K Games') then '2K'
    when publisher in ('Microsoft Game Studios', 'Microsoft Studios') then 'Microsoft'
    when publisher = 'Konami Digital Entertainment' then 'Konami'
    else publisher end as publisher
from games;

-- clean table: only games with sales, blanks in regions turned into 0
drop table if exists fact_games;
create table fact_games as
select
  g.title,
  g.console,
  case
    when g.console in ('PS', 'PS2', 'PS3', 'PS4', 'PSP', 'PSV', 'PSN') then 'PlayStation'
    when g.console in ('XB', 'X360', 'XOne', 'XBL') then 'Xbox'
    when g.console in ('NES', 'SNES', 'N64', 'GC', 'Wii', 'WiiU', 'NS', 'GB', 'GBC', 'GBA', 'DS', '3DS', 'VC') then 'Nintendo'
    when g.console in ('GEN', 'SAT', 'DC', 'SCD', 'GG') then 'Sega'
    when g.console in ('PC', 'OSX') then 'PC'
    else 'Other' end as platform_family,
  g.genre,
  m.publisher,
  g.critic_score,
  g.total_sales as sales,
  coalesce(g.na_sales, 0) as na_sales,
  coalesce(g.jp_sales, 0) as jp_sales,
  coalesce(g.pal_sales, 0) as pal_sales,
  coalesce(g.other_sales, 0) as other_sales,
  cast(substr(g.release_date, 1, 4) as integer) as release_year
from games g
join publisher_map m on m.raw_name = g.publisher
where g.total_sales is not null;
