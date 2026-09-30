-- 00 clean the raw tables and build the tables the other scripts use
-- (I imported the 4 csv files as products, stores, inventory and sales. written in sqlite)

-- checks first, these should all be 0 except the counts
select count(*) as sales_rows from sales;
select count(*) - count(distinct sale_id) as duplicate_sale_ids from sales;
select count(*) as orphan_products from sales where product_id not in (select product_id from products);
select count(*) as orphan_stores from sales where store_id not in (select store_id from stores);
select count(*) as inventory_rows from inventory;

-- cost and price are stored as text like '$9.99 ' so remove the $ and spaces
drop table if exists dim_product;
create table dim_product as
select product_id as product_id,
  product_name as product_name,
  product_category as category,
  cast(replace(replace(trim(product_cost), '$', ''), ',', '') as real) as unit_cost,
  cast(replace(replace(trim(product_price), '$', ''), ',', '') as real) as unit_price
from products;

-- mexico city is spelled 'Cuidad' in the city column but 'Ciudad' in the store name, fixed it
drop table if exists dim_store;
create table dim_store as
select store_id as store_id,
  store_name as store_name,
  case when store_city = 'Cuidad de Mexico' then 'Ciudad de Mexico' else store_city end as city,
  store_location as location_type,
  store_open_date as open_date
from stores;

-- main table, one row per sale with revenue, cost and profit
drop table if exists fact_sales;
create table fact_sales as
select s.sale_id as sale_id,
  s.date as sale_date,
  substr(s.date, 1, 7) as year_month,
  cast(substr(s.date, 1, 4) as integer) as year,
  cast(substr(s.date, 6, 2) as integer) as month_num,
  s.store_id as store_id,
  s.product_id as product_id,
  s.units as units,
  s.units * p.unit_price as revenue,
  s.units * p.unit_cost as cost,
  s.units * (p.unit_price - p.unit_cost) as profit
from sales s
join dim_product p on p.product_id = s.product_id;

create index idx_fact_store on fact_sales(store_id);
create index idx_fact_product on fact_sales(product_id);

drop table if exists fact_inventory;
create table fact_inventory as
select store_id as store_id, product_id as product_id, stock_on_hand as stock_on_hand from inventory;
