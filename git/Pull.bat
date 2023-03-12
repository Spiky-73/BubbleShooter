@echo off
git add .
git commit -a -m %message%
git push
echo Pulled all changes from remote
timeout /t -1