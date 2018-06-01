from suspect_scrape_app import settings
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
#from helpers import Suspect, Leaver
from helpers import load_tables


class SuspectPipeline(object):
    # def __init__(self):
    #     sesh = load_suspects()
    def process_item(self, item, spider):
        #sesh = load_suspects()
        sesh = spider.sesh
        #suspect = Suspect(name=item['name'], leaverid=item['ident'], role=item['role'], include='Yes', firm=item['firm'], location=item['location'], link=item['link'])
        print("ITEM'S ROLE VALUE: ", item['role'])
        if item['link'] in spider.link_list:
            print('duplicate', item['name'])
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
                print('trying...')
                sesh.add(suspect)
                sesh.commit()
            except IntegrityError:
                print('except....', item['name'])
        return item

    # def close_spider(self, spider):
    #     spider.sesh.commit()
