"""
将字节码解码为文本
"""

"""
UTF8编码解码为文本
"""
s = r'\344\270\200\346\254\241'

result = bytes(
    int(x, 8) for x in s.split('\\') if x
).decode('utf-8')

print(result)