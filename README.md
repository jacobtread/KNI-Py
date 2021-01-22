# KAMAR Notices Interface 
Python Edition

KNI (KAMAR Notices Interface) is a project designed to bring a way of accessing notices from
the [KAMAR](https://kamar.nz) portal software. KNIs goal is to produce usable libraries in as many
languages as possible

[![Supported Versions](https://img.shields.io/pypi/pyversions/knij.svg)](https://pypi.org/project/requests)

KNI is available on PyPI:

```console
$ python -m pip install knij
```


### Retrieving Notices
```python
from kni import KNI

kni = KNI('demo.school.kiwi')
notices = kni.retrieve()
for notice in notices.notices:
    print(notice)
```
Specifying a custom date
```python
# Use leading zeros on single digits (e.g 01/01/2021)
notices = kni.retrieve('DAY/MONTH/YEAR')
```

By Jacobtread