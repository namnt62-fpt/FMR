import db
from sqlalchemy import Column, Integer, Numeric ,String, ForeignKey, func, update, text, UniqueConstraint
from sqlalchemy.sql.expression import and_, desc
import pandas as pd
from sqlalchemy.dialects.postgresql import insert


class codelist_item_used(db.Base):
    __tablename__ = "codelist_item_used"
    id = Column(Integer, primary_key=True)
    cs_id = Column(String)
    agency_id = Column(String)
    codelist_id = Column(String)
    ver_codelist = Column(String)
    item_codelist_used = Column(String)
    status = Column(Integer)
    __table_args__ = (
        UniqueConstraint('agency_id', 'codelist_id', 'ver_codelist', 'item_codelist_used', name='uq_codelist_item'),
        {'extend_existing': True}
    )

db.Base.metadata.create_all(db.engine)

class _codelist_item_used():
    def __init__(self, cs_id = None, agency_id = None, codelist_id = None, ver_codelist = None, item_codelist_used = None, status = 1):
        self.cs_id = cs_id
        self.agency_id = agency_id
        self.codelist_id = codelist_id
        self.ver_codelist = ver_codelist
        self.item_codelist_used = item_codelist_used
        self.status = status
    def ins_record(records):
        try:
            stmt = insert(codelist_item_used).values(records)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=['agency_id', 'codelist_id', 'ver_codelist', 'item_codelist_used']
            )
            db.session.execute(stmt)
            db.session.commit()    
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
db.session.close()