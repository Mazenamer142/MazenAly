-- 06 the sound of names: last letters, name families, length

-- share of babies whose name ends in "n", every year
select
  gender, year,
  round(100.0 * sum(case when lower(substr(name, -1)) = 'n' then births else 0 end) / sum(births), 1) as pct_ends_in_n
from nat_names
group by gender, year
order by gender, year;

-- which last letters moved the most between 1980 and 2009? (points of share)
select
  gender,
  lower(substr(name, -1)) as last_letter,
  round(100.0 * sum(case when year = 2009 then births else 0 end) / (select sum(births) from nat_names x where x.gender = n.gender and x.year = 2009)
      - 100.0 * sum(case when year = 1980 then births else 0 end) / (select sum(births) from nat_names x where x.gender = n.gender and x.year = 1980), 1) as change_pts
from nat_names n
where year in (1980, 2009)
group by gender, lower(substr(name, -1))
order by gender, change_pts;

-- the "-den" family for boys: aiden, jayden, hayden, brayden, caden, kaden...
select
  year,
  round(100.0 * sum(case when lower(name) like '%aden' or lower(name) like '%ayden' or lower(name) like '%aiden' then births else 0 end) / sum(births), 2) as pct_den_family
from nat_names
where gender = 'M'
group by year
order by year;

select name, sum(births) as births
from nat_names
where gender = 'M' and (lower(name) like '%aden' or lower(name) like '%ayden' or lower(name) like '%aiden')
group by name
order by births desc
limit 8;

-- average name length (weighted by babies)
select year, round(1.0 * sum(length(name) * births) / sum(births), 2) as avg_length
from nat_names
group by year
order by year;

-- not every name that ends in n went up. biggest changes in share of boys, 1980 to 2009 (points)
select name,
  round(100.0 * sum(case when year = 2009 then births else 0 end) / (select sum(births) from nat_names where gender = 'M' and year = 2009)
      - 100.0 * sum(case when year = 1980 then births else 0 end) / (select sum(births) from nat_names where gender = 'M' and year = 1980), 2) as change_pts
from nat_names
where gender = 'M' and lower(substr(name, -1)) = 'n' and year in (1980, 2009)
group by name
order by change_pts desc
limit 8;

select name,
  round(100.0 * sum(case when year = 2009 then births else 0 end) / (select sum(births) from nat_names where gender = 'M' and year = 2009)
      - 100.0 * sum(case when year = 1980 then births else 0 end) / (select sum(births) from nat_names where gender = 'M' and year = 1980), 2) as change_pts
from nat_names
where gender = 'M' and lower(substr(name, -1)) = 'n' and year in (1980, 2009)
group by name
order by change_pts
limit 4;
