@echo off
rem Baut PokerGrid.exe mit dem C#-Compiler, der bei Windows 10 bereits dabei ist (.NET Framework 4.x).
setlocal
cd /d "%~dp0"

set "CSC=%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
if not exist "%CSC%" set "CSC=%WINDIR%\Microsoft.NET\Framework\v4.0.30319\csc.exe"
if not exist "%CSC%" (
    echo csc.exe nicht gefunden - ist das .NET Framework 4.x installiert?
    exit /b 1
)

if not exist dist mkdir dist
"%CSC%" /nologo /target:winexe /optimize+ /codepage:65001 ^
    /out:dist\PokerGrid.exe ^
    /r:System.dll /r:System.Core.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll ^
    src\*.cs
if errorlevel 1 (
    echo.
    echo Build fehlgeschlagen.
    exit /b 1
)
echo.
echo Fertig: dist\PokerGrid.exe
