@echo off
cd /d "%~dp0"
python deploy.py > deploy_log.txt 2>&1
