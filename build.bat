@echo off
call python gen.py %1
call zip_tests.bat %1