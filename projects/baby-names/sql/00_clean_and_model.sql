-- 00 checks and clean tables
-- raw tables: names (state, gender, year, name, births) and regions (state, region)

select count(*) as rows_in_file from names;

select count(*) as rows_with_nulls
from names
where state is null or gender is null or year is null or name is null or births is null;

-- same state + gender + year + name twice?
select count(*) as duplicate_rows
from (select state, gender, year, name from names group by state, gender, year, name having count(*) > 1);

select min(year) as first_year, max(year) as last_year, min(births) as smallest_count from names;

-- states that are in names but not in regions
select count(distinct state) as states_missing_from_regions
from names
where state not in (select state from regions);

-- region labels, one of them looks off
select region, count(*) as states from regions group by region order by region;

-- fix the regions table: "New England" was written two ways, and michigan is missing (it is in the midwest)
drop table if exists dim_region;
create table dim_region as
select state as state, case when region = 'New England' then 'New_England' else region end as region
from regions
union all
select 'MI', 'Midwest';

-- main table: every row of names plus its region
drop table if exists fact_names;
create table fact_names as
select n.state as state, r.region as region, n.gender as gender, n.year as year, n.name as name, n.births as births
from names n
join dim_region r on r.state = n.state;

create index ix_fact on fact_names(year, gender, name);

-- national totals per name, year and gender (used by most of the other scripts)
drop table if exists nat_names;
create table nat_names as
select year, gender, name, sum(births) as births
from fact_names
group by year, gender, name;

create index ix_nat on nat_names(gender, name, year);

-- did the join lose any rows?
select (select count(*) from names) - (select count(*) from fact_names) as rows_lost;
