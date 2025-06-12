@echo off
REM filepath: c:\Users\a.zuev\PythonProjects\kmo.api\run_app.cmd

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application (example for uvicorn)
uvicorn servio.main:app --reload

REM Pause to keep the window open after execution
pause
