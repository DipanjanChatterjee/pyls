import json
import argparse
from datetime import datetime


class UnixCommand:

    def __init__(self, structure_dict: dict):
        self.structure = structure_dict

    # Parse Directory
    def directory_parser(self, name: str):
        if self.structure.get('name') == name:
            self.structure = self.structure.get('contents')

    # Output Generated Commands
    # ls - lists out the top level directories and files, and it ignores those files which starts with '.'
    # A - lists out the top level directories and files, and it ignores those files which starts with '.'
    def output_generated_command(self, a_flag: bool, l_flag: bool) -> str:
        """
        Generate Output for commands like ls, A, l
        :param a_flag: boolean type if false then any files starts with '.', will be ignored else will be included
        :param l_flag: type: boolean type if false then only file name will be going to shown else every details like
        permission, file or directory size, date, name will be shown
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
                for items in self.structure if not items.get('name').startswith('.')])
        elif not l_flag and a_flag:  # pyls -A
            return ' '.join([items.get('name') for items in self.structure])
        else:  # pyls
            return ' '.join([items.get('name') for items in self.structure if not items.get('name').startswith('.')])


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
                         'file or directory size, date, name.')
args = parser.parse_args()  # Creating the argument object to parse argument

# Parsing Arguments
structure_path = args.structure
path = args.path
all_file_flag = args.A
list_info_flag = args.l

# Reading Structures
file_object = open(structure_path, 'r')
structure = json.load(file_object)
file_object.close()

command_object = UnixCommand(structure)  # Creating Unix Command Objects

if path:
    print()
else:
    command_object.directory_parser('interpreter')

print(command_object.output_generated_command(all_file_flag, list_info_flag))
