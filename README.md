# pyls

Retrieve and display the top-level directories and files from a JSON file, excluding those whose names start with ".". This tool also supports the execution of various commands, including Unix commands such as ls, ls -A, ls -l, and more, along with some custom commands. Explore the extensive range of functionalities by referring to the **[Commands](#commands)** section below.

## **Installation**
Download the wheel file from the **dist** directory and use the following command:

`pip install pyls-1.0-py3-none-any.whl`

## **Usage**
Type pyls in the command prompt and start executing commands. Below are the supported commands with examples.  

## **Commands:**
1. **`pyls`**: This lists out the top level (in the directory interpreter) directories and files, and it ignores the file which starts with '.'. Example:

    ![pyls](images/pyls.png "pyls")
2. **`pyls -A`**: This prints all the files and directories (including files starting with '.'). Example:
    
    ![pyls -A](images/pyls_-A.png "pyls -A")
3. **`pyls -l`**: This prints details information of the files and directories like permission, file or directory size, date, name vertically. Example:

   ![pyls -l](images/pyls_-l.png "pyls -l")
4. **`pyls -l -r`**: This reverses the order of the files and directory. Example:

   ![pyls -l -r](images/pyls_-l_-r.png "pyls -l -r")
5. **`pyls -l -t`**: This sorted order of the files and directory based on time (oldest first). Example:

   ![pyls -l -t](images/pyls_-l_-t.png "pyls -l -t")
6. **`pyls -l --filter=<option>`**: This filtered out file or directories based on provided options(file, dir). `pyls -l --filter=file` filtered out only file, `pyls -l --filter=dir` filtered out only dir, but an error message will be displayed if neither _file_ nor _dir_ is specified. Example:
   
   |          Command          |                                         Images                                          |
   |:-------------------------:|:---------------------------------------------------------------------------------------:|
   |  `pyls -l --filter=dir`   |     ![pyls -l --filter=dir](images/pyls_-l_-filter=dir.png "pyls -l --filter=dir")      |
   |  `pyls -l --filter=file`  |    ![pyls -l --filter=file](images/pyls_-l_-filter=file.png "pyls -l --filter=file")    |
   | `pyls -l --filter=folder` | ![pyls -l --filter=folder](images/pyls_-l_-filter=folder.png "pyls -l --filter=folder") |
7. **`pyls -l <path>`**: This searched through the directories shows all the subdirectories, files. It can also handle relative paths, but if the path is unknown, then an error will be shown. Example:

   |           Command           |                                        Images                                         |
   |:---------------------------:|:-------------------------------------------------------------------------------------:|
   |      `pyls -l parser`       | ![pyls_-l_directory_name](images/pyls_-l_directory_name.png "pyls_-l_directory_name") |
   | `pyls -l parser/parser.go`  |  ![pyls_-l_relative_path](images/pyls_-l_relative_path.png "pyls_-l_relative_path")   |
   | `pyls -l non_existent_path` | ![pyls_-l_incorrect_path](images/pyls_-l_incorrect_path.png "pyls_-l_incorrect_path") |
8. **`pyls -l -h`**: This converted size of the file or directory to human-readable size. Example:

   ![pyls -l -h](images/pyls_-l_-h.png "pyls -l -h")
9. **`pyls --help`**: This showed helpful message, usage, description, lists all available commands and example. Example:

   ![pyls --help](images/pyls_-help1.png "pyls --help")
   ![pyls --help](images/pyls_-help2.png "pyls --help")

## **Testcases**
Testcases are provided in the [Testcases](testcases) directory. The tests are conducted using the pytest module. To install the pytest module, use the following command `pip install pytest`. Please reference the file [Structure.json](pyls/Structure/Structure.json) where all the directory structure has been mentioned, which is used for taking examples and executing the script to build the test cases.