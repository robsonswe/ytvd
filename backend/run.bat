@echo off
cd /d "%~dp0"
cd ..
echo ==============================
echo Buscando atualizacoes na aplicacao...
echo ==============================
git pull
echo.

cd "%~dp0"
echo ==============================
echo  Verificando ambiente virtual...
echo ==============================
echo.

if not exist "venv" (
    echo Ambiente virtual nao encontrado. Criando um novo...
    python -m venv venv
)

echo ==============================
echo  Ativando ambiente virtual...
echo ==============================
echo.

call venv\Scripts\activate.bat

echo ==============================
echo  Atualizando yt-dlp...
echo ==============================
echo.

pip install yt-dlp -U

echo.
echo ==============================
echo  Iniciando a aplicacao...
echo ==============================
echo.

python app.py
pause
