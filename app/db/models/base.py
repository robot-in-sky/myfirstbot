from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()
'''
Don't use as field names:
    - ident
    - skip
    - limit
    - order_by
'''

