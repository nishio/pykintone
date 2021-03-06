# pykintone

Python library to access [kintone](https://kintone.cybozu.com).

```python
import pykintone

r = pykintone.app("kintone domain", "app id", "api token").select("updated_time > NOW()")
if r.ok:
    records = r.records
```

## Feature

**Basic operation**

* create
* read
* update
* delete

**Record and model mapping**

```python
import pykintone
from pykintone import model


class Person(model.kintoneModel):

    def __init__(self):
        super(Person, self).__init__()
        self.last_name = ""
        self.first_name = ""


app = pykintone.load("path_to_account_setting").app()
persons = app.select().models(Person)

someone = persons[0]
someone.last_name = "xxx"
app.update(someone)

```

## Installation

You can download from [pypi](https://pypi.python.org/pypi/pykintone).

```
pip install pykintone
```

`pykintone` works on Python3, and it depends on below libraries.

* [PyYAML](http://pyyaml.org/wiki/PyYAML)
* [requests](http://docs.python-requests.org/en/latest/)
* ([enum34](https://pypi.python.org/pypi/enum34)) for Python2

You can write account setting file as below (yaml format).

```
domain: xxx
login:
    id: user_id
    password: password
basic:
    id: basic_id
    password: password
apps:
    test:
        id: 1
```

Of course you can use api_token. 

```
domain: xxx
apps:
    test:
        id: 1
        api_token: xxxx
```

## Test

You have to create test application on kintone, and you can use `tests/pykintoneTest.zip` (application template) to do it.
