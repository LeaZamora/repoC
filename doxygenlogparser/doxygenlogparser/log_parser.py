import os
import re
import csv
import argparse


class LogParser:
    def __init__(self, log_file, output_file):
        self.log_file = log_file
        self.header = ['file', 'line', 'message']
        self.output_file = output_file

    def __process_warning_txt(self):
        with open(self.log_file, "r") as file:
            lines = file.readlines()
        return [self._format_line(line) for line in lines if self._format_line(line)]

    def _format_line(self, log_data):
        pattern = r"(?P<file_name>.+([.](\w+)))\:(?P<line_number>\d+)\: (?P<message>.*)"
        file_name = None

        matches = re.finditer(pattern, log_data, re.DOTALL)
        for match in matches:
            if match:
                # Extract named groups (file_name, line_number, message)
                file_name = match.group('file_name')
                line_number = match.group('line_number')
                message = match.group('message').strip()

        return [file_name, line_number, message] if file_name is not None else None

    def __write_to_csv(self, log_lines):
        with open(self.output_file, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(self.header)
            writer.writerows(log_lines)

    def parse_file(self):
        stripped_lines = self.__process_warning_txt()
        #print(stripped_lines)
        self.__write_to_csv(stripped_lines)


def validate_args(args):
    if not os.path.exists(args.warning_log_file):
        raise ValueError(f'warning_log_file "{args.warning_log_file}" does not exist!')
    args.output = 'output.csv' if args.output is None else args.output
    return args


def main():

    parser = argparse.ArgumentParser(description="Simple Doxygen Log Parser")
    parser.add_argument('--warning_log_file', type=str, help='Path to warning_log_file.txt', required=True)
    parser.add_argument('--output', type=str, help='Path TO Output file. This is optional', required=False)
    args = parser.parse_args()
    try:
        validated_args = validate_args(args)
    except ValueError as e:
        parser.error(str(e))
    log_parser = LogParser(validated_args.warning_log_file, validated_args.output)
    log_parser.parse_file()


if __name__ == '__main__':
    main()