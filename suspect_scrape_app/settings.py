NAME = 'suspects'
#USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
SPIDER_MODULES = ['suspect_scrape_app.spiders']
#DATABASE = {
        #'hostname' = 'ec2-54-83-192-68.compute-1.amazonaws.com',
        #'password' = '3bbdbc41dc14a4c3d05ffb990edb0901befcff1c921864c35becf36c654739bc',
        #'username' = 'tuemchwwqigygt', # your password
        #'database' = 'd4k3frt6kjv0rf',
        #'port' = '5432',
        #}
        #'postgresql://{}:{}@{}:{}/{}'
def get_con_string():
    url = 'postgresql://{}:{}@{}:{}/{}'
    user='tuemchwwqigygt'
    password='3bbdbc41dc14a4c3d05ffb990edb0901befcff1c921864c35becf36c654739bc'
    host='ec2-54-83-192-68.compute-1.amazonaws.com'
    port='5432'
    db='d4k3frt6kjv0rf'
    url = url.format(user, password, host, port, db)
    return url
ITEM_PIPELINES = {
    'suspect_scrape_app.pipelines.SuspectPipeline': 300,
    }
