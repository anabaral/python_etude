@echo off
REM 임시로 받았던 그림파일들 지우는 명령. 
REM Windows Command로는 표현에 한계가 있어 linux 명령으로 지움.
wsl rm [0-9][0-9]*.jpg [0-9][0-9]-*.jpg [0-9][0-9].gif [0-9][0-9]-*.gif [0-9][0-9].png [0-9][0-9]-*.png [0-9][0-9].mp4  2>nul
