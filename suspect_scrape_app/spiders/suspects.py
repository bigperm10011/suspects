import scrapy
import re
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.engine.url import URL
import sqlalchemy
from suspect_scrape_app import settings
from sqlalchemy.orm import mapper, sessionmaker
from suspect_scrape_app.items import TrackItem
from helpers import load_tables, remove_html_markup
#################### Spider Description ####################
#grabs 5 leavers sorted by the last time they were scraped
#collects possible suspects after google searching their name & specifying linkedin
#scrapes relevant details and + to db after filtering duplicates
############################################################
class QuotesSpider(scrapy.Spider):
    name = "suspects"
    sesh, Suspect, Leaver = load_tables()
    lvr = sesh.query(Leaver).filter_by(status='Lost', updated='No').order_by(Leaver.timestamp).limit(5).all()
    slinks = sesh.query(Suspect).all()
    link_list = []
    for s in slinks:
        link_list.append(s.link)
    def start_requests(self, sesh=sesh, Leaver=Leaver, lvr=lvr):
        if len(lvr) > 0:
            for l in lvr:
                print('Leaver Selected: ', l.name)
                lid = l.id
                url = 'https://www.google.com/search?q=' + l.name + ' ' + 'site:www.linkedin.com'

                yield scrapy.Request(url=url, callback=self.parse, meta={'lid': l.id})
        else:
            raise CloseSpider('All Leavers Have Suspects')
    def parse(self, response):
        try:
            for i in response.xpath('//*[@id="ires"]/ol/div[@class="g"]'):
                item = TrackItem()
                link_string = str(i.xpath('div/div[1]/cite').extract())
                stage_link = remove_html_markup(link_string).strip('[').strip(']').strip("\'")
                name_placeholder = i.xpath('h3/a/b/text()').extract()
                item['name'] = name_placeholder[0].strip('[').strip(']')
                item['ident'] = response.meta['lid']
                if 'https://www.linkedin.com/pub/dir/' in stage_link or 'site:www.linkedin.com' in name_placeholder[0]:
                    pass
                else:
                    item['link'] = stage_link
                    deet = i.xpath('div/div[2]/text()').extract()
                    if len(deet) == 1:
                        deets = deet[0].replace(u'\xa0-\xa0', u'-')
                        deet_lst = deets.split('-')
                        print('DEET  LIST VALUE: ', deet_lst[1])
                        #print('!!!!!!!!!!', len(deet_lst))
                        if len(deet_lst) == 3:
                            try:
                                item['location'] = deet_lst[0]
                            except:
                                item['location'] = None
                            try:
                                item['role'] = deet_lst[1]
                            except:
                                item['role'] = None
                            try:
                                item['firm'] = deet_lst[2]
                            except:
                                item['firm'] = None
                        else:
                            item['location'] = None
                            item['role'] = None
                            item['firm'] = None
                    item['status'] = 'Success'
                    yield item
        except:
            item = TrackItem()
            item['status'] = 'Fail'
            yield item
