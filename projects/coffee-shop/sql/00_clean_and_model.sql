-- 00 checks and clean tables
-- the raw table is called sales, one row = one product line on a receipt

select count(*) as sale_lines from sales;

-- ids should be unique
select count(*) - count(distinct transaction_id) as duplicate_ids from sales;

-- any empty cells?
select count(*) as rows_with_nulls
from sales
where transaction_id is null or transaction_date is null or transaction_time is null
   or transaction_qty is null or store_id is null or product_id is null or unit_price is null;

-- date range
select min(transaction_date) as first_day, max(transaction_date) as last_day from sales;

-- some products have more than one price, i want to know how many
select count(*) as products_with_2_prices
from (select product_id from sales group by product_id having count(distinct unit_price) > 1);

drop table if exists dim_product;
create table dim_product as
select distinct product_id, product_category as category, product_type, product_detail as product
from sales;

drop table if exists dim_store;
create table dim_store as
select distinct store_id, store_location
from sales;

-- fact table: one row per line, with revenue, hour, weekday and size added
drop table if exists fact_sales;
create table fact_sales as
select
  transaction_id as sale_id,
  transaction_date as sale_date,
  substr(transaction_date, 1, 7) as month,
  cast(substr(transaction_time, 1, 2) as integer) as hour,
  cast(strftime('%w', transaction_date) as integer) as weekday_num,   -- 0 = sunday
  store_id,
  store_location,
  product_id,
  product_category as category,
  product_type,
  product_detail as product,
  case when product_detail like '% Sm' then 'Small'
       when product_detail like '% Rg' then 'Regular'
       when product_detail like '% Lg' then 'Large'
       else 'No size' end as size,
  transaction_qty as qty,
  unit_price,
  transaction_qty * unit_price as revenue
from sales;
