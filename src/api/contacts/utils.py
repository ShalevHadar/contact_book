import uuid

def phn():
    return str(uuid.uuid4().int)[:10]