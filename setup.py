#coding=utf-8 #
# mysetup.py
from distutils.core import setup
import py2exe
import matplotlib

setup(windows=["main.py"],options = { "py2exe":{"dll_excludes":["MSVCP90.dll"]}},data_files=matplotlib.get_py2exe_datafiles(),)




