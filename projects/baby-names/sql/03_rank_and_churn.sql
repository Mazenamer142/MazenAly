-- 03 who is number one, and how fast do the top names change?

with ranked as (
  select
    year, gender, name, births,
    rank() over (partition by year, gender order by births desc) as rnk,
    100.0 * births / sum(births) over (partition by year, gender) as share_pct
  from nat_names
)
select year, gender, name, births, round(share_pct, 2) as share_pct
from ranked
where rnk = 1
order by gender, year;

-- of the top 100 names in 1980, how many are still in the top 100 in 2009? same for the top 10
with r as (
  select year, gender, name, rank() over (partition by year, gender order by births desc) as rnk
  from nat_names
  where year in (1980, 2009)
)
select
  a.gender,
  sum(case when a.rnk <= 100 and b.rnk <= 100 then 1 else 0 end) as top100_kept,
  sum(case when a.rnk <= 10 and b.rnk <= 10 then 1 else 0 end) as top10_kept
from r a
join r b on b.gender = a.gender and b.name = a.name and a.year = 1980 and b.year = 2009
group by a.gender;

-- how many times did a name enter the top 10 after not being in it the year before? (by gender, 1981 to 2009)
with r as (
  select year, gender, name, rank() over (partition by year, gender order by births desc) as rnk
  from nat_names
),
t as (select * from r where rnk <= 10)
select cur.gender, count(*) as new_top10_entries
from t cur
where cur.year > 1980
  and not exists (select 1 from t prev where prev.gender = cur.gender and prev.name = cur.name and prev.year = cur.year - 1)
group by cur.gender;

-- where were the 2009 top 10 names in 1980? (empty rank = not in the file that year)
with r as (
  select year, gender, name, rank() over (partition by year, gender order by births desc) as rnk
  from nat_names
  where year in (1980, 2009)
)
select b.gender, b.name, b.rnk as rank_2009, a.rnk as rank_1980
from r b
left join r a on a.gender = b.gender and a.name = b.name and a.year = 1980
where b.year = 2009 and b.rnk <= 10
order by b.gender, b.rnk;
