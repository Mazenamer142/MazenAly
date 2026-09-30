-- 02 are names getting more varied?
-- effective number of names = 1 / sum of (share squared). if every baby had a different name it would be the
-- number of babies, if all had the same name it would be 1. it is an easy way to compare years.

with shares as (
  select
    year, gender, name,
    1.0 * births / sum(births) over (partition by year, gender) as share,
    row_number() over (partition by year, gender order by births desc) as rnk
  from nat_names
)
select
  year, gender,
  count(*) as unique_names,
  round(100 * sum(case when rnk <= 10 then share end), 1) as top10_pct,
  round(1.0 / sum(share * share)) as effective_names
from shares
group by year, gender
order by gender, year;
