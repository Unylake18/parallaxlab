@echo off
setlocal
set "BLENDER=%BLENDER_EXE%"
if "%BLENDER%"=="" set "BLENDER=C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
if not exist "%BLENDER%" (
  echo Blender nao encontrado em %BLENDER%
  echo Defina a variavel BLENDER_EXE com o caminho do blender.exe
  pause
  exit /b 1
)
start "" "%BLENDER%" -P "%~dp0..\abrir_no_blender.py" -- superficie_parametrizada
