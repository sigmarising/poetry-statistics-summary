"""
File: character_summary.py
Desc:
    脚本 - 用于统计字频
    只统计所有诗词的正文部分内容
"""
import settings
import os
import re
import json
from collections import Counter
from module.ColorLogDecorator import ColorLogDecorator


def main():
    ColorLogDecorator.active()

    # 数据结构
    print(ColorLogDecorator.green("Step1. 创建数据结构"))
    dynasty_str: dict = {
        "元": "",
        "先秦": "",
        "南北朝": "",
        "唐": "",
        "宋": "",
        "明": "",
        "汉": "",
        "清": "",
        "辽": "",
        "金": "",
        "隋": "",
        "魏晋": ""
    }
    sum_counter = Counter()
    dynasty_counter: dict = {
        "元": Counter(),
        "先秦": Counter(),
        "南北朝": Counter(),
        "唐": Counter(),
        "宋": Counter(),
        "明": Counter(),
        "汉": Counter(),
        "清": Counter(),
        "辽": Counter(),
        "金": Counter(),
        "隋": Counter(),
        "魏晋": Counter()
    }
    top_dir = settings.INPUT_DIR1
    r_marks = re.compile("|".join(settings.MARKS))
    r_classical = re.compile("|".join(settings.CLASSICAL))
    print(ColorLogDecorator.green("Step1. DONE"))

    # 获取所有诗词正文 并去掉标点符号
    print(ColorLogDecorator.green("Step2. 读取数据集"))
    for dynasty in os.listdir(top_dir):  # 朝代
        dynasty_path = os.path.join(top_dir, dynasty)
        if os.path.isdir(dynasty_path):
            for author in os.listdir(dynasty_path):  # 作者
                author_path = os.path.join(dynasty_path, author)
                with open(author_path, 'r', encoding='utf-8', errors='ignore') as f:  # 文件
                    print(ColorLogDecorator.yellow("  Handling:" + dynasty + author))
                    data: dict = json.load(f)
                    for item in data["poems"]:
                        raw_str = item["content"]
                        if raw_str:
                            dynasty_str[dynasty] += "".join(r_classical.split("".join(r_marks.split(raw_str))))
    print(ColorLogDecorator.green("Step2. DONE"))

    # 统计信息
    print(ColorLogDecorator.green("Step3. 进行统计"))
    for k, v in dynasty_str.items():
        dynasty_counter[k].update(v)
        sum_counter.update(dynasty_counter[k])
    print(ColorLogDecorator.green("Step3. DONE"))

    # 输出统计
    print(ColorLogDecorator.green("Step4. 输出信息"))
    output_path = os.path.join(settings.OUTPUT_DIR, 'character_summary')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for k, v in dynasty_counter.items():  # 统计每个朝代 top N 常用字
        output = {}
        print(ColorLogDecorator.yellow("  Handling: " + k))
        for item in v.most_common(settings.TOP_N):
            output[item[0]] = {}
            for k1, v1 in dynasty_counter.items():  # 对每个朝代的 top N 常用字 统计其在各个朝代的常用频率
                output[item[0]][k1] = v1[item[0]] / len(dynasty_str[k1])
        file_path = os.path.join(output_path, k + ".json")
        with open(file_path, "w+", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
    output = {}
    sum_len = 0
    for k, v in dynasty_str.items():
        sum_len += len(v)
    print(ColorLogDecorator.yellow("  Handling: Summary"))
    for item in sum_counter.most_common(settings.TOP_N):
        output[item[0]] = {"汇总": item[1] / sum_len}
        for k, v in dynasty_counter.items():
            output[item[0]][k] = v[item[0]] / len(dynasty_str[k])
    with open(os.path.join(output_path, "汇总.json"), "w+", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(ColorLogDecorator.green("Step4. DONE"))


if __name__ == '__main__':
    main()
