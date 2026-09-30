-- 07 regions

select region, count(distinct state) as states, sum(births) as births,
  round(100.0 * sum(births) / (select sum(births) from fact_names), 1) as share_pct
from fact_names
group by region
order by births desc;

-- signature names: how many times more common is a name in a region than in the whole country?
-- (location quotient = share in the region / share nationally, names with 30,000+ babies)
with reg as (
  select region, gender, name, sum(births) as b from fact_names group by region, gender, name
),
reg_total as (select region, gender, sum(b) as t from reg group by region, gender),
nat as (select gender, name, sum(b) as b from reg group by gender, name),
nat_total as (select gender, sum(b) as t from nat group by gender),
lq as (
  select r.region, r.gender, r.name, (1.0 * r.b / rt.t) / (1.0 * n.b / nt.t) as lq
  from reg r
  join reg_total rt on rt.region = r.region and rt.gender = r.gender
  join nat n on n.gender = r.gender and n.name = r.name
  join nat_total nt on nt.gender = r.gender
  where n.b >= 30000
),
ranked as (select *, row_number() over (partition by region order by lq desc) as rn from lq)
select region, name, gender, round(lq, 1) as lq
from ranked
where rn <= 5
order by region, rn;

-- how varied are names in each region in 2009? (effective number of names, as in script 02)
with s as (
  select region, gender, name, 1.0 * sum(births) / sum(sum(births)) over (partition by region, gender) as share
  from fact_names
  where year = 2009
  group by region, gender, name
)
select region, gender, round(1.0 / sum(share * share)) as effective_names
from s
group by region, gender
order by gender, effective_names desc;

-- number one name in each region in 2009
with s as (
  select region, gender, name, sum(births) as b,
    row_number() over (partition by region, gender order by sum(births) desc) as rn
  from fact_names
  where year = 2009
  group by region, gender, name
)
select region, gender, name from s where rn = 1 order by region, gender;
