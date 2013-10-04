select count(1) as model_cnt from load_model;
select count(1) as carepack_cnt from load_carepack;
select count(1) as cp from carepacks;
select count(1) as dev from devices;
select count(1) as cat from carepack_categories;
select length(raw1) from carepacks order by length(raw1) desc limit 10;
select length(raw2) from carepacks order by length(raw2) desc limit 10;
select * from devices_carepacks limit 100;
select "subcat";
select * from carepack_categories;
select  devicename from devices limit 200;
select Link from devices limit 100;
select  SKU  from carepacks  order by sku desc limit 100; 
select title1 from carepacks limit 200;
select title2 from carepacks limit 200;
select raw1 from carepacks limit 1;
select raw2 from carepacks limit 1;

