echo "list each main product page and number of product scraped from them"
mysql -u root hp1 -e "select convert( replace(replace(substring(srcurl, 68, 3),'&',''),'c',''),UNSIGNED INTEGER )  a, count(1)  from load_carepack group by a  order by a desc limit 1000;"
