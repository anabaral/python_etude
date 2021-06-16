@echo off
REM 사용하기 위해서는 ImageMagick 프로그램이 필요함.
REM 오유(todayhumor.com)는 그림파일이 너무 크면 까맣게 되면서 제대로 올라기지 못하는 경우가 있음. 이를 커버하기 위해 만든 툴.
REM 가로로는 넉넉하게 4000, 세로로는 적당히 6000 (이게 7000~8000대 넘어갈 때 문제 발생) 정도에서 끊는데
REM 단점은 그림이 아무데서나 잘림...

c:\usr\ImageMagick\convert.exe -crop 4000x6000 %1 %1
