import hashlib

def MD5(pwd):
    hash = hashlib.md5()
    hash.update(pwd.encode("utf-8"))
    return hash.hexdigest()

# print(type(str(MD5("123"))))
