import hashlib
import re

REGEXES = {
    "url": "https?:\/\/(?:www\.)?([-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b)*(\/[\/\d\w\.-]*)*(?:[\?])*(.+)*",
    "username": "^([A-Z]|[a-z]|[0-9]|-|_){1,}$"
}

def validate(data, type):
    if type == "url":
        return re.match(REGEXES["url"], data)
    elif type == "username":
        return re.match(REGEXES["username"], data)


def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()
