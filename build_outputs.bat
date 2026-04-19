@echo off
REM Phase E build script — generates PDF, HTML, and DOCX from source Markdown files.
REM
REM Requires:
REM   - Node.js v18+ with npx (for md-to-pdf, PDF and HTML generation)
REM   - Pandoc v3+ (for DOCX generation) — typical path:
REM     %LOCALAPPDATA%\Pandoc\pandoc.exe
REM
REM Usage: double-click this file, or run from terminal:
REM   build_outputs.bat
REM
REM Output goes to build_output/ (gitignored).
REM
REM Publishable files generated:
REM   English:
REM     Arduino_PBL_Program.pdf / .html       — master document (Ministry proposal)
REM     Arduino_PBL_Program_Overview.pdf / .html / .docx — 10-page executive overview
REM     Arduino_Project_1.pdf / .html         — Project 1 detailed source file
REM   Hebrew (RTL):
REM     Arduino_PBL_Program_Overview_he.pdf / .docx — Hebrew overview

set PANDOC=%LOCALAPPDATA%\Pandoc\pandoc.exe

echo.
echo ============================================================
echo   Phase E Build Pipeline
echo   Generating PDF, HTML, and DOCX from source Markdown files
echo ============================================================
echo.

if not exist build_output mkdir build_output

REM --- Master document: Arduino_PBL_Program.md ---
echo [1/9] Generating Arduino_PBL_Program.pdf ...
call npx --yes md-to-pdf --config-file md-to-pdf.config.js Arduino_PBL_Program.md >nul 2>&1
if errorlevel 1 ( echo ERROR ) else ( move /Y Arduino_PBL_Program.pdf build_output\ >nul & echo       Done. )

echo [2/9] Generating Arduino_PBL_Program.html ...
call npx --yes md-to-pdf --config-file md-to-pdf.config.js --as-html Arduino_PBL_Program.md >nul 2>&1
if errorlevel 1 ( echo ERROR ) else ( move /Y Arduino_PBL_Program.html build_output\ >nul & echo       Done. )

REM --- English overview: Arduino_PBL_Program_Overview.md ---
echo [3/9] Generating Arduino_PBL_Program_Overview.pdf ...
call npx --yes md-to-pdf --config-file md-to-pdf.config.js Arduino_PBL_Program_Overview.md >nul 2>&1
if errorlevel 1 ( echo ERROR ) else ( move /Y Arduino_PBL_Program_Overview.pdf build_output\ >nul & echo       Done. )

echo [4/9] Generating Arduino_PBL_Program_Overview.html ...
call npx --yes md-to-pdf --config-file md-to-pdf.config.js --as-html Arduino_PBL_Program_Overview.md >nul 2>&1
if errorlevel 1 ( echo ERROR ) else ( move /Y Arduino_PBL_Program_Overview.html build_output\ >nul & echo       Done. )

echo [5/9] Generating Arduino_PBL_Program_Overview.docx ...
"%PANDOC%" Arduino_PBL_Program_Overview.md -o build_output\Arduino_PBL_Program_Overview.docx --from markdown --to docx
if errorlevel 1 ( echo ERROR - is pandoc installed? ) else ( echo       Done. )

REM --- Hebrew overview: Arduino_PBL_Program_Overview_he.md ---
echo [6/9] Generating Arduino_PBL_Program_Overview_he.pdf (RTL) ...
call npx --yes md-to-pdf --config-file md-to-pdf-he.config.js Arduino_PBL_Program_Overview_he.md >nul 2>&1
if errorlevel 1 ( echo ERROR ) else ( move /Y Arduino_PBL_Program_Overview_he.pdf build_output\ >nul & echo       Done. )

echo [7/9] Generating Arduino_PBL_Program_Overview_he.docx (RTL) ...
"%PANDOC%" Arduino_PBL_Program_Overview_he.md -o build_output\Arduino_PBL_Program_Overview_he.docx --from markdown --to docx --metadata=dir:rtl --metadata=lang:he
if errorlevel 1 ( echo ERROR - is pandoc installed? ) else ( echo       Done. )

REM --- Project 1 source file: Arduino_Project_1.md ---
echo [8/9] Generating Arduino_Project_1.pdf ...
call npx --yes md-to-pdf --config-file md-to-pdf.config.js "Arduino_Projects\Project_1_Light_Signals\Arduino_Project_1.md" >nul 2>&1
if errorlevel 1 ( echo ERROR ) else ( move /Y "Arduino_Projects\Project_1_Light_Signals\Arduino_Project_1.pdf" build_output\ >nul & echo       Done. )

echo [9/10] Generating Arduino_Project_1.html ...
call npx --yes md-to-pdf --config-file md-to-pdf.config.js --as-html "Arduino_Projects\Project_1_Light_Signals\Arduino_Project_1.md" >nul 2>&1
if errorlevel 1 ( echo ERROR ) else ( move /Y "Arduino_Projects\Project_1_Light_Signals\Arduino_Project_1.html" build_output\ >nul & echo       Done. )

REM --- Cards-only bundle (Hebrew): Project_1_Cards_he.html + .pdf ---
echo [10/10] Generating Project_1_Cards_he.html + .pdf (standalone cards bundle) ...
call node build_cards_only.js he >nul 2>&1
if errorlevel 1 ( echo ERROR ) else ( echo       Done. )

echo.
echo ============================================================
echo   Build complete. Output files in build_output/
echo ============================================================
echo.
dir build_output\*.pdf build_output\*.html build_output\*.docx 2>nul
echo.
pause
