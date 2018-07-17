Airbloc Data Producer Node
================

Data producer module for ingesting and registering data.  

### Setup
Requires Python 3.6 or above.

```
pip install -r requirements.txt
```


## Development Guide

### Compile Protobuf

Running `generate_proto.py` will compile Protobuf codes in `protos/` and
will generate stubs and services into `airbloc/proto`.

```
$ python generate_proto.py
Codes are generated into airbloc/proto.
```
