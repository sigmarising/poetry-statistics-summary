"""
File: multi_summary.py
Desc:
    脚本 - 用于统计诗文中的常见意象
"""
import settings
import os
import json
from module.ColorLogDecorator import ColorLogDecorator

summary_season = {}  # 季节统计
summary_solar_term = {}  # 节气统计
summary_imagery = {}  # 意象统计
summary_color = {}  # 颜色统计


def __init_ds():
    # 季节统计
    for item in settings.DYNASTY:
        summary_season[item] = {}
    for v in summary_season.values():
        for item in settings.SUMMARY_SEASON:
            v[item] = 0
        v["summary"] = 0
    # 节气统计
    for item in settings.DYNASTY:
        summary_solar_term[item] = {}
    for v in summary_solar_term.values():
        for item in settings.SUMMARY_SOLAR_TERM:
            v[item] = 0
        v["summary"] = 0
    # 意象统计
    for item in settings.DYNASTY:
        summary_imagery[item] = {}
    for v in summary_imagery.values():
        for item in settings.SUMMARY_IMAGERY:
            v[item] = 0
        v["summary"] = 0
    # 颜色统计
    for item in settings.DYNASTY:
        summary_color[item] = {}
    for v in summary_color.values():
        for key in settings.SUMMARY_COLOR.keys():
            v[key] = {}
            for value in settings.SUMMARY_COLOR[key]:
                v[key][value] = 0
            v[key]["summary"] = 0
        v["summary"] = 0


def __count_all(dynasty: str, raw_str: str):
    # 季节统计
    for item in settings.SUMMARY_SEASON:
        count = raw_str.count(item)
        summary_season[dynasty][item] += count
        summary_season[dynasty]["summary"] += count
        summary_season["汇总"][item] += count
        summary_season["汇总"]["summary"] += count
    # 节气统计
    for item in settings.SUMMARY_SOLAR_TERM:
        count = raw_str.count(item)
        summary_solar_term[dynasty][item] += count
        summary_solar_term[dynasty]["summary"] += count
        summary_solar_term["汇总"][item] += count
        summary_solar_term["汇总"]["summary"] += count
    # 意象统计
    for item in settings.SUMMARY_IMAGERY:
        count = raw_str.count(item)
        summary_imagery[dynasty][item] += count
        summary_imagery[dynasty]["summary"] += count
        summary_imagery["汇总"][item] += count
        summary_imagery["汇总"]["summary"] += count
    # 颜色统计
    for key, arr in settings.SUMMARY_COLOR.items():
        for value in arr:
            count = raw_str.count(value)
            summary_color[dynasty][key][value] += count
            summary_color[dynasty][key]["summary"] += count
            summary_color[dynasty]["summary"] += count
            summary_color["汇总"][key][value] += count
            summary_color["汇总"][key]["summary"] += count
            summary_color["汇总"]["summary"] += count


def __summary_all():
    top_dir = settings.INPUT_DIR1
    for dynasty in os.listdir(top_dir):
        dynasty_path = os.path.join(top_dir, dynasty)
        if os.path.isdir(dynasty_path):
            for author_filename in os.listdir(dynasty_path):
                author_file_path = os.path.join(dynasty_path, author_filename)
                with open(author_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    print(ColorLogDecorator.yellow("  Processing: " + dynasty + "-" + str(author_filename)))
                    data = json.load(f)
                    for item in data["poems"]:
                        raw_str = item["title"] + item["content"]
                        if raw_str:
                            __count_all(dynasty, raw_str)


def __output_summary():
    output_path = os.path.join(settings.OUTPUT_DIR, 'multi_summary')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open(os.path.join(output_path, "season.json"), 'w+', encoding='utf-8') as f:
        json.dump(summary_season, f, ensure_ascii=False, indent=4)

    with open(os.path.join(output_path, "solar_term.json"), 'w+', encoding='utf-8') as f:
        json.dump(summary_solar_term, f, ensure_ascii=False, indent=4)

    with open(os.path.join(output_path, "imagery.json"), 'w+', encoding='utf-8') as f:
        json.dump(summary_imagery, f, ensure_ascii=False, indent=4)

    with open(os.path.join(output_path, "color.json"), 'w+', encoding='utf-8') as f:
        json.dump(summary_color, f, ensure_ascii=False, indent=4)


def main():
    ColorLogDecorator.active()

    # Step1. 数据结构 创建
    print(ColorLogDecorator.blue("Step1. 创建数据结构 - PROCESSING"))
    __init_ds()
    print(ColorLogDecorator.green("Step1. 创建数据结构 - DONE"))

    # Step2. 统计所有诗词信息
    print(ColorLogDecorator.blue("Step2. 统计各项信息 - PROCESSING"))
    __summary_all()
    print(ColorLogDecorator.green("Step2. 统计各项信息 - DONE"))

    # Step3. 输出信息
    print(ColorLogDecorator.blue("Step3. 输出统计信息 - PROCESSING"))
    __output_summary()
    print(ColorLogDecorator.green("Step3. 输出统计信息 - DONE"))

    print("----" + ColorLogDecorator.green(" ALL DONE ", "bg-strong") + "----")


if __name__ == "__main__":
    main()
