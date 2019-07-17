import os
import peewee as pw
import datetime
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(os.getenv('DATABASE'))

class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default = datetime.datetime.now)
    updated_at = pw.DateTimeField(default = datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
    
    class Meta:
        database = db
        legacy_table_names = False

class Store(BaseModel):
    name = pw.CharField(unique=True)

class Warehouse(BaseModel):
    store= pw.ForeignKeyField(Store, backref = 'warehouses', unique = True)
    location=pw.TextField()

class Product(BaseModel):
    name = pw.CharField(index = True) #add database indexing ie. create a separate table that only the dbms can see that has the entries in a column sorted numerically / alphabetically with an index . Then we can track down entries using binary search / some more efficient algo.
    description = pw.TextField()
    warehouse = pw.ForeignKeyField(Warehouse, backref='products')
    color = pw.CharField(null=True)
