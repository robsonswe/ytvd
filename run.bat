@echo off
cd /d "%~dp0"

:check_git_updates
echo Verificando atualizacoes do repositorio...
echo ==============================
git pull > git_update_check.txt 2>&1
findstr /C:"Already up to date." git_update_check.txt >nul
if %ERRORLEVEL% NEQ 0 (
    echo Atualizacoes encontradas no repositorio Git. Reiniciando o script...
    del git_update_check.txt
    timeout /t 2 /nobreak >nul
    start "" "%~f0"
    exit
)
del git_update_check.txt
echo Repositorio ja esta atualizado.
echo.

echo Executando script de atualizacao...
update-tool.exe ^
    --ytvd-folder YTVD2 ^
    --version-file version.txt ^
    --zip-url https://github.com/robsonswe/ytvd/releases/latest/download/YTVD2.zip ^
    --github-api-url https://api.github.com/repos/robsonswe/ytvd/releases/latest
if %ERRORLEVEL% NEQ 0 (
    echo Erro: O script de atualizacao falhou. Verifique os logs acima.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Iniciando a aplicacao...
echo ==============================
cd /d "%~dp0\YTVD2"
start "" "YouTubeDownloader.exe"