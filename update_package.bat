@echo off

REM Navigate to your package directory
REM cd path\to\your\package

REM Optional: Uninstall the existing package version
pip uninstall GuiFramework -y

REM Build a new wheel file
python setup.py sdist bdist_wheel

REM Find the latest wheel file in the dist directory and store it in a variable
FOR /F "delims=" %%i IN ('dir /b /o-d /t:c dist\*.whl') DO SET "new_wheel=%%i" & GOTO :install

:install
REM Install the new wheel file
pip install dist\%new_wheel% --force-reinstall

pause