import re
import sys
import json
import argparse
from pathlib import Path
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
    def output_generated_command(self, a_flag: bool, l_flag: bool, h_flag: bool) -> str:
        """
        Generate Output for commands like ls, A, l
        :param a_flag: Boolean type if false then any files starts with '.', will be ignored else will be included
        :param l_flag: type: Boolean type if false then only file name will be going to shown else every details like
        permission, file or directory size, date, name vertically will be shown
        :param h_flag: Boolean type if true then size of the file will be converted into human-readable size else size
        will remain the same.
        :return: type: string type as a final output
        """
        if l_flag and a_flag:  # pyls -l -A
            return '\n'.join([
                f'{items.get("permissions")} {self.size_converter(items.get("size")) if h_flag else items.get("size")} '
                f'{datetime.fromtimestamp(items.get("time_modified")).strftime("%b %d %H:%M")} {items.get("name")}'
                for items in self.structure
            ])
        elif l_flag and not a_flag:  # pyls -l
            return '\n'.join([
                f'{items.get("permissions")} {self.size_converter(items.get("size")) if h_flag else items.get("size")} '
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

    # Human Readable Size Converter - Convert file or directory size into Human Readable Size
    def size_converter(self, size: Union[int, float], units=None) -> str:
        """
        Convert file or directory size into human-readable size
        :param size: Float or Integer type; file or directory size
        :param units: None type, Optional; units holds size units
        :return: String type; returns converted human-readable size
        """
        if units is None:
            units = ['', 'K', 'M', 'G', 'T', 'P', 'E']
        return re.sub('\\.\\d+$', '', f'{size:.1f}{units[0]}') if size < 1024 else (self.size_converter
                                                                                    (size / 1024, units[1:]))


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
parser = argparse.ArgumentParser(
    prog='PYLS',
    usage='%(prog)s retrieve and display the top-level directories and files from a JSON file, excluding those whose'
          ' names start with "."',
    description='This is equipped to execute a variety of commands, including Unix commands such as ls, '
                'ls -A, ls -l, and more alongside some custom commands.\nExplore the extensive range of functionalities'
                ' by referring to the provided arguments.',
    epilog='''Example:
    python pyls.py | pyls 
    python pyls.py --structure=Structure/Structure.json  | pyls --structure=Structure/Structure.json
    python pyls.py --root=interpreter | pyls --root=interpreter
    python pyls.py  parser | pyls parser
    python pyls.py  -A | pyls -A
    python pyls.py  -l | pyls -l
    python pyls.py  -l -r | pyls -l -r
    python pyls.py  -l -t | pyls -l -t
python pyls.py  -l --filter=file | python pyls.py  -l --filter=dir | pyls -l --filter=file | pyls -l --filter=dir
    python pyls.py  -l -h | pyls -l -h
    python pyls.py  --help | pyls --help
    ''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    add_help=False)
parser.add_argument('--structure', type=str, default='Structure/Structure.json',
                    help='JSON file location which holds files and directory information. Default value is '
                         'Structure/Structure.json')
parser.add_argument('--root', type=str, default='interpreter',
                    help='Decide the root directory. Default value is interpreter')
parser.add_argument('path', nargs='?', type=str, default='',
                    help='Handle paths to navigate the directory structure, also supports relative paths')
parser.add_argument('-A', action='store_true',
                    help='Show all the files and directories including files starting with "."')
parser.add_argument('-l', action='store_true',
                    help='Show the files and directories information like permission, size, date, name vertically.')
parser.add_argument('-r', action='store_true', help='Reverse the order of files and directories.')
parser.add_argument('-t', action='store_true', help='Sort files and directories based on time (oldest first).')
parser.add_argument('--filter', type=str, default='',
                    help='Filter out files or directories. Available options are 1. file 2. dir.')
parser.add_argument('-h', action='store_true', help='Convert size of file or directories into human-readable size.')
parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help='Show help message and exit')

is_path_found = False


def execute(arguments=None):
    args = parser.parse_args(arguments)  # Creating the argument object to parse argument

    # Parsing Arguments and Defined Variables
    structure_path = args.structure
    root_directory = args.root
    path = args.path
    all_file_flag = args.A
    list_info_flag = args.l
    reverse_flag = args.r
    time_sorting_flag = args.t
    filter_type = args.filter
    human_size_flag = args.h

    # Reading Structures
    file_object = open(Path(Path(__file__).parent, structure_path), 'r')
    structure = json.load(file_object)
    file_object.close()

    if path:
        for updated_structure in handle_directory_path(structure,
                                                       re.sub('^\\./', f'{root_directory}/', path).split('/'),
                                                       ['.'] if '/' in path else []):
            structure = updated_structure
    else:
        for updated_structure in handle_directory_path(structure, root_directory.split('/')):
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
    print(command_object.output_generated_command(all_file_flag, list_info_flag, human_size_flag))
