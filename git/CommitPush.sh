echo Adding all changes
git add -A
echo Creating commit
set /p "message=Enter commit message: "
git commit -a -m "%message%"
echo Pushing
git push
echo Pushed all changes to remote