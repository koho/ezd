import os
import subprocess
import sys
import servicemanager
import win32service
import win32serviceutil


class MainService(win32serviceutil.ServiceFramework):
    _svc_name_ = ""
    proc = None
    request_stop = False

    def SvcDoRun(self):
        os.chdir(sys.argv[1])
        os.environ["PATH"] += os.pathsep + os.path.dirname(__file__)
        self.__class__.proc = subprocess.Popen(sys.argv[2:])
        ret = self.__class__.proc.wait()
        assert self.__class__.request_stop or ret == 0

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.__class__.request_stop = True
        self.__class__.proc.terminate()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(MainService)
    servicemanager.StartServiceCtrlDispatcher()
