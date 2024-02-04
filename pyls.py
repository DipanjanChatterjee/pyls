import re
import sys
import json
import argparse
from typing import Union
from datetime import datetime


class UnixCommand:

    def __init__(self, structure_list: list):
        self.structure = structure_list

    # Output Generated Commands
    # ls - lists out the top level directories and files, and it ignores those files which starts with '.'
    # A - lists out the top level directories and files including files which starts with '.'
    # l - get details information of the files and directories like permission, file or directory size, date,
    # name vertically
    def output_generated_command(self, a_flag: bool, l_flag: bool) -> str:
        """
        Generate Output for commands like ls, A, l
        :param a_flag: Boolean type if false then any files starts with '.', will be ignored else will be included
        :param l_flag: type: Boolean type if false then only file name will be going to shown else every details like
        permission, file or directory size, date, name vertically will be shown
        :return: type: string type as a final output
        """
        if l_flag and a_flag:  # pyls -l -A
            return '\n'.join([
                f'{items.get("permissions")} {items.get("size")} '
                f'{datetime.fromtimestamp(items.get("time_modified")).strftime("%b %d %H:%M")} {items.get("name")}'
                for items in self.structure
            ])
        elif l_flag and not a_flag:  # pyls -l
            return '\n'.join([
                f'{items.get("permissions")} {items.get("size")} '
                f'{datetime.fromtimestamp(items.get("time_modified")).strftime("%b %d %H:%M")} {items.get("name")}'
                for items in self.structure if len(re.findall('^\\.\\w+', items.get('name'))) <= 0])
        elif not l_flag and a_flag:  # pyls -A
            return ' '.join([items.get('name') for items in self.structure])
        else:  # pyls
            return ' '.join(
                [items.get('name') for items in self.structure if len(re.findall('^\\.\\w+', items.get('name'))) <= 0])

    # Transformation Commands

    # r - reverse the order of the file or directory
    def command_r(self):
        """
        Reverse the order of the file or directory and update the existing structure.
        :return: None
        """
        self.structure = reversed(self.structure)

    # t - sorted the order of the file or directory based on time (oldest first)
    def command_t(self):
        """
        Sort the order based on time (oldest first) of the file or directory and update the existing structure.
        :return: None
        """
        self.structure = sorted(self.structure, key=lambda item: datetime.fromtimestamp(item.get('time_modified')))

    # filter - filter out files or directory based on the filter type
    def command_filter(self, filter_name: str):
        """
        Filter out files or directory.
        :param filter_name: String type if file then all files will be filtered out else if directory then all
        directories will be filtered out else error will be thrown with proper information and update the existing
        structure.
        :return: None
        """
        if filter_name.lower() == 'dir':
            self.structure = [items for items in self.structure if
                              len(re.findall('(?i)\\.|LICENSE', items.get('name'))) <= 0]
        elif filter_name.lower() == 'file':
            self.structure = [items for items in self.structure if
                              len(re.findall('(?i)\\.|LICENSE', items.get('name'))) > 0]
        else:
            raise Exception(f"'{filter_name}' is not a valid filter criteria. Available filters are 'dir' and 'file'")


# <path> - Search path item in directory info and find all subdirectories, files.
def handle_directory_path(directory_info: Union[dict, list], path_list: list, route_list=None) -> list:
    """
    A generator recursive function that searches the provided path through directory info. If found, then yield all
    corresponding subdirectories, files or path of the file.
    :param route_list: None type, Optional; if the relative path is provided, then traversal route gets created in this
    list.
    :param directory_info: Dictionary or List type; this holds all the details of the directories, subdirectories and
    files.
    :param path_list: List type; this holds all fragments of path as elements.
    :return: If found, then all information with subdirectories and files or about the files only.
    """

    global is_path_found

    if route_list is None:
        route_list: list = []
    path_fragment: str = path_list[0]
    if isinstance(directory_info, dict):
        if directory_info.get('name') == path_fragment:
            route_list += [directory_info.get('name')] if len(route_list) > 0 else []
            path_list: list = path_list[1:]
            if len(path_list) > 0:
                directory_info: Union[dict, list] = directory_info.get('contents')
                for result in handle_directory_path(directory_info, path_list, route_list):
                    yield result
            else:
                if len(route_list) > 0:
                    directory_info['name'] = '/'.join(route_list)
                is_path_found = True
                yield directory_info.get('contents') or [directory_info]
        else:
            directory_info: Union[dict, list] = directory_info.get('contents')
            for result in handle_directory_path(directory_info, path_list, route_list):
                yield result
    elif isinstance(directory_info, list):
        for item in directory_info:
            for result in handle_directory_path(item, path_list, route_list):
                yield result


# Argument Parser Inputs
parser = argparse.ArgumentParser(description='Unix Command Executor For Directory Parser')
parser.add_argument('--structure', type=str, default='Structure/Structure.json',
                    help='Provide Structure file location, Default Structure.json')
parser.add_argument('path', nargs='?', type=str, default='',
                    help='Provide file or directory name or relative path')
parser.add_argument('-A', action='store_true',
                    help='Provide -A to get all the files and directories including files starting with "."')
parser.add_argument('-l', action='store_true',
                    help='Provide -l to get all the files and directories information like permission, '
                         'file or directory size, date, name vertically.')
parser.add_argument('-r', action='store_true', help='Provide -r to get the files and directories in reverse order.')
parser.add_argument('-t', action='store_true',
                    help='Provide -t to get the files and directories in sorted order based on time (oldest first).')
parser.add_argument('--filter', type=str, default='',
                    help='Provide --filter to filter out files or directories, available options are file and dir.')
args = parser.parse_args()  # Creating the argument object to parse argument

# Parsing Arguments and Defined Variables
structure_path = args.structure
path = args.path
all_file_flag = args.A
list_info_flag = args.l
reverse_flag = args.r
time_sorting_flag = args.t
filter_type = args.filter
is_path_found = False

# Reading Structures
file_object = open(structure_path, 'r')
structure = json.load(file_object)
file_object.close()

if path:
    for updated_structure in handle_directory_path(structure, re.sub('^\\./', 'interpreter/', path).split('/'),
                                                   ['.'] if '/' in path else []):
        structure = updated_structure
else:
    for updated_structure in handle_directory_path(structure, 'interpreter'.split('/')):
        structure = updated_structure

if not is_path_found:
    print(f"error: can not access '{path}': No such file or directory")
    sys.exit()

command_object = UnixCommand(structure)  # Creating Unix Command Objects

if filter_type:
    try:
        command_object.command_filter(filter_name=filter_type)
    except Exception as error_message:
        print(f"error: {', '.join(error_message.args)}")
        sys.exit()
if time_sorting_flag:
    command_object.command_t()
if reverse_flag:
    command_object.command_r()
print(command_object.output_generated_command(all_file_flag, list_info_flag))
