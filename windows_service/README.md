# 단순한 윈도우즈 서비스를 파이썬으로 만들어 보기.


아직 잘 모르는게 많아서 일단 적어두고 나중에 정리해 보자..

참고 사이트: https://nick2ya.tistory.com/16

준비:
```
> python -m pip install --upgrade pip
> pip install winregistry

```

만든 프로그램: ![](./WindowsService_ChangeScr.py)

실행파일 만들기:
```
> pip install pyinstaller
> pyinstaller -F --hidden-import=win32timezone -n ChgScrSav.exe WindowsService_ChangeScr.py
```

그냥 실행파일을 만든 정도가 아니라 윈도우즈 서비스로 등록하는 프로그램을 만든 거임.

```
> dir dist\ChgScrSav.exe
> dist\ChgScrSav.exe --startup=auto install
Installing service Change ScreenSaver
Service installed
> sc query "Change ScreenSaver"
...
```

나중에 지울 때는 위의 배포 프로그램을 사용. (없어도 지울 수 있긴 한데)
```
> dist\ChgScrSav.exe remove
```
