"""
统一C++程序#include中路径分隔符,将\或\\转换为/
"""
#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

# 需要处理的文件类型
SOURCE_EXTENSIONS = {
    ".c", ".cpp", ".cc", ".cxx",
    ".h", ".hpp", ".hh"
}

# 匹配 #include "xxx" 和 #include <xxx>
INCLUDE_PATTERN = re.compile(
    rb'(^[ \t]*#[ \t]*include[ \t]*["<])([^">\r\n]+)([">])',
    re.MULTILINE
)


def fix_include_paths(path: Path) -> int:
    """修改单个文件中的 include 路径，返回修改数量。"""

    try:
        data = path.read_bytes()

        def replace(match):
            prefix = match.group(1)
            include_path = match.group(2)
            suffix = match.group(3)

            new_path = include_path.replace(b'\\', b'/')

            return prefix + new_path + suffix

        new_data, _ = INCLUDE_PATTERN.subn(replace, data)

        if new_data != data:
            # 统计实际发生路径变化的 include 数量
            count = sum(
                1
                for m in INCLUDE_PATTERN.finditer(data)
                if b'\\' in m.group(2)
            )

            path.write_bytes(new_data)

            print(f"[完成] {path}，修改 {count} 个 include")
            return count

        return 0

    except Exception as e:
        print(f"[错误] {path}: {e}")
        return 0


def process_path(target: Path):
    """递归处理目录或单个文件。"""

    file_count = 0
    include_count = 0

    if target.is_file():
        files = [target]

    elif target.is_dir():
        files = (
            p for p in target.rglob("*")
            if p.is_file()
            and p.suffix.lower() in SOURCE_EXTENSIONS
        )

    else:
        print(f"[跳过] 路径不存在: {target}")
        return 0, 0

    for file_path in files:
        if file_path.suffix.lower() not in SOURCE_EXTENSIONS:
            continue

        count = fix_include_paths(file_path)

        if count > 0:
            file_count += 1
            include_count += count

    return file_count, include_count


def main():
    parser = argparse.ArgumentParser(
        description="递归修复 C/C++ 文件中的 #include 路径"
    )

    parser.add_argument(
        "paths",
        nargs="+",
        help="需要处理的文件或目录，支持多个路径"
    )

    args = parser.parse_args()

    total_files = 0
    total_includes = 0

    for path_str in args.paths:
        target = Path(path_str)

        print(f"\n[扫描] {target}")

        files, includes = process_path(target)

        total_files += files
        total_includes += includes

    print("\n========== 处理完成 ==========")
    print(f"修改文件数量: {total_files}")
    print(f"修改 include 数量: {total_includes}")
    print("================================")


if __name__ == "__main__":
    main()
