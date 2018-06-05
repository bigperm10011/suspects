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

class QuotesSpider(scrapy.Spider):
    name = "testing"
    sesh, Suspect, Leaver = load_tables()
    lvr = sesh.query(Leaver).filter_by(status='Lost', updated='No').order_by(Leaver.timestamp).limit(5).all()


    slinks = sesh.query(Suspect).all()
    link_list = []
    for s in slinks:
        link_list.append(s.link)
    def start_requests(self, sesh=sesh, Leaver=Leaver, lvr=lvr):
        test_name = 'Michael Gefen'
        test_id = 10
        url = 'https://www.google.com/search?q=' + test_name + ' ' + 'site:www.linkedin.com'

        yield scrapy.Request(url=url, callback=self.parse, meta={'lid': test_id})

    def parse(self, response):

        #for i in response.xpath('//*[@id="ires"]/ol/div[@class="g"]'):
        for i in response.xpath('//*[@id="ires"]/ol/div[@class="g"]'):
        #for i in response.xpath('//*[@id="ires"]/ol/div[@class="g"]'):
            item = TrackItem()
            print('*********************************RESPONSE: ')
            print(i.extract())
            link_string = str(i.xpath('div/div[1]/cite').extract())
            print('link_string: ', link_string)
            stage_link = remove_html_markup(link_string).strip('[').strip(']').strip("\'")
            print('stage_link: ', stage_link)
            name_placeholder = i.xpath('h3/a/b/text()').extract()
            name_place = i.xpath('h3/a/text()').extract()
            print('length of HTML TEST: ', len(name_place))
            for k in name_place:
                print('pre-HTML content: ', k)
            np_test = remove_html_markup(name_place)
            print('HTML MarkUp Test: ', np_test)
            for j in name_placeholder:
                print('name_placeholder: ', j)
            item['name'] = name_placeholder[0].strip('[').strip(']')
            print("item['name']", item['name'])
            item['ident'] = response.meta['lid']
            if 'https://www.linkedin.com/pub/dir/' in stage_link or 'site:www.linkedin.com' in name_placeholder[0]:
                pass
            else:
                item['link'] = stage_link
                deet = i.xpath('div/div[2]/text()').extract()
                if len(deet) == 1:
                    deets = deet[0].replace(u'\xa0-\xa0', u'-')
                    deet_lst = deets.split('-')
                    print('deet_lst length: ', len(deet_lst))
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


                #xtrct = str(i.xpath('h3/a/@href').extract())
                #item['link'] = re.search('q=(.*)&(amp;)?sa', xtrct)
                #text = response.xpath('/a').extract()
                #item['details'] = re.sub('<[^<]+?>', '', text)
                #item['details'] = response.xpath('/a').extract()
                yield item
