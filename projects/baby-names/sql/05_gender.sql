-- 05 names that both boys and girls get

select count(*) as names_used_for_both
from (select name from nat_names group by name having count(distinct gender) = 2);

-- the most used names that are close to even (girls between 20% and 80%), 50,000+ babies
select
  name,
  sum(case when gender = 'F' then births else 0 end) as girls,
  sum(case when gender = 'M' then births else 0 end) as boys,
  round(100.0 * sum(case when gender = 'F' then births else 0 end) / sum(births)) as girls_pct
from nat_names
group by name
having sum(births) >= 50000
   and 100.0 * sum(case when gender = 'F' then births else 0 end) / sum(births) between 20 and 80
order by sum(births) desc;

-- names that changed side: girls' share in the 1980s vs the 2000s (20,000+ babies, used in both periods)
select
  name,
  round(100.0 * sum(case when gender = 'F' and year <= 1989 then births else 0 end) / sum(case when year <= 1989 then births else 0 end)) as girls_pct_80s,
  round(100.0 * sum(case when gender = 'F' and year >= 2000 then births else 0 end) / sum(case when year >= 2000 then births else 0 end)) as girls_pct_00s,
  sum(births) as total
from nat_names
group by name
having sum(births) >= 20000
   and sum(case when year <= 1989 then births else 0 end) > 0
   and sum(case when year >= 2000 then births else 0 end) > 0
order by (100.0 * sum(case when gender = 'F' and year >= 2000 then births else 0 end) / sum(case when year >= 2000 then births else 0 end))
       - (100.0 * sum(case when gender = 'F' and year <= 1989 then births else 0 end) / sum(case when year <= 1989 then births else 0 end));
