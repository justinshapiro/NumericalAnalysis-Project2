from distutils.core import setup
import py2exe
import numpy
from distutils.filelist import findall
import os
import matplotlib
import sys
sys.setrecursionlimit(5000)

matplotlibdatadir = matplotlib.get_data_path()
matplotlibdata = findall(matplotlibdatadir)
matplotlibdata_files = []
for f in matplotlibdata:
    dirname = os.path.join('matplotlibdata', f[len(matplotlibdatadir)+1:])
    matplotlibdata_files.append((os.path.split(dirname)[0], [f]))

setup(
    data_files=matplotlib.get_py2exe_datafiles(),
    options={
        "py2exe": {
        "dll_excludes": ["MSVCP90.dll", "HID.DLL", "w9xpopen.exe"],
        "includes": ['scipy', 'scipy.integrate', 'scipy.special.*','scipy.sparse.csgraph._validation', 'scipy.linalg.*'],
    }
},windows=['Project2_Team23.py'])

#changes4