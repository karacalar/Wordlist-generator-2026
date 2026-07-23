@echo off
py -3.12 -m pip install -r requirements.txt
py -3.12 -m PyInstaller combination_studio.spec
