import os
import sys
from cx_Freeze import setup, Executable

sys.setrecursionlimit(3000)  # Increase the recursion limit to 3000
sys.path.append("src")


# base directory where the script and other files are located
base_directory = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(base_directory, "src", "guis", "TipOutApp.py")
icon_path = os.path.join(base_directory, "output.icns")

# this will include the figs folder, hopefully! 
include_files = ["figs/", 'figs/']

build_exe_options = {
    "packages": ["csv", "datetime", "smtplib", "ssl", "certifi", "pandas", "numpy", "reportlab", "email", "tkinter"],
    "include_files" : include_files
}

setup(
    name = "TipOutCalc",
    version = "0.1",
    description = "This application will manage an employee database, compute nightly tip-outs, generate reports, and distribute emails.",
    executables = [Executable(script_path, icon=icon_path)],
    options = {"build_exe": build_exe_options}
)





