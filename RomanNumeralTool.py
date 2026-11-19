"""
1.罗马数字检测
2.罗马数字转换
在main中修改需要结果
"""

import re
import unicodedata


# Unicode 罗马数字映射表
# 使用真正的 Unicode 罗马数字字符，而不是 ASCII 字母组合
ROMAN_MAP = {
    1: "Ⅰ",
    2: "Ⅱ",
    3: "Ⅲ",
    4: "Ⅳ",
    5: "Ⅴ",
    6: "Ⅵ",
    7: "Ⅶ",
    8: "Ⅷ",
    9: "Ⅸ",
    10: "Ⅹ",
    11: "Ⅺ",
    12: "Ⅻ",
    50: "Ⅼ",
    100: "Ⅽ",
    500: "Ⅾ",
    1000: "Ⅿ"
}


def find_roman_numbers(text):
    """
    检测文本中是否包含 Unicode 罗马数字字符。

    参数：
        text: 待检测文本

    返回：
        list: 罗马数字字符及其位置、Unicode 编码
    """

    results = []

    for index, char in enumerate(text):

        # Unicode 罗马数字字符范围：U+2160 ~ U+2188
        if "\u2160" <= char <= "\u2188":

            results.append({
                "character": char,
                "position": index,
                "unicode": f"U+{ord(char):04X}",
                "name": unicodedata.name(char, "UNKNOWN")
            })

    return results


def arabic_to_roman(number):
    """
    将阿拉伯数字转换为 Unicode 罗马数字。

    支持范围：
        1~12、50、100、500、1000

    注意：
        其他数字采用标准罗马数字的组合规则，
        但输出仍然使用 Unicode 罗马数字字符。
    """

    if not isinstance(number, int) or isinstance(number, bool):
        raise ValueError("输入必须是整数！")

    if not 1 <= number <= 3999:
        raise ValueError("转换范围为 1~3999！")

    # 标准罗马数字组合表，输出全部使用 Unicode 字符
    mapping = [
        (1000, "Ⅿ"),
        (900, "ⅭⅯ"),
        (500, "Ⅾ"),
        (400, "ⅭⅮ"),
        (100, "Ⅽ"),
        (90, "ⅩⅭ"),
        (50, "Ⅼ"),
        (40, "ⅩⅬ"),
        (10, "Ⅹ"),
        (9, "Ⅸ"),
        (5, "Ⅴ"),
        (4, "Ⅳ"),
        (1, "Ⅰ")
    ]

    result = ""

    for value, symbol in mapping:
        count, number = divmod(number, value)
        result += symbol * count

    return result


def convert_text_numbers(text):
    """
    将文本中的阿拉伯整数转换为 Unicode 罗马数字。

    只转换 1~3999 的整数。
    """

    pattern = re.compile(r"(?<![\d.])\d+(?![\d.])")

    def replace_number(match):
        number = int(match.group())

        if 1 <= number <= 3999:
            return arabic_to_roman(number)

        return match.group()

    return pattern.sub(replace_number, text)


# ============================
# 主程序测试
# ============================

if __name__ == "__main__":

    text = "反时限Ⅰ段,反时限II段"

    print("原始文本：")
    print(text)

    # 1. 检测 Unicode 罗马数字
    print("\n罗马数字检测结果：")

    results = find_roman_numbers(text)

    if results:
        for item in results:
            print(
                f"字符：{item['character']}，"
                f"位置：{item['position']}，"
                f"编码：{item['unicode']}，"
                f"名称：{item['name']}"
            )
    else:
        print("未检测到 Unicode 罗马数字。")

    # 2. 阿拉伯数字转换
    print("\n数字转换结果：")

    converted = convert_text_numbers(text)

    print(converted)

    # 3. 单个数字转换
    print("\n单个数字转换：")

    for number in [1, 2, 3, 4, 5, 6]:
        print(f"{number} -> {arabic_to_roman(number)}")
