@echo off
REM Phase E build script — generates PDF and HTML from source Markdown files.
REM Requires: Node.js (v18+) with npx available.
REM Uses md-to-pdf (https://github.com/simonhaenisch/md-to-pdf) via npx.
REM
REM Usage: double-click this file, or run from terminal:
REM   build_outputs.bat
REM
REM Output goes to build_output/ (gitignored).
REM
REM Publishable files generated:
REM   1. Arduino_PBL_Program.pdf        — the master document (Ministry proposal)
REM   2. Arduino_PBL_Program.html       — HTML version of the master document
REM   3. Arduino_Project_1.pdf          — Project 1 detailed source file
REM   4. Arduino_Project_1.html         — HTML version of Project 1

echo.
echo ============================================================
echo   Phase E Build Pipeline
echo   Generating PDF and HTML from source Markdown files
echo ============================================================
echo.

REM Create output directory
if not exist build_output mkdir build_output

REM --- Master document: Arduino_PBL_Program.md ---
echo [1/4] Generating Arduino_PBL_Program.pdf ...
call npx --yes md-to-pdf --config-file md-to-pdf.config.js Arduino_PBL_Program.md
if errorlevel 1 (
  echo ERROR: Failed to generate Arduino_PBL_Program.pdf
) else (
  move /Y Arduino_PBL_Program.pdf build_output\ >nul
  echo       Done.
)

echo [2/4] Generating Arduino_PBL_Program.html ...
call npx --yes md-to-pdf --config-file md-to-pdf.config.js --as-html Arduino_PBL_Program.md
if errorlevel 1 (
  echo ERROR: Failed to generate Arduino_PBL_Program.html
) else (
  move /Y Arduino_PBL_Program.html build_output\ >nul
  echo       Done.
)

REM --- Project 1 source file: Arduino_Project_1.md ---
echo [3/4] Generating Arduino_Project_1.pdf ...
call npx --yes md-to-pdf --config-file md-to-pdf.config.js "Arduino_Projects\Project_1_Light_Signals\Arduino_Project_1.md"
if errorlevel 1 (
  echo ERROR: Failed to generate Arduino_Project_1.pdf
) else (
  move /Y "Arduino_Projects\Project_1_Light_Signals\Arduino_Project_1.pdf" build_output\ >nul
  echo       Done.
)

echo [4/4] Generating Arduino_Project_1.html ...
call npx --yes md-to-pdf --config-file md-to-pdf.config.js --as-html "Arduino_Projects\Project_1_Light_Signals\Arduino_Project_1.md"
if errorlevel 1 (
  echo ERROR: Failed to generate Arduino_Project_1.html
) else (
  move /Y "Arduino_Projects\Project_1_Light_Signals\Arduino_Project_1.html" build_output\ >nul
  echo       Done.
)

echo.
echo ============================================================
echo   Build complete. Output files in build_output/
echo ============================================================
echo.
dir build_output\*.pdf build_output\*.html 2>nul
echo.
pause
