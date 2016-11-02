import sys
import os
from cx_Freeze import setup, Executable, hooks

def load_win32clipboard(finder, module):
    finder.IncludeModule("pywintypes")
    
#os.environ['TCL_LIBRARY']="C:\\Users\\DS_THE_DRAGON\\AppData\\Local\\Programs\\Python\\Python35\\tcl\\tcl8.6"
#os.environ['TK_LIBRARY']="C:\\Users\\DS_THE_DRAGON\\AppData\\Local\\Programs\\Python\\Python35\\tcl\\tk8.6"
build_exe_options = {"packages": ["os", "sys", "datetime", "sqlite3",  "shutil",  "random", "functools", "string"],
                     "includes":["PyQt5"],
                     "excludes": ["PyQt5.uic", "tkinter"],
                     "include_files": ["data/"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
setup(  name = "Staff-DATA",
        version = "0.1",
        description = "This is a staff monitoring app design by RMCO to store staff data and activity.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("index.py", base=base)])