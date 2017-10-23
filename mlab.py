import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds151004.mlab.com:51004/cuagaidaicuong
host = "ds151004.mlab.com"
port = 51004
db_name = "cuagaidaicuong"
user_name = "kouu195"
password = "259952az"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)


def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())
