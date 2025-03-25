@echo off
cd /d "%~dp0"

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

echo ==============================
echo Iniciando a aplicacao...
echo ==============================
cd /d "%~dp0\YTVD2"
start "" "YouTubeDownloader.exe"