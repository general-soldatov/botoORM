# dynamodb_manager
Библиотека для управления сервисами YandexCloud в serverless режиме на основе библиотеки `botocore` и `pydantic`.

# Создание таблицы

Для создания таблицы нужно определить ключевую схему с помощью класса `KeySchema`. Импортируем и объявим его экземпляр.

```python
from app.models.db_model import KeySchema

key_schema = KeySchema(HASH='name', RANGE='user_id')

```
Также определим схему таблицы с помощью класса на базе модели `DBModel`. Имена ключей, объявленные в ключевой схеме, должны присутствовать в классе модели.

```python
from app.models.db_model import DBModel

class Table(DBModel):
    name: str
    user_id: int
    create: float

```
Для ограничения пропускной способности, воспользуйтесь экземпляром класса `ProvisionedThroughput`.

```python
from app.db_manager import ProvisionedThroughput
prov = ProvisionedThroughput(ReadCapacityUnits=1, WriteCapacityUnits=1)
```

Для работы с сервисами AWS необходимо использование переменных окружения в файле `.env`:
```env
ENDPOINT ='example'
AWS_DEFAULT_REGION = 'ru-central1'
AWS_ACCESS_KEY_ID='example'
AWS_SECRET_ACCESS_KEY='example'
```

Либо создать свой конфиг на базе экземпляров классов `AWSConfig` и `AWSSession`.

```python
from app.models.config import AWSConfig, AWSSession

session = AWSSession(access_key: str = 'example', secret_key: str = 'example')
config = AWSConfig(service_name: str = 'example', endpoint_url: str = 'example', region_name: str = 'example')
```

Создать таблицу можно с помощью метода `create_table` экземпляра класса `DynamodbManage`

```python
from app.db_manager import DynamodbManage

db = DynamodbManage(resource_name='Table_test')
db.create_table(key_schema, attribute=Table, provisioned_throughput=prov)
```
Экземпляр класса `DynamodbManage` имеет следующие аргументы:
```python
resource_name: str # название таблицы
config: Union[AWSConfig, dict] # конфигурация ресурсного клиента:
    service_name: Any['dynamodb', 's3'],
    endpoint_url: str
    region_name: str
session_aws: Union[AWSSession, dict] # конфигурация сессии botocore:
    access_key: str
    secret_key: str
```

Добавить элемент в таблицу можно с помощью команды:
```python
from app.models.db_model import DBModel

class Table(DBModel):
    name: str
    user_id: int
    create: float

data = Table(name='Name', user_id=238, create=19.97)
db = DynamodbManage(resource_name='Table_test')
db.put_item(data)
```
