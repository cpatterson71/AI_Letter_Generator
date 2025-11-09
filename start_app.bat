@echo off
echo Starting AI Letter Generator...
cd /d "%~dp0"
call .venv\Scripts\activate
echo.
echo Your app is running at the URL below.
echo Open the URL in your web browser.
echo.
streamlit run app.py
pause