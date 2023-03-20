@echo off
cd %~dp0
echo Pulling all commits
git pull
echo Pulled all new commits from remote
timeout /t -1