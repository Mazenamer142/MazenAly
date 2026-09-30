-- 04 rises, falls and sudden spikes

-- when did names peak? (names with at least 20,000 births in total)
with tot as (
  select gender, name from nat_names group by gender, name having sum(births) >= 20000
),
p as (
  select n.gender, n.name, n.year,
    row_number() over (partition by n.gender, n.name order by n.births desc, n.year) as rn
  from nat_names n
  join tot t on t.gender = n.gender and t.name = n.name
)
select year as peak_year, count(*) as names
from p
where rn = 1
group by year
order by year;

-- the biggest one-year jumps (names that already had 1,500+ babies that year)
with j as (
  select a.gender, a.name, a.year, a.births, coalesce(b.births, 0) as prev
  from nat_names a
  left join nat_names b on b.gender = a.gender and b.name = a.name and b.year = a.year - 1
  where a.year > 1980 and a.births >= 1500
)
select gender, name, year, births, prev, round(1.0 * births / (prev + 1), 1) as jump
from j
order by jump desc
limit 8;

-- yearly babies for a few names (used for the line charts)
select gender, name, year, births
from nat_names
where (gender = 'F' and name in ('Jennifer', 'Jessica', 'Emily', 'Emma', 'Madison', 'Nevaeh'))
   or (gender = 'M' and name in ('Michael', 'Jacob', 'Jayden'))
order by gender, name, year;
