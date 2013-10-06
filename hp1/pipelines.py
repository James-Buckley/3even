from scrapy import log
from twisted.enterprise import adbapi
import time
import MySQLdb.cursors
from  hp1.items import CarepackItems 
from  hp1.items import ModelItems
from  scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.contrib.exporter import CsvItemExporter
# Custom exporters
import csv

# OUTPUT data, simply spider send each item scraped to this
# pipeline for furhter processing in our case, load to DB
# Have csv and mysql options (see settings.py) for activation

class CSV1Pipeline(object):
    def __init__(self):
       # required code to start
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
#NOTE CSV need more comment
# we use mysql so i annote that
  # steps to take when spider starts
  # init DB       
    def spider_open(self, spider):
        self.csv_exporter_item   = CsvItemExporter(open("carepack.csv", "w"),quoting=csv.QUOTE_ALL )
        self.csv_exporter_detail = CsvItemExporter(open("model.csv"   ,"w" ),quoting=csv.QUOTE_ALL )

        # Make a quick copy of the list
        self.csv_exporter_item.start_exporting()
        self.csv_exporter_detail.start_exporting()


    def spider_closed(self, spider):
        self.csv_exporter_item.finish_exporting()
        self.csv_exporter_detail.finish_exporting()



    def process_item(self, item, spider):
        if (item, CarepackItems):
            self.csv_exporter_item.export_item(item)      
        elif isinstance(item, ModelItems):
            self.csv_exporter_detail.export_item(item)
        return item


    def storeHeaders(item, spider):
        pass # make some things with Headers item here

    def storeBody(item, spider):
        pass # make some things with Body item here




# send info to DB, this hase db info  (until i put in seperate file)

class MySQL1StorePipeline(object):

    def __init__(self):
        # @@@ hardcoded db settings
        # TODO: make settings configurable through settings
        # connect open and close function to transmitter (workflow)
        # what to call to load the DB when all is done
        dispatcher.connect(self.spider_closed, signals.spider_closed)

                
  

        self.conn = MySQLdb.connect(user='root', passwd='', db='hp1', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor() 
        self.cursor.execute("""INSERT INTO xlog( logType, logMessage ) VALUES ( %s, %s ) """ ,("load", "Start batch load"));
        self.conn.commit()    
    
    def process_item(self, item, spider):
        # run db query in thread pool

# Only issue with scrappy need to define how to handle each type
# model or device (they are adding a more generic solution)
# we only hae two objects so no real problem
       
# if care pack or model/device send data to load table
        if isinstance(item, CarepackItems):
            try:
                self.cursor.execute("""INSERT INTO load_carepack(srcurl, cpsku, cpurl, cppriceamt, cpsubcattext, cptitletext , cptitle2text , cpdescr_html, cpspecs_html, cptext1)
                       VALUES (%s, %s, %s ,%s,  %s, %s, %s, %s, %s ,%s ) """ ,
                      ( item["srcurl"].encode("utf-8"),
                        item['cpsku'].encode('utf-8'), 
                        item['cpurl'].encode('utf-8'),
                        item['cppriceamt'].replace(',','').encode('utf-8'),
                        item['cpsubcattext'].encode('utf-8'),
                        item['cptitletext'].encode('utf-8'),
                        item['cptitle2text'].encode('utf-8'),
                        item['cpdescr_html'].encode('utf-8','ignore'),
                        item['cpspecs_html'].encode('utf-8','ignore'),
                        item['cptext1'].encode('utf-8','ignore')                     
                          ))
                self.conn.commit()
       # note: ignore means if encounter non asci char just drop remove, ok for this site, not for german language 
            except MySQLdb.Error, e:

                msg = "Error %d: %s" % (e.args[0], e.args[1])
                self.cursor.execute("""INSERT INTO xlog( logType, logMessage ) VALUES ( %s, %s ) """ ,("ERROR", msg))
                self.conn.commit()
                log.msg(msg, level=log.ERROR)



 
        if isinstance(item, ModelItems):
           
            try:
                self.cursor.execute("""INSERT INTO load_model(mcpsku, mdescr,  murl, mprodid, msubcatid, mcatid    )
                       VALUES (%s, %s ,%s,  %s, %s, %s ) """ ,
                      ( item['mcpsku'].encode('utf-8'),
                        item['mdescr'].encode('utf-8'),
                        item['murl'].encode('utf-8'),
                        item['mprodid'].encode('utf-8'),
                        item['msubcatid'].encode('utf-8'),
                        item['mcatid'].encode('utf-8')
                         ) )



                self.conn.commit()



            except MySQLdb.Error, e:
                msg = "Error %d: %s" % (e.args[0], e.args[1])
                self.cursor.execute("""INSERT INTO xlog( logType, logMessage ) VALUES ( %s, %s ) """ ,("ERROR", msg))
                self.conn.commit()  
                log.msg(msg, level=log.ERROR)

# After load send data from load table to live tables
# todo add sql


    def spider_closed(self,spider):

        self.cursor.execute("""INSERT INTO xlog( logType, logMessage ) VALUES ( %s, %s ) """ , ("END", "batch loaded data") );
        self.conn.commit()
        try:



            self.cursor.execute("""INSERT INTO xlog( logType, logMessage ) VALUES ( %s, %s ) """ ,("normalize", "Move data from load to live table"))

            self.conn.commit()
        
            self.cursor.execute("""insert into  carepack_categories (RawCategory) select distinct cpsubcattext from load_carepack where  cpsubcattext not in (select RawCategory from carepack_categories)""")


     
            self.cursor.execute("""insert into carepacks (SKU, Title1, Title2, Price, Raw1,  Raw2, Link, fkCategory) select cpsku , cptitletext, cptitle2text, cppriceamt, cpdescr_html, cpspecs_html, cpurl, cat.pk From load_carepack join carepack_categories cat on  cpsubcattext = cat.RawCategory where cpsku  not in (select SKU from carepacks) and loadFlag=%s """, ('N',) )


            self.cursor.execute("""insert into devices (prodID, CatID, SubCatID, deviceName, Link) select distinct mprodid, mcatid, msubcatid, mdescr, murl from load_model where loadFlag = %s  and mprodid  not in (select prodID from devices)""", ('N',) ) 

# Our own little y2k bug, not work if carepack exced 99999999, can replace this
#simple append logic with database stored procedure but did nto want add anything
# to database OR use actual SKU id to test, but using keys  Much Faster


            self.cursor.execute("""insert into  devices_carepacks (fkDevice, fkCarepack) select distinct D.pk, C.pk from load_model L join carepacks  C  on (L.mcpsku = C.SKU) join devices D on (L.mprodid = D.prodID) where loadFlag = %s and D.pk * 1000000 + C.pk not in (select fkDevice* 1000000 + fkCarepack from devices_carepacks)""",('N',))

            self.conn.commit()
        
            self.cursor.execute("""update load_model set loadFlag =%s where loadFlag = %s""", ('L','N') )
            self.cursor.execute("""update load_carepack set loadFlag =%s where loadFlag = %s""", ('L','N') )   
         
            self.conn.commit()


            #self.cursor.execute( """Update carepacks set title2 = %s where length(title2) >=60""",('Empty',) )

            self.conn.commit()


        except MySQLdb.Error, e:
            msg="Error %d: %s" % (e.args[0], e.args[1])
            log.msg( msg, level=log.ERROR)
            self.conn.commit() 

