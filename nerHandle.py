import os
import json
import settings
from module.ColorLogDecorator import ColorLogDecorator


class FileReader(object):
    def __init__(self, filename: str):
        self.filename: str = filename

    def get_line(self):
        with open(self.filename, 'r+', encoding='utf-8', errors='ignore') as f:
            for line in f:
                yield line.rstrip('\n').rstrip('\r').rstrip('\n\r').rstrip('\r\n')


def main():
    def __handle_detail(temp: list, target: dict, tag: str):
        if tag == 'L':
            final = "location"
        elif tag == 'T':
            final = "time"
        elif tag == 'P':
            final = "person"

        count_b = 0
        count_e = 0
        for item in temp:
            if item["tag_full"][0] == 'B':
                count_b += 1
            elif item["tag_full"][0] == 'E':
                count_e += 1

        word_list: list
        if count_b >= count_e:
            word_str = ""
            for item in temp:
                if item["tag_full"][0] == 'B':
                    word_str += "B"
                word_str += item["text"]
            word_list = list(filter(lambda x: x, word_str.split('B')))
        elif count_b < count_e:
            word_str = ""
            for item in temp:
                word_str += item["text"]
                if item["tag_full"][0] == 'E':
                    word_str += "E"
            word_list = list(filter(lambda x: x, word_str.split('E')))
        for item in word_list:
            target[final].append(item)

    ColorLogDecorator.active()
    print(ColorLogDecorator.green("- START -"))

    input_dir_top = settings.INPUT_DIR2
    input_dir_text = os.path.join(input_dir_top, 'forLattice')
    input_dir_tag = os.path.join(input_dir_top, 'tag')
    output_path = os.path.join(settings.OUTPUT_DIR, 'nerResult')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for file in os.listdir(input_dir_tag):
        print(ColorLogDecorator.blue("Handling: " + file))

        dynasty = file.split('_')[0]
        author = str(file.split('_')[1]).split('.')[0]

        path_text = os.path.join(input_dir_text, file)
        path_tag = os.path.join(input_dir_tag, file)

        fr_text = FileReader(path_text)
        fr_tag = FileReader(path_tag)
        generate_text = fr_text.get_line()
        generate_tag = fr_tag.get_line()

        result: dict = {
            "dynasty": dynasty,
            "author": author,
            "location": [],
            "person": [],
            "time": []
        }
        state = "O"
        temp_word = []

        try:
            while True:
                line_text = next(generate_text)
                line_tag = next(generate_tag)
                if line_text == "" or line_tag == "":
                    continue

                text = line_text.split(' ')[0]
                tag_id = line_tag.split('-')[1] if len(line_tag) > 1 else line_tag[0]

                if state == 'O':
                    if tag_id == 'O':
                        state = 'O'
                    elif tag_id == 'L':
                        state = 'L'
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                    elif tag_id == 'T':
                        state = 'T'
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                    elif tag_id == 'P':
                        state = 'P'
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                elif state == 'L':
                    if tag_id == 'O':
                        state = 'O'
                        __handle_detail(temp_word, result, 'L')
                        temp_word.clear()
                    elif tag_id == 'L':
                        state = 'L'
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                    elif tag_id == 'T':
                        state = 'T'
                        __handle_detail(temp_word, result, 'L')
                        temp_word.clear()
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                    elif tag_id == "P":
                        state = 'P'
                        __handle_detail(temp_word, result, 'L')
                        temp_word.clear()
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                elif state == 'T':
                    if tag_id == 'O':
                        state = 'O'
                        __handle_detail(temp_word, result, 'T')
                        temp_word.clear()
                    elif tag_id == 'L':
                        state = 'L'
                        __handle_detail(temp_word, result, 'T')
                        temp_word.clear()
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                    elif tag_id == 'T':
                        state = 'T'
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                    elif tag_id == 'P':
                        state = 'P'
                        __handle_detail(temp_word, result, 'T')
                        temp_word.clear()
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                elif state == 'P':
                    if tag_id == 'O':
                        state = 'O'
                        __handle_detail(temp_word, result, 'P')
                        temp_word.clear()
                    elif tag_id == 'L':
                        state = 'L'
                        __handle_detail(temp_word, result, 'P')
                        temp_word.clear()
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                    elif tag_id == 'T':
                        state = 'T'
                        __handle_detail(temp_word, result, 'P')
                        temp_word.clear()
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
                    elif tag_id == 'P':
                        state = 'P'
                        temp_word.append({
                            "text": text,
                            "tag_full": line_tag
                        })
        except StopIteration:
            if len(temp_word) != 0:
                __handle_detail(temp_word, result, state)

        output_file_path = os.path.join(output_path, str(file.split('.')[0]) + ".json")
        with open(output_file_path, 'w+', encoding='utf-8', errors='ignore') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    print(ColorLogDecorator.green("- DONE -"))


if __name__ == '__main__':
    main()
