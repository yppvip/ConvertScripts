"""
将人阅读的字符串转换为计算机字符串
"""
import json
import sys


def script_to_json_value(script: str) -> str:
    """把多行脚本转换成可直接作为 JSON value 的字符串。"""
    return json.dumps(script, ensure_ascii=False)


def convert_file(file_path: str):
    # Windows bat 一般可先尝试 UTF-8；如果你的文件是 GBK，可改成 encoding="gbk"
    with open(file_path, "r", encoding="utf-8") as f:
        script = f.read()

    json_value = script_to_json_value(script)

    print(json_value)

    # 同时生成一个完整 JSON 示例
    result = {
        "script": script
    }

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n已生成 output.json")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python convert.py xxx.bat")
        sys.exit(1)

    convert_file(sys.argv[1])