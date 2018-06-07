from suspect_scrape_app import settings
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from helpers import load_tables

#processes spider items into postgres db
class SuspectPipeline(object):
    def process_item(self, item, spider):
        #getting sqlalchemy session from spider
        sesh = spider.sesh
        if item['link'] in spider.link_list:
            #ID duplicate
            pass
        else:
            print('New Suspect Found')
            suspect = spider.Suspect()
            suspect.name=item['name']
            suspect.leaverid=item['ident']
            suspect.role=item['role']
            suspect.include='Yes'
            suspect.firm=item['firm']
            suspect.location=item['location']
            suspect.link=item['link']
            lvr = sesh.query(spider.Leaver).filter_by(id=item['ident']).one()
            lvr.updated='Yes'
            print('changing updated status for: ', lvr.name)

            try:
                print('Updating DB...')
                sesh.add(suspect)
                sesh.commit()
            except IntegrityError:
                print('DB Integrity Error....', item['name'])
        return item
