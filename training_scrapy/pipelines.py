# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Quote(Base):
    __tablename__ = 'quote'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    author = Column(String(200))
    tags = Column(String(400))


class QuotesToDBPipeline:

    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        quote = Quote(
            text=item['text'],
            author=item['author'],
            tags=', '.join(item['tags']),
        )
        self.session.add(quote)
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
