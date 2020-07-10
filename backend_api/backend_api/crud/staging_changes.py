from sqlalchemy.orm import Session
import sqlalchemy.exc
import backend_api.exc


def id_exists(db: Session, table: str, id: int):
    pass

    # table = declarative_base().metadata.tables[table]
    # if db.query(table).filter(table.id == id).all() == None:
    #     return False
    # return True
