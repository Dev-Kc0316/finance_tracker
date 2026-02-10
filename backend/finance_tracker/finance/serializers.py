from bson import ObjectId
import datetime

def serialize_doc(doc):
    new_doc = {}

    for k, v in doc.items():
        if isinstance(v, ObjectId):
            new_doc[k] = str(v)
        elif isinstance(v, datetime.datetime):
            new_doc[k] = v.isoformat()
        else:
            new_doc[k] = v
    return new_doc

def serialize_list(docs):
    return [serialize_doc(doc) for doc in docs]