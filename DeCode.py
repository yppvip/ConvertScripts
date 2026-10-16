"""
将字节码解码为文本
"""

"""
UTF8编码(十六进制) 解码为文本
"""
s = r'\xe7\xba\xbf\xe8\xb7\xaf\xe4\xbf\x9d\xe6\x8a\xa4'

result = bytes(
    int(x, 16) for x in s.replace(r'\x', ' ').split()
).decode('utf-8')

print(result)