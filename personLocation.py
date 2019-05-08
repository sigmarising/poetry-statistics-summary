import os
import json
import settings
from collections import Counter
from module.ColorLogDecorator import ColorLogDecorator

INPUT_DIR = os.path.join(settings.INPUT_DIR, 'nerResult')
OUTPUT_DIR = os.path.join(settings.OUTPUT_DIR, 'impact')
TOP_N = 100


def main():
    ColorLogDecorator.active()
    print(ColorLogDecorator.green("- START -", "strong"))

    print(ColorLogDecorator.yellow("STEP 1. 创建数据结构"))
    locations = []  # 汇总所有的提及地点
    persons = []  # 汇总所有的提及人物
    result_locations = {}  # 最终 地点 结果
    result_persons = {}  # 最终 人物 结果
    for item in settings.DYNASTY:  # 初始化
        result_locations[item] = []
        result_persons[item] = []
    print(ColorLogDecorator.yellow("STEP 1. DONE"))

    print(ColorLogDecorator.yellow("STEP 2. 统计人物、地点影响力"))
    for dynasty in os.listdir(INPUT_DIR):  # 对于每个朝代

        dynasty_path = os.path.join(INPUT_DIR, dynasty)
        this_location = []  # 此朝代的所有提及地点
        this_person = []  # 此朝代的所有提及人物
        all_files = os.listdir(dynasty_path)
        this_len = len(all_files)
        pointer = 0

        for file in all_files:  # 朝代中的每个文件

            pointer += 1
            msg = "  Handling {0} {1:.2f}% : {2}".format(dynasty, pointer * 100 / this_len, file)
            print(ColorLogDecorator.blue(msg))
            file_path = os.path.join(dynasty_path, file)
            with open(file_path, 'r+', encoding='utf-8', errors='ignore') as f:
                raw = json.load(f)
                this_location += raw["location"]
                this_person += raw["person"]

        this_location_count = Counter(this_location)
        this_person_count = Counter(this_person)
        for item in this_location_count.most_common(TOP_N):
            result_locations[dynasty].append({
                "name": item[0],
                "value": item[1] / len(this_location)
            })
        for item in this_person_count.most_common(TOP_N):
            result_persons[dynasty].append({
                "name": item[0],
                "value": item[1] / len(this_person)
            })

        locations += this_location
        persons += this_person

    all_location_count = Counter(locations)
    all_person_count = Counter(persons)
    for item in all_location_count.most_common(TOP_N):
        result_locations["汇总"].append({
            "name": item[0],
            "value": item[1] / len(locations),
        })
    for item in all_person_count.most_common(TOP_N):
        result_persons["汇总"].append({
            "name": item[0],
            "value": item[1] / len(persons)
        })
    print(ColorLogDecorator.yellow("STEP 2. DONE"))

    print(ColorLogDecorator.yellow("STEP 3. 输出文件"))
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(os.path.join(OUTPUT_DIR, "locations.json"), 'w+', encoding='utf-8') as f:
        json.dump(result_locations, f, ensure_ascii=False, indent=4)
    with open(os.path.join(OUTPUT_DIR, "persons.json"), 'w+', encoding='utf-8') as f:
        json.dump(result_persons, f, ensure_ascii=False, indent=4)
    print(ColorLogDecorator.yellow("STEP 3. DONE"))

    print(ColorLogDecorator.green("- ALL DONE -", "strong"))


if __name__ == '__main__':
    main()
