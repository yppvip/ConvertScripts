"""
将文本编码为字节
"""

"""
文本 编码为 UTF8编码(十六进制)
"""
text = "线路保护"
prefix = "\\x"  # 可以替换成 "%", "0x", " " 等

encoded = ''.join(f'{prefix}{b:02x}' for b in text.encode('utf-8'))

print(encoded)