import re
import requests


def _get_input(url, retries=5):
    tries = 0
    while tries < retries:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text
    raise Exception("Failed to get puzzle input.")


def _read_input(filepath):
    file_contents = None
    with open(filepath, "r") as f:
        file_contents = f.readlines()
    return file_contents


def day_01():
    input_lines = _read_input("inputs/day01.txt")

    # Part 1
    calibration_sum = 0

    for line in input_lines:
        digits = ""
        for i in range(len(line)):
            if line[i] in "0123456789":
                digits += line[i]
                break
        for i in range(len(line) - 1, -1, -1):
            if line[i] in "0123456789":
                digits += line[i]
                break
        calibration_sum += int(digits)

    print(calibration_sum)

    # Part 2
    calibration_sum = 0
    first_digit_re = re.compile(r"^.*?(one|two|three|four|five|six|seven|eight|nine|[0-9]){1}.*")
    last_digit_re = re.compile(r".*(one|two|three|four|five|six|seven|eight|nine|[0-9]){1}.*?$")
    text_to_digit = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }

    for line in input_lines:
        first_digit = first_digit_re.match(line).group(1)
        last_digit = last_digit_re.match(line).group(1)
        if first_digit in text_to_digit:
            first_digit = text_to_digit[first_digit]
        if last_digit in text_to_digit:
            last_digit = text_to_digit[last_digit]
        calibration_sum += int(first_digit + last_digit)

    print(calibration_sum)


def day_02():
    input_lines = _read_input("inputs/day02.txt")

    # Part 1

    id_sum = 0

    for i in range(len(input_lines)):
        line = input_lines[i]
        game_id = i + 1
        bad_game = False
        _, reveal_text = line.split(":")
        reveals = reveal_text.split(";")
        for reveal in reveals:
            cube_counts = [r.strip() for r in reveal.split(",")]
            for count in cube_counts:
                number, color = count.split(" ")
                number = int(number)
                if (color == "red" and number > 12) or (color == "green" and number > 13) or (color == "blue" and number > 14):
                    bad_game = True
                    break
            if bad_game:
                break
        if not bad_game:
            id_sum += game_id

    print(id_sum)

    # Part 2

    power_sum = 0

    for line in input_lines:
        _, reveal_text = line.split(":")
        reveals = reveal_text.split(";")
        max_red, max_green, max_blue = (0, 0, 0)
        for reveal in reveals:
            cube_counts = [r.strip() for r in reveal.split(",")]
            for count in cube_counts:
                number, color = count.split(" ")
                number = int(number)
                if color == "red" and number > max_red:
                    max_red = number
                elif color == "green" and number > max_green:
                    max_green = number
                elif color == "blue" and number > max_blue:
                    max_blue = number
        power_sum += max_red * max_green * max_blue

    print(power_sum)


if __name__ == "__main__":
    day_02()
