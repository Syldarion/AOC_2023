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


if __name__ == "__main__":
    day_01()
