import os
import re
import sys
from pathlib import Path


def grep_function_file(reg_exp, path, arg_dict):
    try:
        file_descriptor = open(path, "r")
        file_lines_normal = file_descriptor.readlines()
        if arg_dict.get("-ignoreCase"):
            reg_exp = reg_exp.upper()
            file_lines = list(map(lambda line: line.upper(), file_lines_normal))
        else:
            file_lines = file_lines_normal
        match_lines = []
        not_match_lines = []
        file_match_counter = 0
        for index, file_line in enumerate(file_lines):
            line_match_counter = len(re.findall(reg_exp, file_line))
            if line_match_counter > 0:
                match_lines.append(file_lines_normal[index])
            else:
                not_match_lines.append(file_lines_normal[index])
            file_match_counter += line_match_counter
        if arg_dict.get("-not"):
            if arg_dict.get("-count"):
                print(len(not_match_lines))
            else:
                for line in not_match_lines:
                    print(line[:len(line) - 1])
        else:
            if arg_dict.get("-count"):
                print(len(match_lines))
            else:
                for line in match_lines:
                    print(line[:len(line) - 1])
    except:
        print("Failed to read the file")


def grep_function_directory(reg_exp, path, arg_dict):
    if arg_dict.get("-ignoreCase"):
        reg_exp = reg_exp.upper()
    if os.path.isdir(path):
        for element in os.listdir(path):
            file_path = os.path.join(path, element)
            if os.path.isfile(file_path):
                try:
                    file_descriptor = open(file_path, "r")
                    file_lines = file_descriptor.readlines()
                    if arg_dict.get("-ignoreCase"):
                        file_lines = list(map(lambda line: line.upper(), file_lines))
                    match_counter = 0
                    for file_line in file_lines:
                        line_match_counter = len(re.findall(reg_exp, file_line))
                        match_counter += line_match_counter
                    if match_counter > 0 and not arg_dict.get("-not"):
                        if arg_dict.get("-count"):
                            print(file_path + " " + str(match_counter))
                        else:
                            print(file_path)
                    elif match_counter == 0 and arg_dict.get("-not"):
                        print(file_path)
                except:
                    continue
            else:
                grep_function_directory(reg_exp, file_path, arg_dict)
    return 0


if __name__ == '__main__':
    arguments_no = len(sys.argv)
    if arguments_no < 2 or arguments_no > 6:
        print('[Invalid number of arguments] grep.py reg_exp path -ignoreCase -not -count')
        exit(1)

    if not isinstance(sys.argv[1], str):
        print('[Invalid argument] Second argument must be an regular expression.')
        exit(1)

    path = Path(sys.argv[2])
    if not path.exists():
        print("[Invalid argument] The file doesn\'t exists.")
        exit(1)

    arguments = dict.fromkeys(["-ignoreCase", "-not", "-count"], False)
    if arguments_no > 3:
        optional_arguments = sys.argv[3:arguments_no]
        for argument in optional_arguments:
            if argument in ["-ignoreCase", "-not", "-count"]:
                arguments.update({argument: True})
            else:
                print("[Invalid optional argument] grep.py reg_exp file -ignoreCase -not -count")
                exit(1)
    #print(arguments.values())
    if os.path.isdir(path):
        grep_function_directory(sys.argv[1], path, arguments)
    else:
        grep_function_file(sys.argv[1], path, arguments)
