"""
File: forLatticeUse.py
Desc:
    为使用 lattice lstm 模型进行数据输入的预处理工作
"""
import settings
import os
import json
import re
from module.ColorLogDecorator import ColorLogDecorator


def main():
    ColorLogDecorator.active()

    r_rm = re.compile("|".join(settings.MARKS_RM))
    r_seg = re.compile("|".join(settings.MARKS_SEG))

    output_path = os.path.join(settings.OUTPUT_DIR, 'forLattice')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    top_dir = settings.INPUT_DIR1
    for dynasty in os.listdir(top_dir):  # 朝代
        dynasty_path = os.path.join(top_dir, dynasty)
        if os.path.isdir(dynasty_path):
            for author in os.listdir(dynasty_path):
                print(ColorLogDecorator.yellow("Handle: " + dynasty + " " + author))

                author_path = os.path.join(dynasty_path, author)
                data: dict = {}
                with open(author_path, 'r', encoding='utf-8', errors='ignore') as f:
                    data = json.load(f)

                output_str: str = ""
                for item in data["poems"]:
                    raw = "".join(item["title"].split(" ")) + "，" + "".join(item["content"].split(" "))
                    raw = list("\n".join(r_seg.split("".join(r_rm.split(raw)))))
                    for c in raw:
                        if c != "\n":
                            output_str = output_str + c + " O\n"
                        else:
                            output_str += c

                output_file = os.path.join(output_path, dynasty + "_" + os.path.splitext(author)[0] + ".txt")
                with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(output_str)
    print(ColorLogDecorator.green("DONE"))


if __name__ == '__main__':
    main()
