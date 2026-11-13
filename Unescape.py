"""
将包含 JSON 转义字符的文本或C类型字符的转义文本，还原成正常可阅读的文本，并将转换结果保存到 output.txt 文件中。
示例：
"Hello\nWorld\t123"
转换为
Hello
World	123
使用示例:
python Unescape.py input.txt
"""
import json
import sys


def json_value_to_text(value: str) -> str:
    """
    将 JSON/程序形式的字符串转换成人可读文本。

    例如：
        "hello\\nworld\\t123"
    转换为：
        hello
        world   123
    """

    value = value.strip()

    # 如果输入本身已经带 JSON 双引号，直接解析
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)

    # 如果只复制了字符串内容，没有外层双引号
    return json.loads('"' + value + '"')


def convert_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        encoded_text = f.read()

    readable_text = json_value_to_text(encoded_text)

    print("===== 转换结果 =====")
    print(readable_text)

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(readable_text)

    print("\n已生成 output.txt")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python decode.py input.txt")
        sys.exit(1)

    convert_file(sys.argv[1])