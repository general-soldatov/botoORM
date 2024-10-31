from app.models.db_model import DBModel, KeySchema, Key, Filter
from app.db_manager import DynamodbManage, ProvisionedThroughput
from app.s3_manager import S3Manager

class Table(DBModel):
    name: str
    user_id: int
    create: float

key_schema = KeySchema(HASH='name', RANGE='user_id')
data = Table(name='Eli', user_id=249, create=20.07)
prov = ProvisionedThroughput(ReadCapacityUnits=1, WriteCapacityUnits=1)

db = DynamodbManage(table_name='Table_test')
s3 = S3Manager(bucket_name='serverless-shortener')
# tests to dynamodb
# response = db.create_table(key_schema, attribute=Table, provisioned_throughput=prov)
# response = db.put_item(data)
# response = db.get_item(key_schema('Yur', 238))
# response = db.scan(need_args=['name', 'cheate'])
# response = db.scan(filters=Filter('user_id').ge(237))
# response = db.update_item(key_schema('Yur', 238), args={'create': 123, 'toper': '23'})

# tests to s3 bucket
# response = s3.create_bucket()
# response = s3.put_object('TEST', name_file='test.txt')
# response = s3.upload_file(file_path='app/s3_manager.py', name_file='manager.py')
# response = s3.delete_objects(['manager.py', 'test.txt'])
# response = s3.list_objects()
response = s3.get_str_object('index.html')

print(response)
# print(db._check_arg_models(key_schema('Yur', 238)))
# print(response['Items'])
# print(key_schema.query(HASH_VALUE=['Eli', 'Yur']))
