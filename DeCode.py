"""
将字节码解码为文本
"""

"""
UTF8编码解码为文本
"""
s = r'\xe5\xbc\x80\xe5\x85\xa5\xe9\x87\x8f\xe8\xbf\x94\xe5\x9b\x9e\xe6\x97\xb6\xe9\x97\xb4'

result = bytes(
    int(x, 16) for x in s.split('\\x') if x
).decode('utf-8')

print(result)