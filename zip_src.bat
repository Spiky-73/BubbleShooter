@echo off
if exist src rmdir /s /q src
mkdir src
xcopy /i /y /s /q core src\core
xcopy /i /y /s /q etats src\etats
xcopy /i /y /s /q themes src\themes
xcopy /i /y /s /q niveaux src\niveaux
xcopy /i /y /s /q images src\images
xcopy .\*.py src
if exist src\core\__pycache__ rmdir /s /q src\core\__pycache__
if exist src\etats\__pycache__ rmdir /s /q src\etats\__pycache__
if exist src\images\git rmdir /s /q src\images\git
cd src
tar -a -c -f ..\src.zip *
cd  ..
rmdir /s /q src
