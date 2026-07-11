@echo off
set "PYTHONPATH=%~dp0src"
py -m cddex.cli %*

