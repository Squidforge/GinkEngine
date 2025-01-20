@echo off
cd Core\WPy64-31280\python\
python.exe ..\..\Scripts\log.py log_startup
python.exe ..\..\Scripts\main.py
python.exe ..\..\Scripts\log.py log_exit