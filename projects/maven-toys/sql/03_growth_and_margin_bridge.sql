-- 03 growth vs profit
-- the data stops on 30 sep 2023 so i compare jan-sep of both years

select year,
  round(sum(revenue)) as revenue,
  round(sum(profit)) as profit,
  round(sum(profit) * 100.0 / sum(revenue), 1) as margin_pct
from fact_sales
where month_num <= 9
group by year
order by year;

-- profit change per product (jan-sep 2022 vs jan-sep 2023)
select p.product_name,
  p.category,
  round(sum(case when f.year = 2022 then f.profit else 0 end)) as profit_2022,
  round(sum(case when f.year = 2023 then f.profit else 0 end)) as profit_2023,
  round(sum(case when f.year = 2023 then f.profit else 0 end) - sum(case when f.year = 2022 then f.profit else 0 end)) as profit_change,
  sum(case when f.year = 2022 then f.units else 0 end) as units_2022,
  sum(case when f.year = 2023 then f.units else 0 end) as units_2023
from fact_sales f
join dim_product p on p.product_id = f.product_id
where f.month_num <= 9
group by p.product_id, p.product_name, p.category
order by profit_change;

-- margin bridge
-- each product has one price and one cost, so its margin never changes.
-- that means the overall margin only moves when the mix of what we sell changes.
-- contribution = (share of revenue 2023 - share 2022) * (product margin - overall margin 2022)
with by_product as (
  select product_id,
    sum(case when year = 2022 then revenue else 0 end) as rev22,
    sum(case when year = 2023 then revenue else 0 end) as rev23,
    sum(case when year = 2022 then profit else 0 end) as prof22
  from fact_sales
  where month_num <= 9
  group by product_id
),
totals as (
  select sum(rev22) as t22, sum(rev23) as t23, sum(prof22) / sum(rev22) as margin22
  from by_product
)
select p.product_name,
  round(b.rev22 * 100.0 / t.t22, 2) as rev_share_2022_pct,
  round(b.rev23 * 100.0 / t.t23, 2) as rev_share_2023_pct,
  round((p.unit_price - p.unit_cost) * 100.0 / p.unit_price, 1) as product_margin_pct,
  round(100.0 * (b.rev23 / t.t23 - b.rev22 / t.t22) * ((p.unit_price - p.unit_cost) / p.unit_price - t.margin22), 2) as contribution_pp
from by_product b
cross join totals t
join dim_product p on p.product_id = b.product_id
order by contribution_pp;
