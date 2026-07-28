@echo off
setlocal enabledelayedexpansion
title Installation Riot Account Manager
color 0B

echo ============================================
echo   Installation de Riot Account Manager
echo ============================================
echo.

REM ------------------------------------------------------------
REM 1. Verifier si Python est REELLEMENT installe
REM    (Windows a un faux "python.exe" qui renvoie vers le
REM    Microsoft Store et fait planter la detection classique
REM    "where python", d'ou la verification du contenu ici)
REM ------------------------------------------------------------
set "PY_FOUND=0"
set "PY_OUTPUT="

for /f "delims=" %%v in ('python --version 2^>^&1') do set "PY_OUTPUT=%%v"
echo !PY_OUTPUT! | findstr /I "Python" >nul
if !errorlevel!==0 (
    set "PY_FOUND=1"
    set "PY_CMD=python"
)

if !PY_FOUND!==0 (
    for /f "delims=" %%v in ('py --version 2^>^&1') do set "PY_OUTPUT=%%v"
    echo !PY_OUTPUT! | findstr /I "Python" >nul
    if !errorlevel!==0 (
        set "PY_FOUND=1"
        set "PY_CMD=py"
    )
)

if !PY_FOUND!==1 (
    echo [OK] Python est deja installe.
    echo       Version detectee : !PY_OUTPUT!
    goto :install_deps
)

echo [INFO] Python n'est pas installe ^(ou seulement le stub Microsoft Store^).
echo        Installation en cours...
echo.

REM ------------------------------------------------------------
REM 2. Essayer d'installer Python via winget
REM ------------------------------------------------------------
where winget >nul 2>nul
if %errorlevel%==0 (
    echo [INFO] Installation de Python via winget...
    winget install --id Python.Python.3.13 -e --silent --accept-package-agreements --accept-source-agreements
    if !errorlevel!==0 (
        echo [OK] Python installe via winget.
        goto :refresh_path
    ) else (
        echo [ATTENTION] winget a echoue, tentative via telechargement direct...
    )
) else (
    echo [INFO] winget non disponible, tentative via telechargement direct...
)

REM ------------------------------------------------------------
REM 3. Fallback : telecharger et installer Python directement
REM ------------------------------------------------------------
set "PY_VERSION=3.13.2"
set "PY_INSTALLER=python-installer.exe"
set "PY_URL=https://www.python.org/ftp/python/%PY_VERSION%/python-%PY_VERSION%-amd64.exe"

echo [INFO] Telechargement de Python %PY_VERSION%...
powershell -Command "Invoke-WebRequest -Uri '%PY_URL%' -OutFile '%TEMP%\%PY_INSTALLER%'"

if not exist "%TEMP%\%PY_INSTALLER%" (
    echo [ERREUR] Le telechargement de Python a echoue.
    echo Verifie ta connexion internet, ou installe Python manuellement depuis python.org
    pause
    exit /b 1
)

echo [INFO] Installation silencieuse de Python...
"%TEMP%\%PY_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_launcher=1

del "%TEMP%\%PY_INSTALLER%"

:refresh_path
REM ------------------------------------------------------------
REM 4. Rafraichir le PATH de la session courante
REM ------------------------------------------------------------
echo [INFO] Rafraichissement du PATH...
for /f "usebackq tokens=2,*" %%A in (`reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path`) do set "SYS_PATH=%%B"
for /f "usebackq tokens=2,*" %%A in (`reg query "HKCU\Environment" /v Path 2^>nul`) do set "USER_PATH=%%B"
set "PATH=%SYS_PATH%;%USER_PATH%"

REM ------------------------------------------------------------
REM 5. Utiliser le lanceur "py" en priorite : il n'est jamais
REM    intercepte par le stub Microsoft Store, contrairement a
REM    "python.exe" qui peut rester ambigu selon l'ordre du PATH
REM ------------------------------------------------------------
set "PY_CMD="
for /f "delims=" %%v in ('py --version 2^>^&1') do set "PY_OUTPUT=%%v"
echo !PY_OUTPUT! | findstr /I "Python" >nul
if !errorlevel!==0 set "PY_CMD=py"

if not defined PY_CMD (
    for /f "delims=" %%v in ('python --version 2^>^&1') do set "PY_OUTPUT=%%v"
    echo !PY_OUTPUT! | findstr /I "Python" >nul
    if !errorlevel!==0 set "PY_CMD=python"
)

if not defined PY_CMD (
    echo [ERREUR] Python ne semble toujours pas accessible apres installation.
    echo Ferme cette fenetre, ouvre un NOUVEAU terminal, et relance ce script.
    echo Si le probleme persiste, verifie Parametres Windows ^> Applications ^>
    echo Alias d'execution des applications, et desactive "python.exe".
    pause
    exit /b 1
)

echo [OK] Python est maintenant installe et accessible via "!PY_CMD!".
echo.

REM ------------------------------------------------------------
REM 6. Installer les dependances Python
REM ------------------------------------------------------------
:install_deps
if not defined PY_CMD set "PY_CMD=python"

echo ============================================
echo   Installation des dependances Python
echo ============================================
echo.

!PY_CMD! -m pip install --upgrade pip

!PY_CMD! -m pip install ^
    customtkinter ^
    opgg.py ^
    requests ^
    pillow ^
    CTkToolTip ^
    pywinstyles ^
    cachetools ^
    pyperclip ^
    pygetwindow ^
    pyautogui ^
    psutil ^
    opencv-python ^
    pywin32

if not !errorlevel!==0 (
    echo.
    echo [ERREUR] Une ou plusieurs dependances n'ont pas pu s'installer.
    echo Verifie le message d'erreur ci-dessus.
    pause
    exit /b 1
)

echo.
echo [INFO] Finalisation de pywin32...
!PY_CMD! -m pywin32_postinstall -install >nul 2>nul

echo.
echo ============================================
echo   Installation terminee avec succes !
echo ============================================
echo.
echo Tu peux maintenant lancer l'application avec :
echo     !PY_CMD! main.py
echo.
pause