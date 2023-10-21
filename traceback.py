import linecache
import traceback
import sys

def get_current_line_using_linecache(file_path):
    current_line = linecache.getline(file_path, sys._getframe().f_lineno)
    print("Using linecache.getline():", current_line, "Line No:", sys._getframe().f_lineno)

def get_current_line_using_file_object(file_path):
    with open(file_path, 'r') as f:
        current_line = None
        for i, line in enumerate(f):
            if i + 1 == sys._getframe().f_lineno:
                current_line = line
                break
    print("Using file.tell():", current_line, "Line No:", sys._getframe().f_lineno)

def get_current_line_using_traceback(file_path):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    current_line = traceback.extract_tb(exc_traceback)[-1][1]
    print("Using traceback.extract_tb():", current_line, "Line No:", sys._getframe().f_lineno)

if __name__ == "__main__":
    file_path = "example.txt"
    get_current_line_using_linecache(file_path)
    get_current_line_using_file_object(file_path)
    get_current_line_using_traceback(file_path)
