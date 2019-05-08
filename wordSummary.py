import os
import json
import settings
from collections import Counter
from module.ColorLogDecorator import ColorLogDecorator

INPUT_DIR = os.path.join(settings.INPUT_DIR, 'segment')
OUTPUT_DIR = os.path.join(settings.OUTPUT_DIR, 'segmentSummary')
TOP_N = 100
FLUSH_LEN = 26


def main():
    ColorLogDecorator.active()
    print(ColorLogDecorator.green("- START - ", "strong"))

    result_summary = {}  # store the result by dynasty
    file_dynasty = {}  # store the files in each dynasty
    all_counter = Counter()  # store all word's count
    all_words_length = 0

    for item in settings.DYNASTY:  # init the ds
        result_summary[item] = []
        file_dynasty[item] = []

    # start handling
    all_files = os.listdir(INPUT_DIR)
    for file in all_files:
        dynasty = file.split('_')[0]
        file_dynasty[dynasty].append(file)

    all_length = len(all_files)
    pointer = 0
    for k, v in file_dynasty.items():

        file_words_list = []  # store the word which's length > 2 in this file

        for file in v:  # for every file
            pointer += 1
            msg = "Handling {0:.2f}% : {1}".format(pointer * 100 / all_length, file)
            print("\r" + ColorLogDecorator.blue(msg), end="")

            file_path = os.path.join(INPUT_DIR, file)

            with open(file_path, 'r+', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    raw_str = line.rstrip('\n').rstrip('\r').rstrip('\n\r').rstrip('\r\n')
                    if len(raw_str) > 1:
                        file_words_list.append(raw_str)

        this_counter = Counter(file_words_list)
        for item in this_counter.most_common(TOP_N):  # need top n limit
            result_summary[k].append({
                "name": item[0],
                "value": item[1] / len(file_words_list)
            })

        all_counter.update(this_counter)
        all_words_length += len(file_words_list)

    print("\r" + ColorLogDecorator.blue("Handling {0:.2f}%".format(100)))

    for item in all_counter.most_common(TOP_N):  # need top n limit
        result_summary["汇总"].append({
            "name": item[0],
            "value": item[1] / all_words_length
        })

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(os.path.join(OUTPUT_DIR, "summary.json"), 'w+', encoding='utf-8') as f:
        json.dump(result_summary, f, ensure_ascii=False, indent=4)
    print(ColorLogDecorator.green("- DONE - ", "strong"))


if __name__ == '__main__':
    main()
