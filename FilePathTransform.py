#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


def fix_include_paths(file_path: str) -> None:
    path = Path(file_path)

    if not path.is_file():
        print(f"[跳过] 文件不存在: {file_path}")
        return

    # 使用 bytes 处理，避免改变原文件编码
    data = path.read_bytes()

    # 匹配：
    # #include "xxx"
    # #include <xxx>
    pattern = re.compile(
        rb'(#\s*include\s*["<])([^">\r\n]+)([">])'
    )

    def replace(match):
        prefix = match.group(1)
        include_path = match.group(2)
        suffix = match.group(3)

        include_path = include_path.replace(b'\\', b'/')

        return prefix + include_path + suffix

    new_data, count = pattern.subn(replace, data)

    if new_data != data:
        path.write_bytes(new_data)
        print(f"[完成] {file_path}，修改 {count} 个 include")
    else:
        print(f"[无需修改] {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description='将 #include 路径中的 \\ 转换为 /'
    )
    parser.add_argument(
        'files',
        nargs='+',
        help='一个或多个需要修改的文件'
    )

    args = parser.parse_args()

    for file_path in args.files:
        fix_include_paths(file_path)


if __name__ == '__main__':
    main()