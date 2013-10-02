 select  "CHECKING ON THE LOAD PROGRESS";
 


 select count(1) as "visited main product pages" from (select distinct srcurl from load_carepack where loadFlag='N') as a;

 select count(1) as "devices records loaded" from load_model  where loadFlag='N';

 select count(1) as "carepacks loaded" from  load_carepack  where loadFlag='N';

select srcurl as "Product pages not scrape all 100 products", count(1) as "carepack count" from load_carepack  where loadFlag='N' group by srcurl having count(1) < 100;
