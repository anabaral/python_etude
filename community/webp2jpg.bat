@echo off
REM set target=%~n1
REM c:\usr\imagemagick\convert.exe  %1 %target%.jpg

REM 사용하기 위해서는 ImageMagick 프로그램이 필요함.

for %%i in ( *.webp ) do @( c:\usr\imagemagick\convert.exe %%i %%i.jpg )

del *.webp

