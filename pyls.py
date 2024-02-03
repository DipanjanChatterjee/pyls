import json
import argparse


class UnixCommand:

    def __init__(self, structure_dict: dict):
        self.structure = structure_dict

    # Parse Directory
    def directory_parser(self, name: str):
        if self.structure.get('name') == name:
            self.structure = self.structure.get('contents')

    # Output Generated Commands

    # ls - lists out the top level directories and files, and it ignores those files which starts with '.'
    def command_ls(self) -> str:
        return ' '.join([items.get('name') for items in self.structure if not items.get('name').startswith('.')])

    # A - lists out the top level directories and files, and it ignores those files which starts with '.'
    def command_a(self) -> str:
        return ' '.join([items.get('name') for items in self.structure])


# Argument Parser Inputs
parser = argparse.ArgumentParser(description='Unix Command Executor For Directory Parser')
parser.add_argument('--structure', type=str, default='Structure/Structure.json',
                    help='Provide Structure file location, Default Structure.json')
parser.add_argument('path', nargs='?', type=str, default='',
                    help='Provide file or directory name or relative path')
parser.add_argument('-A', action='store_true',
                    help='Provide -A to get all the files and directories including files starting with "."')
args = parser.parse_args()  # Creating argument object to parse argument

# Parsing Arguments
structure_path = args.structure
path = args.path
all_file_flag = args.A

# Reading Structures
file_object = open(structure_path, 'r')
structure = json.load(file_object)
file_object.close()

command_object = UnixCommand(structure)  # Creating Unix Command Objects

if path:
    print()
else:
    command_object.directory_parser('interpreter')

if not all_file_flag:
    print(command_object.command_ls())
else:
    print(command_object.command_a())
