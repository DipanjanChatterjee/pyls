from pytest import mark

# Custom Import
from pyls.pyls import execute


class TestPyls:

    @mark.parametrize(
        'args, expected',
        [
            (
                    [],
                    'LICENSE README.md ast go.mod lexer main.go parser token'
            ),
            (
                    ['-A'],
                    '.gitignore LICENSE README.md ast go.mod lexer main.go parser token'
            ),
            (
                    ['-l'],
                    '''drwxr-xr-x 1071 Nov 14 11:27 LICENSE
drwxr-xr-x 83 Nov 14 11:27 README.md
-rw-r--r-- 4096 Nov 14 15:58 ast
drwxr-xr-x 60 Nov 14 13:51 go.mod
drwxr-xr-x 4096 Nov 14 15:21 lexer
-rw-r--r-- 74 Nov 14 13:57 main.go
drwxr-xr-x 4096 Nov 17 12:51 parser
-rw-r--r-- 4096 Nov 14 14:57 token'''
            ),
            (
                    ['-A', '-l'],
                    '''drwxr-xr-x 8911 Nov 14 11:27 .gitignore
drwxr-xr-x 1071 Nov 14 11:27 LICENSE
drwxr-xr-x 83 Nov 14 11:27 README.md
-rw-r--r-- 4096 Nov 14 15:58 ast
drwxr-xr-x 60 Nov 14 13:51 go.mod
drwxr-xr-x 4096 Nov 14 15:21 lexer
-rw-r--r-- 74 Nov 14 13:57 main.go
drwxr-xr-x 4096 Nov 17 12:51 parser
-rw-r--r-- 4096 Nov 14 14:57 token
'''
            ),
            (
                    ['-r'],
                    'token parser main.go lexer go.mod ast README.md LICENSE'
            ),
            (
                    ['-l', '-r'],
                    '''-rw-r--r-- 4096 Nov 14 14:57 token
drwxr-xr-x 4096 Nov 17 12:51 parser
-rw-r--r-- 74 Nov 14 13:57 main.go
drwxr-xr-x 4096 Nov 14 15:21 lexer
drwxr-xr-x 60 Nov 14 13:51 go.mod
-rw-r--r-- 4096 Nov 14 15:58 ast
drwxr-xr-x 83 Nov 14 11:27 README.md
drwxr-xr-x 1071 Nov 14 11:27 LICENSE
'''
            ),
            (
                    ['-A', '-l', '-r'],
                    '''-rw-r--r-- 4096 Nov 14 14:57 token
drwxr-xr-x 4096 Nov 17 12:51 parser
-rw-r--r-- 74 Nov 14 13:57 main.go
drwxr-xr-x 4096 Nov 14 15:21 lexer
drwxr-xr-x 60 Nov 14 13:51 go.mod
-rw-r--r-- 4096 Nov 14 15:58 ast
drwxr-xr-x 83 Nov 14 11:27 README.md
drwxr-xr-x 1071 Nov 14 11:27 LICENSE
drwxr-xr-x 8911 Nov 14 11:27 .gitignore'''
            ),
            (
                    ['-t'],
                    'LICENSE README.md go.mod main.go token lexer ast parser'
            ),
            (
                    ['-l', '-t'],
                    '''drwxr-xr-x 1071 Nov 14 11:27 LICENSE
drwxr-xr-x 83 Nov 14 11:27 README.md
drwxr-xr-x 60 Nov 14 13:51 go.mod
-rw-r--r-- 74 Nov 14 13:57 main.go
-rw-r--r-- 4096 Nov 14 14:57 token
drwxr-xr-x 4096 Nov 14 15:21 lexer
-rw-r--r-- 4096 Nov 14 15:58 ast
drwxr-xr-x 4096 Nov 17 12:51 parser
'''
            ),
            (
                    ['-l', '-r', '-t'],
                    '''drwxr-xr-x 4096 Nov 17 12:51 parser
-rw-r--r-- 4096 Nov 14 15:58 ast
drwxr-xr-x 4096 Nov 14 15:21 lexer
-rw-r--r-- 4096 Nov 14 14:57 token
-rw-r--r-- 74 Nov 14 13:57 main.go
drwxr-xr-x 60 Nov 14 13:51 go.mod
drwxr-xr-x 83 Nov 14 11:27 README.md
drwxr-xr-x 1071 Nov 14 11:27 LICENSE
'''
            ),
            (
                    ['-A', '-l', '-r', '-t'],
                    '''drwxr-xr-x 4096 Nov 17 12:51 parser
-rw-r--r-- 4096 Nov 14 15:58 ast
drwxr-xr-x 4096 Nov 14 15:21 lexer
-rw-r--r-- 4096 Nov 14 14:57 token
-rw-r--r-- 74 Nov 14 13:57 main.go
drwxr-xr-x 60 Nov 14 13:51 go.mod
drwxr-xr-x 83 Nov 14 11:27 README.md
drwxr-xr-x 1071 Nov 14 11:27 LICENSE
drwxr-xr-x 8911 Nov 14 11:27 .gitignore
'''
            ),
            (
                    ['--filter=file'],
                    'LICENSE README.md go.mod main.go'
            ),
            (
                    ['--filter=dir'],
                    'ast lexer parser token'
            ),
            (
                    ['--filter=folder'],
                    "error: 'folder' is not a valid filter criteria. Available filters are 'dir' and 'file'"
            ),
            (
                    ['-l', '--filter=file'],
                    '''drwxr-xr-x 1071 Nov 14 11:27 LICENSE
drwxr-xr-x 83 Nov 14 11:27 README.md
drwxr-xr-x 60 Nov 14 13:51 go.mod
-rw-r--r-- 74 Nov 14 13:57 main.go'''
            ),
            (
                    ['-l', '--filter=dir'],
                    '''-rw-r--r-- 4096 Nov 14 15:58 ast
drwxr-xr-x 4096 Nov 14 15:21 lexer
drwxr-xr-x 4096 Nov 17 12:51 parser
-rw-r--r-- 4096 Nov 14 14:57 token'''
            ),
            (
                    ['-l', '--filter=folder'],
                    "error: 'folder' is not a valid filter criteria. Available filters are 'dir' and 'file'"
            ),
            (
                    ['-l', '-r', '--filter=file'],
                    '''-rw-r--r-- 74 Nov 14 13:57 main.go
drwxr-xr-x 60 Nov 14 13:51 go.mod
drwxr-xr-x 83 Nov 14 11:27 README.md
drwxr-xr-x 1071 Nov 14 11:27 LICENSE'''
            ),
            (
                    ['-l', '-r', '--filter=dir'],
                    '''-rw-r--r-- 4096 Nov 14 14:57 token
drwxr-xr-x 4096 Nov 17 12:51 parser
drwxr-xr-x 4096 Nov 14 15:21 lexer
-rw-r--r-- 4096 Nov 14 15:58 ast'''
            ),
            (
                    ['-l', '-r', '--filter=folder'],
                    "error: 'folder' is not a valid filter criteria. Available filters are 'dir' and 'file'"
            ),
            (
                    ['-l', '-r', '-t', '--filter=file'],
                    '''-rw-r--r-- 74 Nov 14 13:57 main.go
drwxr-xr-x 60 Nov 14 13:51 go.mod
drwxr-xr-x 83 Nov 14 11:27 README.md
drwxr-xr-x 1071 Nov 14 11:27 LICENSE'''
            ),
            (
                    ['-l', '-r', '-t', '--filter=dir'],
                    '''drwxr-xr-x 4096 Nov 17 12:51 parser
-rw-r--r-- 4096 Nov 14 15:58 ast
drwxr-xr-x 4096 Nov 14 15:21 lexer
-rw-r--r-- 4096 Nov 14 14:57 token'''
            ),
            (
                    ['-l', '-r', '-t', '--filter=folder'],
                    "error: 'folder' is not a valid filter criteria. Available filters are 'dir' and 'file'"
            ),
            (
                    ['-A', '-l', '-r', '-t', '--filter=file'],
                    '''-rw-r--r-- 74 Nov 14 13:57 main.go
drwxr-xr-x 60 Nov 14 13:51 go.mod
drwxr-xr-x 83 Nov 14 11:27 README.md
drwxr-xr-x 1071 Nov 14 11:27 LICENSE
drwxr-xr-x 8911 Nov 14 11:27 .gitignore'''
            ),
            (
                    ['-A', '-l', '-r', '-t', '--filter=dir'],
                    '''drwxr-xr-x 4096 Nov 17 12:51 parser
-rw-r--r-- 4096 Nov 14 15:58 ast
drwxr-xr-x 4096 Nov 14 15:21 lexer
-rw-r--r-- 4096 Nov 14 14:57 token'''
            ),
            (
                    ['-A', '-l', '-r', '-t', '--filter=folder'],
                    "error: 'folder' is not a valid filter criteria. Available filters are 'dir' and 'file'"
            ),
            (
                    ['parser'],
                    'parser_test.go parser.go go.mod'
            ),
            (
                    ['parser/parser.go'],
                    './parser/parser.go'
            ),
            (
                    ['parser', '-l'],
                    '''drwxr-xr-x 1342 Nov 17 12:51 parser_test.go
-rw-r--r-- 1622 Nov 17 12:05 parser.go
drwxr-xr-x 533 Nov 14 16:03 go.mod'''
            ),
            (
                    ['parser/parser.go', '-l'],
                    '-rw-r--r-- 1622 Nov 17 12:05 ./parser/parser.go'
            ),
            (
                    ['-l', '-h'],
                    '''drwxr-xr-x 1.0K Nov 14 11:27 LICENSE
drwxr-xr-x 83 Nov 14 11:27 README.md
-rw-r--r-- 4.0K Nov 14 15:58 ast
drwxr-xr-x 60 Nov 14 13:51 go.mod
drwxr-xr-x 4.0K Nov 14 15:21 lexer
-rw-r--r-- 74 Nov 14 13:57 main.go
drwxr-xr-x 4.0K Nov 17 12:51 parser
-rw-r--r-- 4.0K Nov 14 14:57 token
'''
            ),
        ],
    )
    def test_pyls(self, args, expected, capsys):
        try:
            execute(args)
        except SystemExit:
            pass
        output, error = capsys.readouterr()
        assert output.strip() == expected.strip()
