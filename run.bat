@echo off
cd /d "%~dp0"

:check_internet
cls
echo Verificando conexao com a internet...
echo ==============================
ping -n 1 8.8.8.8 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Sem conexao com a internet!
    echo Por favor, conecte-se a internet para continuar.
    echo.
    echo Pressione qualquer tecla para tentar novamente...
    pause >nul
    goto check_internet
)
echo Conexao com a internet estabelecida!
echo.

echo Verificando instancias abertas do programa...
echo ==============================
tasklist /FI "IMAGENAME eq YouTubeDownloader.exe" 2>NUL | find /I /N "YouTubeDownloader.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Fechando instancia anterior do programa...
    taskkill /F /IM "YouTubeDownloader.exe" >nul 2>&1
    timeout /t 2 /nobreak >nul
)
echo.

:check_git_updates
echo Verificando atualizacoes do repositorio...
echo ==============================
git pull > git_update_check.txt 2>&1

REM 1. Verifica se o "git pull" falhou
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Ocorreu um erro ao tentar sincronizar com o GitHub.
    echo Detalhes do erro:
    type git_update_check.txt
    del git_update_check.txt
    echo.
    echo Pulando atualizacoes e iniciando a aplicacao...
    timeout /t 3 /nobreak >nul
    goto start_app
)

REM 2. Se teve sucesso, verifica se baixou algo novo
findstr /C:"Already up to date." git_update_check.txt >nul
if %ERRORLEVEL% NEQ 0 (
    echo Atualizacoes encontradas e aplicadas. Reiniciando o script...
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
    --ytvd-folder YTVD ^
    --ytvd-exe YTVD\YouTubeDownloader.exe ^
    --zip-url https://github.com/robsonswe/ytvd/releases/latest/download/YTVD2.zip ^
    --api-url https://api.github.com/repos/robsonswe/ytvd/releases/latest

REM 3. Verifica se o script de atualizacao falhou
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] O script de atualizacao falhou. Verifique os logs acima.
    echo Pulando atualizacao e iniciando a aplicacao...
    timeout /t 3 /nobreak >nul
    goto start_app
)

:start_app
echo.
echo Iniciando a aplicacao...
echo ==============================
cd /d "%~dp0YTVD"
start "" "YouTubeDownloader.exe"