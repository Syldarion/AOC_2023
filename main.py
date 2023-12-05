import math
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
        file_contents = [l.strip() for l in f.readlines()]
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


def day_03():
    input_lines = _read_input("inputs/day03.txt")
    input_height = len(input_lines)
    input_width = len(input_lines[0])

    # Part 1

    # numbers are at most 3 digits, and we can do a different check for each digit:
    # 11133
    # 1XXX3
    # 11133
    # This diagram is basically, which positions each digit (1,2,3) need to check.
    # Oh wait, we can just do the first and last
    # There might be more optimization, because with this we'll double-check spots for numbers less than 3 digits

    def is_numeric(char):
        return char in "0123456789"

    neighbors = [
        [-1, -1],
        [0, -1],
        [1, -1],
        [-1, 0],
        [1, 0],
        [-1, 1],
        [0, 1],
        [1, 1],
    ]

    part_number_sum = 0

    for y in range(input_height):
        is_part_number = False
        current_digit_chars = ""
        for x in range(input_width):
            if is_numeric(input_lines[y][x]):
                current_digit_chars += input_lines[y][x]
                for neighbor in neighbors:
                    new_x = x + neighbor[0]
                    new_y = y + neighbor[1]
                    if 0 <= new_x < input_width and 0 <= new_y < input_height:
                        if input_lines[new_y][new_x] not in "0123456789.":
                            is_part_number = True
                            break
            elif current_digit_chars:
                # there's a number to parse
                if is_part_number:
                    part_number_sum += int(current_digit_chars)
                is_part_number = False
                current_digit_chars = ""
        if current_digit_chars and is_part_number:
            part_number_sum += int(current_digit_chars)

    print(part_number_sum)

    # Part 2

    ratio_sum = 0

    # for parts above/below
    # 1.1 -> 2 part
    # 11. -> 1 part
    # .11 -> 1 part
    # 1.. -> 1 part
    # ..1 -> 1 part
    # 111 -> 1 part
    # ... -> 0 part

    for y in range(input_height):
        for x in range(input_width):
            if input_lines[y][x] == "*":
                parts = []
                if y > 0:
                    # check parts above
                    line_slice = input_lines[y - 1][x - 3:x + 4]
                    numbers_in_line = re.findall(r"\d+", line_slice)
                    end = 0
                    for number in numbers_in_line:
                        start = line_slice.index(number, end)
                        end = start + len(number) - 1
                        if (start > 0): start -= 1
                        if (end < 6): end += 1
                        if start <= 3 <= end:
                            parts.append(int(number))
                if y < input_height - 1:
                    # check parts below
                    line_slice = input_lines[y + 1][x - 3:x + 4]
                    numbers_in_line = re.findall(r"\d+", line_slice)
                    end = 0
                    for number in numbers_in_line:
                        start = line_slice.index(number, end)
                        end = start + len(number) - 1
                        # 2,3,4 is the overlap
                        if (start > 0): start -= 1
                        if (end < 6): end += 1
                        if start <= 3 <= end:
                            parts.append(int(number))
                # get before / after
                first_half = input_lines[y][:x]
                second_half = input_lines[y][x+1:]
                first_half_numbers = re.findall(r"\d+", first_half)
                second_half_numbers = re.findall(r"\d+", second_half)

                if first_half_numbers and is_numeric(input_lines[y][x-1]):
                    parts.append(int(first_half_numbers[-1]))
                if second_half_numbers and is_numeric(input_lines[y][x+1]):
                    parts.append(int(second_half_numbers[0]))

                part_count = len(parts)

                if len(parts) == 2:
                    ratio_sum += parts[0] * parts[1]

    print(ratio_sum)


def day_04():
    input_lines = _read_input("inputs/day04.txt")

    card_sum = 0
    winner_count = []

    for line in input_lines:
        _, numbers = line.split(":")
        winners, mine = numbers.split("|")
        winners = winners.strip()
        mine = mine.strip()

        winning_numbers = set([int(num) for num in winners.split()])
        my_numbers = set([int(num) for num in mine.split()])

        matches = winning_numbers.intersection(my_numbers)
        winner_count.append(len(matches))

        if matches:
            card_sum += math.pow(2, len(matches) - 1)

    print(card_sum)

    card_count = len(input_lines)
    card_copies = [1] * card_count

    for i in range(card_count):
        if winner_count[i] > 0:
            for j in range(i + 1, min(card_count, i + winner_count[i] + 1)):
                card_copies[j] += card_copies[i]

    print(sum(card_copies))


def ranges_overlap(start_a, end_a, start_b, end_b):
    return start_a < end_b and end_a > start_b


def day_05():
    input_lines = _read_input("inputs/day05.txt")

    # we're just going to hard-code input lines
    seed_line = input_lines[0]

    ranges = [
        (3, 13),
        (15, 31),
        (34, 48),
        (50, 95),
        (97, 112),
        (114, 137),
        (139, 150)
    ]

    maps = []

    for line_range in ranges:
        lines = input_lines[line_range[0]:line_range[1]]
        map_str = [line.split() for line in lines]
        map_int = [[int(m[0]), int(m[1]), int(m[2])] for m in map_str]
        maps.append(map_int)

    seeds = [int(seed) for seed in seed_line.split(":")[1].strip().split()]

    locations = []
    for seed in seeds:
        current_mapping = seed
        for m in maps:
            temp_m = m[:]
            temp_m.append([current_mapping, current_mapping, 1])
            for dest, source, length in m:
                if source <= current_mapping <= source + length:
                    current_mapping += (dest - source)
                    break
        locations.append(current_mapping)
    print(min(locations))

    seed_starts = seeds[::2]
    seed_ranges = seeds[1::2]

    def find_lowest_location(range_start, range_end, map_index):
        locations = []

        had_overlap = False
        for dest, source, length in maps[map_index]:
            if ranges_overlap(range_start, range_end, source, source + length):
                had_overlap = True
                overlap_start = max(range_start, source)
                overlap_end = min(range_end, source + length)
                new_start = overlap_start + (dest - source)
                new_end = overlap_end + (dest - source)
                if map_index >= len(maps) - 1:
                    locations.append(new_start)
                else:
                    locations.append(find_lowest_location(new_start, new_end, map_index + 1))
        if not had_overlap:
            if map_index >= len(maps) - 1:
                locations.append(range_start)
            else:
                locations.append(find_lowest_location(range_start, range_end, map_index + 1))

        return min(locations)

    lowest_locations = []
    for i in range(len(seed_starts)):
        lowest_locations.append(find_lowest_location(seed_starts[i], seed_starts[i] + seed_ranges[i], 0))

    print(min(lowest_locations))


if __name__ == "__main__":
    day_05()
