from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional, Any, Dict, Union

PARAMS = {
            int: 'N',
            float: 'N',
            str: 'S',
            bool: 'BOOL',
            None: 'NULL',
            list: 'L',
            tuple: 'L',
            dict: 'M',
            bytes: 'B'
        }

PARAMS_REVERSE = {
    'N': lambda x: float(x) if '.' in x else int(x),
    'S': str,
    'BOOL': bool,
    'NULL': None,
    'L': list,
    'M': dict,
    'B': bytes
}

def _params_convert(arg: type, value: Any = None):
    def convert(arg: type):
        if arg not in PARAMS:
            return PARAMS[str]
        return PARAMS[arg]

    condition = lambda x: type(x) not in [str, int, float, bytes]
    if value:
        return {convert(arg): value if condition(value) else str(value)}
    return convert(arg)

def _dump_dict(data: Dict[str, Dict[str, str]]):
    result = {}
    for key, values in data.items():
        types, value = tuple(values.items())[0]
        result[key] = PARAMS_REVERSE[types](value)

    return result

class DBModel(BaseModel):
    def dump_dynamodb(self):
        return {key: _params_convert(self.__annotations__[key], value)
                for key, value in self.model_dump().items()}

    @classmethod
    def dump_schema_db(cls):
        return {key: _params_convert(value) for key, value in
                            cls.__annotations__.items()}


@dataclass
class KeySchema:
    HASH: str
    RANGE: Optional[str] = None

    def __call__(self, HASH_VALUE: Union[str, int, None] = None, RANGE_VALUE: Union[str, int, None] = None):
        """Функция для запроса get_item по значениям HASH и RANGE.
        """
        data = {}
        if RANGE_VALUE:
            data[self.RANGE] = RANGE_VALUE
        if HASH_VALUE:
            data[self.HASH] = HASH_VALUE
        if data:
            return data
        assert KeyError('Not arguments to query')



class Key:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def operator(key, value, operator):
        data = {'ComparisonOperator': operator}
        if value:
            data['AttributeValueList'] = [_params_convert(type(item), item)
                                            for item in value]
        return {key: data}

    def eq(self, value: list):
        """Операция эквивалентности
        """
        return self.operator(self.name, value, operator='EQ')

    def ne(self, value: list):
        """Операция отрицания
        """
        return self.operator(self.name, value, operator='NE')

    def begins_with(self, value: list):
        """Операция поиска строки, начинайщийся с value
        """
        return self.operator(self.name, value, operator='BEGINS_WITH')

    def le(self, value: list):
        """Операция меньше или равно
        """
        return self.operator(self.name, value, operator='LE')

    def lt(self, value: list):
        """Операция меньше
        """
        return self.operator(self.name, value, operator='LT')

    def ge(self, value: list):
        """Операция больше или равно
        """
        return self.operator(self.name, value, operator='GE')

    def gt(self, value: list):
        """Операция больше
        """
        return self.operator(self.name, value, operator='GT')

    def between(self, value: list):
        """Операция между
        """
        return self.operator(self.name, value, operator='BETWEEN')
