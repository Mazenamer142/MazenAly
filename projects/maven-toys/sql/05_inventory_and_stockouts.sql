-- 05 inventory
-- inventory is only one snapshot (stock today), there is no history.
-- so the lost profit here is an estimate: i assume a product that is out of stock would keep
-- selling at that store's average daily profit from the last 90 days of data.

select round(sum(i.stock_on_hand * p.unit_cost)) as stock_value_at_cost,
  sum(case when i.stock_on_hand = 0 then 1 else 0 end) as stockout_pairs,
  count(*) as store_product_pairs,
  round(sum(case when i.stock_on_hand = 0 then 1 else 0 end) * 100.0 / count(*), 1) as stockout_rate_pct
from fact_inventory i
join dim_product p on p.product_id = i.product_id;

-- daily sales rate per store and product, last 90 days (3 jul to 30 sep 2023)
drop table if exists recent_rate;
create table recent_rate as
select store_id, product_id,
  sum(profit) / 90.0 as daily_profit,
  sum(units) / 90.0 as daily_units
from fact_sales
where sale_date >= '2023-07-03'
group by store_id, product_id;

-- which products are out of stock and what it might cost per 30 days
select p.product_name,
  p.category,
  count(*) as stores_out_of_stock,
  round(sum(coalesce(r.daily_profit, 0)) * 30) as est_profit_at_risk_per_30d,
  round((p.unit_price - p.unit_cost) * 100.0 / p.unit_price) as margin_pct
from fact_inventory i
join dim_product p on p.product_id = i.product_id
left join recent_rate r on r.store_id = i.store_id and r.product_id = i.product_id
where i.stock_on_hand = 0
group by p.product_id, p.product_name, p.category, p.unit_price, p.unit_cost
order by est_profit_at_risk_per_30d desc;

-- slow stock: more than 180 days of stock at the recent selling rate
select count(*) as slow_pairs,
  round(sum(i.stock_on_hand * p.unit_cost)) as capital_tied_up
from fact_inventory i
join dim_product p on p.product_id = i.product_id
join recent_rate r on r.store_id = i.store_id and r.product_id = i.product_id
where r.daily_units > 0 and i.stock_on_hand / r.daily_units > 180;

-- store + product pairs that are missing from the inventory table
select count(*) as pairs_missing_from_inventory,
  sum(case when exists (select 1 from fact_sales f where f.store_id = st.store_id and f.product_id = pr.product_id) then 1 else 0 end) as of_which_have_sales
from dim_store st
cross join dim_product pr
where not exists (select 1 from fact_inventory i where i.store_id = st.store_id and i.product_id = pr.product_id);
