from app.models.db_model import DBModel, KeySchema, Key, Filter
from app.db_manager import DynamodbManage, ProvisionedThroughput

class Table(DBModel):
    name: str
    user_id: int
    create: float

key_schema = KeySchema(HASH='name', RANGE='user_id')
data = Table(name='Eli', user_id=249, create=20.07)
prov = ProvisionedThroughput(ReadCapacityUnits=1, WriteCapacityUnits=1)

db = DynamodbManage(resource_name='Table_test')
# response = db.create_table(key_schema, attribute=Table, provisioned_throughput=prov)
# response = db.put_item(data)
# response = db.get_item(key_schema('Yur', 238), need_args=['create', 'name'])
# response = db.scan(need_args=['name', 'cheate'])
response = db.scan(filters=Filter('user_id').ge(237))

print(response)
# print(db._check_arg_models(key_schema('Yur', 238)))
# print(response['Items'])
# print(key_schema.query(HASH_VALUE=['Eli', 'Yur']))
