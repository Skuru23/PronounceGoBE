import csv
import re


def process_row(row):
    pattern = r"\[.*?\]"
    matches = list(re.finditer(pattern, row))
    first_comma_position = None
    for i, char in enumerate(row):
        if char == ",":
            if not any(match.start() < i < match.end() for match in matches):
                first_comma_position = i
                break
    if first_comma_position is not None:
        parts = [row[:first_comma_position], row[first_comma_position + 1 :]]
        result = parts[0] + "+" + parts[1].replace("+", "&")
        return result

    return row


input_file = "create_dictionary/dictionary.csv"
output_file = "create_dictionary/cleaned_dict.csv"

with open(input_file, "r", encoding="utf-16") as infile, open(
    output_file, "w", encoding="utf-8"
) as outfile:
    for line in infile:
        modified_line = process_row(line.strip())
        outfile.write(modified_line + "\n")

print(f"CSV processing complete. Modified file saved as {output_file}.")
