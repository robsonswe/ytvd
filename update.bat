@echo off
cd /d "%~dp0"

set YTVD_FOLDER=YTVD2
set VERSION_FILE=%YTVD_FOLDER%\version.txt
set DOWNLOAD_ZIP=YTVD2.zip
set GITHUB_API_URL=https://api.github.com/repos/robsonswe/ytvd/releases/latest

if not exist "%YTVD_FOLDER%" (
    echo Diretorio YTVD2 nao encontrado. Baixando a versao mais recente...
    curl -L -o "%DOWNLOAD_ZIP%" https://github.com/robsonswe/ytvd/releases/latest/download/YTVD2.zip
    powershell -Command "Expand-Archive -Path '%DOWNLOAD_ZIP%' -DestinationPath '%YTVD_FOLDER%' -Force"
    del "%DOWNLOAD_ZIP%"
    
    curl -s %GITHUB_API_URL% > latest_release.json
    for /f "delims=" %%i in ('powershell -command "(Get-Content latest_release.json | ConvertFrom-Json).tag_name"') do set REMOTE_VERSION=%%i
    del latest_release.json
    echo %REMOTE_VERSION% > "%VERSION_FILE%"
    echo Versao inicial instalada: %REMOTE_VERSION%
) else (
    set /p LOCAL_VERSION=<"%VERSION_FILE%"
    curl -s %GITHUB_API_URL% > latest_release.json
    for /f "delims=" %%i in ('powershell -command "(Get-Content latest_release.json | ConvertFrom-Json).tag_name"') do set REMOTE_VERSION=%%i
    del latest_release.json
    
    echo Versao local: %LOCAL_VERSION%
    echo Versao remota: %REMOTE_VERSION%
    
    if "%LOCAL_VERSION%"=="%REMOTE_VERSION%" (
        echo Nenhuma atualizacao disponivel.
    ) else (
        echo Atualizacao encontrada! Baixando os arquivos...
        curl -L -o "%DOWNLOAD_ZIP%" https://github.com/robsonswe/ytvd/releases/latest/download/YTVD2.zip
        powershell -Command "Expand-Archive -Path '%DOWNLOAD_ZIP%' -DestinationPath '%YTVD_FOLDER%' -Force"
        del "%DOWNLOAD_ZIP%"
        echo %REMOTE_VERSION% > "%VERSION_FILE%"
        echo Atualizacao concluida!
    )
)

echo Iniciando a aplicacao...
call run.bat