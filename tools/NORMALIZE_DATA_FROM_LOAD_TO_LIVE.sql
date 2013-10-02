

insert into xlog (logType, logMessage) 
values ("normalize", "Start process move data from load tables to live tables.");


commit;

insert into   carepack_categories (RawCategory) 
select distinct cpsubcattext 
from load_carepack 
where  cpsubcattext 
 not in (select RawCategory from carepack_categories);


commit;

select 'insert carepack';
select 'note the use of the flag N this allows us to keep records' ;
select 'even duplicates in the load table for historical purposes';
select 'New records are defaulted with flag -N-ew and then set to ';
select '-L-aded.' ;

commit;

insert into carepacks (SKU, Title1, Title2, Price, Raw1,  Raw2, fkCategory) 
select cpsku , cptitletext, cptitle2text, 
       cppriceamt, cpdescr_html, cpspecs_html, cat.pk 
from load_carepack join carepack_categories cat 
 on  cpsubcattext = cat.RawCategory 
where cpsku 
 not in (select SKU from carepacks) 
  and loadFlag='N'
  and cpsku like 'HP%';

commit;


insert into devices (prodID, CatID, SubCatID, deviceName, Link) 
select distinct mprodid, mcatid, msubcatid, mdescr, murl
from load_model 
where loadFlag = 'N'  
 and mprodid 
 not in (select prodID from devices);

commit;



insert into xlog (logType, logMessage) 
values ("normalize", "End process move data from load tables to live tables.");
commit;




insert into  devices_carepacks (fkDevice, fkCarepack)  
select distinct D.pk, C.pk 
from load_model L 
 join carepacks  C 
  on (L.mcpsku = C.SKU) 
 join devices D 
  on (L.mprodid = D.prodID)  
where loadFlag = 'N';


update load_model set loadFlag ='L' where loadFlag = 'N';
update load_carepack set LoadFlag = 'L' where loadFlag = 'N';
commit;




