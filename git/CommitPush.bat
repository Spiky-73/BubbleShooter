@echo off
set /p "message=Enter commit message: "
git add .
git commit -a -m %message%
git push
echo Pushed all changes to remote
timeout /t -1