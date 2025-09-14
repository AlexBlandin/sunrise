@echo off
setlocal
set t=2&if "%date%z" LSS "A" set t=1
for /f "skip=1 tokens=2-4 delims=(-)" %%A in ('echo/^|date') do (
  for /f "tokens=%t%-4 delims=.-/ " %%J in ('date/t') do (
    set %%A=%%J&set %%B=%%K&set %%C=%%L)
)
set sunrisecache="%USERPROFILE%\.cache\sunrise"
if not exist %sunrisecache% (
  mkdir %sunrisecache%
)
set today="%sunrisecache%\%yy%-%mm%-%dd%.txt"
if not exist %today% (
  for %%x in ("%sunrisecache%\*.txt") do del %%x
  @call uv run -qqs sunrise.py %* > %today%
  type %today%
) else (
  type %today%
)
endlocal
