import os


def main():
    DIR = "tag"
    for file in os.listdir(DIR):
        with open(os.path.join(DIR, file), "r+", encoding="utf-8") as f:
            count = 0
            for line in f:
                char = line[0]
                if char == "B":
                    count += 1
                elif char == "E":
                    count -= 1
            if count > 0:
                pass
                # print("B > E: " + str(count) + " " + file)
            elif count < 0:
                print("B < E: " + str(count) + " " + file)


if __name__ == "__main__":
    main()
