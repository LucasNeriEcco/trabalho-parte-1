@echo off
cd /d "%~dp0.."
pip install -r back-end\requirements.txt
python banco-dados\criar_banco.py
pause
