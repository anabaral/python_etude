import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import time
import subprocess
import os
from winregistry import WinRegistry
import datetime

class TestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Change ScreenSaver"
    _svc_display_name_ = "Change ScreenSaver"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = False

    def SvcStop(self):
        # Main.exe Process Kill
        #subprocess.Popen("taskkill /im Main.exe /f", shell=True)   # 서비스 중지 시 Main.exe 프로세스 taskkill 명령어로 중지.
        time.sleep(1)
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False # is_running 를 False로 바꿔 줌으로써 Main.exe 주기적 호출 막기
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.is_running = True
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, ("hello", ""))
        #current_location = str(os.path.abspath(os.path.dirname(sys.argv[0])))   # 현재 위치 체크
        while self.is_running: # self.is_running이 True인 경우에만 while 실행
              rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
              if rc == win32event.WAIT_OBJECT_0:
                break
              else:
                #subprocess.Popen([current_location + "\\Main.exe"]) # 현재 경로에 위치한 Main.exe
                # TEST
                #f = open('e:/download/1/a.log', 'a')
                #f.write(datetime.datetime.now().isoformat())
                #f.close()
                reg = WinRegistry()
                path = r'HKCU\Control Panel\Desktop'
                keyvalue = reg.read_key(path)
                for v in keyvalue['values']:
                  if v['value'] == 'SCRNSAVE.EXE':
                    if v['data'] != 'c:\\Windows\\System32\\PhotoScreensaver.scr':
                      reg.delete_value(path, 'SCRNSAVE.EXE')
                      reg.write_value(path, 'SCRNSAVE.EXE', 'c:\\Windows\\System32\\PhotoScreensaver.scr')
              time.sleep(60)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, ("start", ""))
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(TestService)
    servicemanager.StartServiceCtrlDispatcher()
  else:
    win32serviceutil.HandleCommandLine(TestService)

