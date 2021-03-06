from scrapy import log
from xml.sax.saxutils import escape, unescape
from scrapy.spider                      import  BaseSpider  
from scrapy.selector                    import  HtmlXPathSelector
from hp1.items                        import  CarepackItems
from hp1.items  import ModelItems
from scrapy.contrib.exporter            import CsvItemExporter
from scrapy.contrib.exporter            import JsonItemExporter
from scrapy.contrib.exporter            import JsonLinesItemExporter
from scrapy.contrib.exporter            import XmlItemExporter
from scrapy.contrib.exporter            import BaseItemExporter
from scrapy.contrib.spiders             import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor 
import re
import time
from urlparse import urlparse, parse_qs



#NOTE: see for loop at start_urls to set how many product pages
# are scraped

# Spider parses each start url page for product links and visits each 
# product site for processing
# Parse helpers
# String (html) => String (special char converted)
# get raw html ready for DB storage and xfer to other modules
# convert newlines " and ' to html codes
# String (html)  => Strign with special chars encoded < -> &lt, for DB load
def html_escape(str):
    s = str.encode('ascii', 'ignore')
    return s

# Main crawl
# crawl each of the product list sites then scrap the carepack info
# then create an item for each model(device)
# Crawl (object) => Yields record for each carepack and device to
# pipeline for further processing

class Site1Spider(CrawlSpider):


    name = 'hp1'
    # NOTE PAGE RANGE  Inclusive of start, NON inclusive of end
    # 1,5  read pages 1 to 4 (i could add 1 to end  but wanted keep native python
    # rane behavior
    PAGE_RANGE=xrange(1,244) # DETERMNINES HOW MANY PRODUCT PAGES TO VISIT

    log.msg("Start Spider: %s" % name, level=log.INFO)



# test harness
# INPUT FILE urls.txt with address to the  CP
#    f = open("urls.txt")
#    start_urls = [url.strip() for url in f.readlines()]
#    f.close()
# end test harness


# How to find the links on each main product page
# issue call back to scrape the product pages once they load
    rules = (
        Rule(SgmlLinkExtractor(allow='/product/sku/'), callback='parse_item', follow=True),
        )


    start_urls=['http://h30094.www3.hp.com/searchresults.aspx?itemsperpage=100&page=%s&culture=en-US&store_id=9&pagesize=100&sortorder=prg&price_min=-1&cache=-1036814934&price_max=2147483647'% page for page in PAGE_RANGE]

#    f=open("./urls.txt")
#    start_urls = [url.strip() for url in f.readlines()]
#   f.close()

# Limits leaving the main site
    allowed_domains = ['hp.com']

# stop redirect during IP-limiting
    meta = {'dont_redirect': True}    

# Start code in case run from command line
    #def __init__(self, *args, **kwargs): 
     #   super(Site1Spider, self).__init__(*args, **kwargs) 
     #   self.start_urls = [kwargs.get('start_url')] 
# End code used to run from command line Test

# Start write file helper, not used, debug purposes
    def write(data, outfile):
        f= open(outfile, "w+b")
        pickle.dump(data, f)
        f.close()
# End write file helper for debug
    # String => Strign with special chars encoded

    

# Parse each product page

    def parse_item(self, response):


        item=CarepackItems()       
        hxs = HtmlXPathSelector(response)
# BEGINE Css selectors
# If need to add an element or change where we get it only add here
# ADD NEW ITEM STEP 1.  add css select below
    
        cppriceamt_sel   =  '//div[@class="price"]/span[2]/strong/text()'
        cptitle2text_sel =  '//table/tr/td[@class="cnet_textparagraph"]/text()'
        cppagetitle_sel  =  '//title/text()' 

        cpdescr_html_sel =  '//*[@id="overviewContent"]'
        cpspecs_html_sel =  '//*[@id="specsContent"]'
        cpmodel_list_sel =  '//div[@id="overviewContent"]//span[@class="FlyoutMenuProduct"]'
        cptitle1text_sel ='//span[@class="longdesc prodPageTitle"]/text()'
        cpsku_sel='//div[contains(@class,"mfgPartNo")]/text()'
        cpsubcattext_sel='//div[@class="defaultLink visibleTrue item3"]/span[@class="bread_prodName"]/a[@id="A1"]/text()' 
        # NOTE sute all models have specs and descr 
               
 
        
  

# Map each element to an "ITEM" object array.
# python twisted lib send this array auto. to the pipeline


        # DEVICE INFO
        # NOTE: page (anchor), model and sud cat is selected from the page 
        # title.  The javascript creates this element for those 3 valuse
        # sub cat text live nowhere else in the html except the title
        pagetitle = hxs.select( cppagetitle_sel ).extract()[0].strip()
        prodInfo =  pagetitle.split(" - ")
        item['srcurl']= response.request.headers.get('Referer', None)
      
        #item['srcurl']= response.request.headers.get('Referer', None)
        item["cpsku"] =hxs.select(cpsku_sel).extract()[0].replace("MFG #","").strip()

        
        item["cppriceamt"]= hxs.select(cppriceamt_sel).extract()[0].strip().replace('$','')
        item["cpurl"] = response.url
        # parse from title (sub cat, titel
        item["cpsubcattext"] =hxs.select(cpsubcattext_sel).extract()[0].strip() # prodInfo[1].strip()
        item["cptitletext"] =hxs.select(cptitle1text_sel).extract()[0].strip() #prodInfo[0].strip()
        #Short title (title2) handle if nto present or if there is market text in its place, code can be shoretened but listed to clearly show logic
       # if short title is not there or market info is in its place copy off info and set short title to not present, **** the market info (text1) does nto get moved to live table, stored in load_carepack for ref.  Also any info in that table is also in the html in Raw1 so no info is lost 
        tmp_cptitle2text=hxs.select(cptitle2text_sel).extract()[0].strip()
        if  len(tmp_cptitle2text) > 50 or len(tmp_cptitle2text) < 2:
            item["cptitle2text"] = "Short title not present" 
            item["cptext1"] = tmp_cptitle2text 
        else:
            item["cptitle2text"] = tmp_cptitle2text
            item["cptext1"]='NA'

        # html raw convert special char to html numeric codes
        # to make transfer easier
        item["cpdescr_html"] = html_escape(hxs.select(cpdescr_html_sel).extract()[0] )
        # intoduced bug patch
        #item["cpdescr_html"]="ERROR EMPTY"
        item["cpspecs_html"] = html_escape( hxs.select(cpspecs_html_sel).extract()[0] )
        #item["cpspecs_html"]="ERROR EMPTY"

  

        #MODELS
         

         
        newmodel=ModelItems()
        # for each device there are multiple models
        # parse info
        # Compatable Models
        model_rows =  hxs.select(cpmodel_list_sel) #raw html
        for model in model_rows:
            newmodel['mcpsku'] = item["cpsku"].strip()
            newmodel["murl"]  = model.select('a/@href').extract()[0]
            newmodel["mdescr"] = model.select('span/text()').extract()[0].strip()
           
            qs =   parse_qs(urlparse( newmodel['murl'] ).query )
 
            newmodel["mprodid"] =  qs["prodid"][0].strip()
            newmodel["mcatid"] =qs["catid"][0].strip()
            newmodel["msubcatid"] = qs["subcatid"][0].strip()
           
            yield newmodel
        
        log.msg("Parsed Page: " + response.url, level=log.INFO) 
   
        yield item   
    # author : jpb:
    # date  : Sep 21 2013

