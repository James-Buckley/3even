# Scrapy settings for hp1 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

# Quote all settings

BOT_NAME = 'hp1'

# this is pretty low to prevent IP block
CONCURRENT_ITEMS=16

#  must have for it block
COOKIES_ENABLED=False

# keep this between 2-6 for ip ban
CONCURRENT_REQUESTS=16

# .5 seconds to prevent IP ban AND !!!!!
# must be 2+ seconds to give the user agent module time
# we switch the user agent for each get
# note most site happy with 1 second but we need 2.5 or mote
DOWNLOAD_DELAY=.5


# The spider to use
SPIDER_MODULES=['hp1.spiders']
NEWSPIDER_MODULE='hp1.spiders'
LOG_LEVEL="DEBUG"

# Where sejnd the data, option mysql or CSV
ITEM_PIPELINES = ['hp1.pipelines.MySQL1StorePipeline'] #'hp1.pipelines.CSV1Pipeline']

DUPEFILTER_CLASS='scrapy.dupefilter.BaseDupeFilter'
# USER AGENT NOT USED we use a "middleware"
## to inject a new agent each get (see log)
#SER_AGENT='Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; en; rv:1.9.0.19) Gecko/2011091218 Camino/2.0.9 (like Firefox/3.0.19)'
DOWNLOADER_MIDDLEWARES = {
     'hp1.middleware.CustomUserAgentMiddleware': 545,
}
# force FIFO search prevent throttle
# the below is a hack to force FIFO gets
# otherwise LIFo (beadth search,, makes sennse if deep 
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'
