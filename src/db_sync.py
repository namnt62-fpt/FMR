import db
from sqlalchemy import Column, Integer, Numeric ,String, ForeignKey, func, update, text, UniqueConstraint
from sqlalchemy.sql.expression import and_, desc
import pandas as pd
from sqlalchemy.dialects.postgresql import insert


class codelist(db.Base):
    __tablename__ = "codelist"
    id = Column(Integer, primary_key=True)
    agency_codelist = Column(String)
    codelist_id = Column(String)
    codelist_name_vi = Column(String)
    codelist_name_en = Column(String)
    codelist_version = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

class codelist_detail(db.Base):
    __tablename__ = "codelist_detail"
    id = Column(Integer, primary_key=True)
    agency_codelist = Column(String)
    codelist_id = Column(String)
    codelist_version = Column(String)
    codelist_code = Column(String)
    code_name_vi = Column(String)
    code_name_en = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

class concept(db.Base):
    __tablename__ = "concept"
    id = Column(Integer, primary_key=True)
    agency_id = Column(String)
    concept_id = Column(String)
    concept_version = Column(String)
    concept_name = Column(String)
    description = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

class concept_representation(db.Base):
    __tablename__ = "concept_representation"
    id = Column(Integer, primary_key=True)
    agency_concept = Column(String)
    concept_id = Column(String)
    concept_version = Column(String)
    representation_id = Column(String)
    representation_name = Column(String)
    representation_type = Column(String)
    agency_codelist = Column(String)
    codelist_id = Column(String)
    codelist_version = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

class datastructure(db.Base):
    __tablename__ = "datastructure"
    id = Column(Integer, primary_key=True)
    agency_dsd = Column(String)
    dsd_id = Column(String)
    dsd_name = Column(String)
    version_dsd = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

class datastructure_detail(db.Base):
    __tablename__ = "datastructure_detail"
    id = Column(Integer, primary_key=True)
    agency_dsd = Column(String)
    dsd_id = Column(String)
    detail_type = Column(String)
    detail_id = Column(String)
    agency_codelist = Column(String)
    codelist_id = Column(String)
    codelist_version = Column(String)
    agency_concept = Column(String)
    concept_id = Column(String)
    concept_version = Column(String)
    concept_representation_id = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

class dataconstraint(db.Base):
    __tablename__ = "dataconstraint"
    id = Column(Integer, primary_key=True)
    agency_rc = Column(String)
    rc_id = Column(String)
    rc_name = Column(String)
    version_rc = Column(String)
    agency_df = Column(String)
    df_id = Column(String)
    version_df = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

class dataconstraint_detail(db.Base):
    __tablename__ = "dataconstraint_detail"
    id = Column(Integer, primary_key=True)
    agency_rc = Column(String)
    rc_id = Column(String)
    rc_name = Column(String)
    version_rc = Column(String)
    agency_df = Column(String)
    df_id = Column(String)
    version_df = Column(String)
    dimension_id = Column(String)
    included_values = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

class dataflow(db.Base):
    __tablename__ = "dataflow"
    id = Column(Integer, primary_key=True)
    agency_df = Column(String)
    df_id = Column(String)
    df_name = Column(String)
    version_df = Column(String)
    agency_dsd = Column(String)
    dsd_id = Column(String)
    version_dsd = Column(String)
    status = Column(Integer)
    __table_args__ = {'extend_existing': True}

db.Base.metadata.create_all(db.engine)

class _concept():

    def truncate_table():
        db.session.execute(text("TRUNCATE TABLE concept RESTART IDENTITY CASCADE"))
        db.session.commit()
        db.session.close()

    def ins_record(records):
        try:
            stmt = insert(concept).values(records)
            db.session.execute(stmt)
            db.session.commit()    
        except:
            db.session.rollback()
        finally:
            db.session.close()

class _concept_representation():

    def truncate_table():
        db.session.execute(text("TRUNCATE TABLE concept_representation RESTART IDENTITY CASCADE"))
        db.session.commit()
        db.session.close()

    def ins_record(records):
        try:
            stmt = insert(concept_representation).values(records)
            db.session.execute(stmt)
            db.session.commit()    
        except:
            db.session.rollback()
        finally:
            db.session.close()

class _datastructure():

    def truncate_table():
        db.session.execute(text("TRUNCATE TABLE datastructure RESTART IDENTITY CASCADE"))
        db.session.commit()
        db.session.close()

    def ins_record(records):
        try:
            stmt = insert(datastructure).values(records)
            db.session.execute(stmt)
            db.session.commit()    
        except:
            db.session.rollback()
        finally:
            db.session.close()

class _datastructure_detail():

    def truncate_table():
        db.session.execute(text("TRUNCATE TABLE datastructure_detail RESTART IDENTITY CASCADE"))
        db.session.commit()
        db.session.close()

    def ins_record(records):
        try:
            stmt = insert(datastructure_detail).values(records)
            db.session.execute(stmt)
            db.session.commit()    
        except:
            db.session.rollback()
        finally:
            db.session.close()
    

class _dataflow():

    def truncate_table():
        db.session.execute(text("TRUNCATE TABLE dataflow RESTART IDENTITY CASCADE"))
        db.session.commit()
        db.session.close()

    def ins_record(records):
        try:
            stmt = insert(dataflow).values(records)
            db.session.execute(stmt)
            db.session.commit()    
        except:
            db.session.rollback()
        finally:
            db.session.close()


class _codelist():

    def truncate_table():
        db.session.execute(text("TRUNCATE TABLE codelist RESTART IDENTITY CASCADE"))
        db.session.commit()
        db.session.close()

    def ins_record(records):
        try:
            stmt = insert(codelist).values(records)
            db.session.execute(stmt)
            db.session.commit()    
        except:
            db.session.rollback()
        finally:
            db.session.close()

class _codelist_detail():

    def truncate_table():
        db.session.execute(text("TRUNCATE TABLE codelist_detail RESTART IDENTITY CASCADE"))
        db.session.commit()
        db.session.close()

    def ins_record(records):
        try:
            stmt = insert(codelist_detail).values(records)
            db.session.execute(stmt)
            db.session.commit()    
        except:
            db.session.rollback()
        finally:
            db.session.close()

class _dataconstraint():
    def truncate_table():
        db.session.execute(text("TRUNCATE TABLE dataconstraint RESTART IDENTITY CASCADE"))
        db.session.commit()
        db.session.close()

    def ins_record(records):
        try:
            stmt = insert(dataconstraint).values(records)
            db.session.execute(stmt)
            db.session.commit()    
        except:
            db.session.rollback()
        finally:
            db.session.close()

class _dataconstraint_detail():
    def truncate_table():
        db.session.execute(text("TRUNCATE TABLE dataconstraint_detail RESTART IDENTITY CASCADE"))
        db.session.commit()
        db.session.close()

    def ins_record(records):
        try:
            stmt = insert(dataconstraint_detail).values(records)
            db.session.execute(stmt)
            db.session.commit()    
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
db.session.close()