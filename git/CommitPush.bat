@echo off
cd %~dp0
set /p "message=Enter commit message: "
git add -A
git commit -a -m "%message%"
git push
timeout /t -1