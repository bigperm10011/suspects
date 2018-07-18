import scrapy
import re
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.engine.url import URL
import sqlalchemy
from suspect_scrape_app import settings
from sqlalchemy.orm import mapper, sessionmaker
from suspect_scrape_app.items import TrackItem
from helpers import load_tables, remove_html_markup, clean_string, score_name, find_city, list2string, zone1, zone2, zone3a
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
        print('number of names to be scraped:', len(lvr))
        if len(lvr) > 0:
            for l in lvr:
                print('Leaver Selected: ', l.name)
                lid = l.id
                string = str('https://www.google.com/search?q=' + l.name + ' ' + 'site:www.linkedin.com/in/' + ' ' + 'language:en')
                url = string

                yield scrapy.Request(url=url, callback=self.parse, meta={'lid': l.id, 'name': l.name})
        else:
            raise CloseSpider('All Leavers Have Suspects')
    def parse(self, response):
        db_name = response.meta['name']
        for i in response.xpath("//div[contains(@class, 'g')]"):
            print('**** G CLASS ****', i)
            raw_lnk = str(i.xpath(".//cite").extract())
            clink = zone2(raw_lnk)
            print('Testing New Zone2: ', clink)
            if 'https://www.linkedin.com/in/' in clink:
                h3a = i.xpath(".//h3/a").extract()
                name, role1, firm1 = zone1(h3a)
                slp_xtract = i.xpath(".//div[contains(@class, 'slp')]/descendant::text()").extract()
                print('Raw SLP Xtract: ', slp_xtract)
                print('LENGTH of SLP Xtract: ', len(slp_xtract))

                if len(slp_xtract) > 0:
                    txt = str(slp_xtract)
                    print('length of slp: ', len(txt))
                    print('slp class detected. Running Zone3a Analysis...')
                    city, role, firm = zone3a(txt)
                    print('results from zone3a analysis: ')
                    item = TrackItem()
                    item['name'] = name
                    item['link'] = clink
                    item['ident'] = response.meta['lid']
                    item['location'] = city
                    if role1 == None:
                        item['role'] = role
                    else:
                        item['role'] = role1
                    if firm1 == None:
                        item['firm'] = firm
                    else:
                        item['firm'] = firm1
                    score = score_name(item['name'], db_name)
                    if score > 80:
                        item['status'] = 'Success'
                        yield item
                    else:
                        yield None

                else:
                    print('no slp class found.  salvaging text')
                    st_class = i.xpath(".//span[contains(@class, 'st')]/descendant::text()").extract()
                    print('ST Text Extracted: ', st_class)
                    salvage_string = list2string(st_class)
                    print('st class converted to string: ', salvage_string)
                    cleaned_str = clean_string(salvage_string, name)
                    print('st string filtered: ', cleaned_str)
                    item = TrackItem()
                    item['name'] = name
                    item['link'] = clink
                    item['location'] = None
                    item['ident'] = response.meta['lid']
                    if role1 == None:
                        item['role'] = None
                    else:
                        item['role'] = role1
                    if firm1 == None:
                        item['firm'] = cleaned_str.strip()
                    else:
                        item['firm'] = firm1
                    score = score_name(item['name'], db_name)
                    if score > 80:
                        item['status'] = 'Success'
                        yield item
                    else:
                        yield None




        # try:
        #     for i in response.xpath('//*[@id="ires"]/ol/div[@class="g"]'):
        #         item = TrackItem()
        #         link_string = str(i.xpath('div/div[1]/cite').extract())
        #         stage_link = remove_html_markup(link_string).strip('[').strip(']').strip("\'")
        #         name_placeholder = i.xpath('h3/a/b/text()').extract()
        #         item['name'] = name_placeholder[0].strip('[').strip(']')
        #         item['ident'] = response.meta['lid']
        #         if 'https://www.linkedin.com/pub/' in stage_link or 'site:www.linkedin.com' in name_placeholder[0]:
        #             print('excluding bad result:', stage_link)
        #             pass
        #         elif 'https://www.linkedin.com/in/' in stage_link:
        #             item['link'] = stage_link
        #             deet = i.xpath('div/div[2]/text()').extract()
        #             print('deet value:', deet)
        #             if len(deet) == 1:
        #                 deets = deet[0].replace(u'\xa0-\xa0', u'-')
        #                 deet_lst = deets.split('-')
        #                 print('DEET  LIST VALUE: ', deet_lst[1])
        #                 #print('!!!!!!!!!!', len(deet_lst))
        #                 if len(deet_lst) == 3:
        #                     try:
        #                         item['location'] = deet_lst[0]
        #                     except:
        #                         item['location'] = None
        #                     try:
        #                         item['role'] = deet_lst[1]
        #                     except:
        #                         item['role'] = None
        #                     try:
        #                         item['firm'] = deet_lst[2]
        #                     except:
        #                         item['firm'] = None
        #                 else:
        #                     item['location'] = None
        #                     item['role'] = None
        #                     item['firm'] = None
        #             item['status'] = 'Success'
        #             yield item
        #         else:
        #             yield None
        # except:
        #     item = TrackItem()
        #     item['status'] = 'Fail'
        #     yield item
