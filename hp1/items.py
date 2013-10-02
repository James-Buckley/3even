from scrapy.item import Item, Field
# This is the data model
# ADD NEW ITEMS STEP 2 add entry below and map it to a 
# datamapping in spider.py and then an output mapping in 
# pipeline.py

# every feild here maps 1:1 to the Load_ model | device table
class CarepackItems(Item):
    srcurl = Field()        # url of the main product page (source)
    cpsku = Field()         # 1.1.1
    cppriceamt = Field()    # 1.2 
    cpurl = Field()         # 1.3
    cpsubcattext  = Field() # 1.0
    cptitletext = Field()   # 1.1.2
    cptitle2text= Field()   # 1.4
    cpdescr_html= Field()   # 1.5
    cpspecs_html = Field()  # 1.8
    pass


class ModelItems(Item):
   mcpsku = Field()    # Used join to Carepack
   mdescr = Field()    # 1.6  
   murl = Field()      # 1.7.1
   mprodid = Field()   # 1.7.2
   mcatid = Field()    # 1.7.4
   msubcatid = Field() # 1.7.3
   pass
       
   
