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

    def __init__(self, args):
        MainService._svc_name_ = args[0]
        self._svc_wd_ = win32serviceutil.GetServiceCustomOption(self, "AppDirectory")
        if self._svc_wd_:
            os.chdir(self._svc_wd_)
        app_env = win32serviceutil.GetServiceCustomOption(self, "AppEnvironment")
        if app_env:
            os.environ["PATH"] = app_env + os.pathsep + os.environ["PATH"]
        win32serviceutil.ServiceFramework.__init__(self, args)

    def SvcDoRun(self):
        MainService.proc = subprocess.Popen(sys.argv[1:])
        ret = MainService.proc.wait()
        assert MainService.request_stop or ret == 0

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        MainService.request_stop = True
        MainService.proc.terminate()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(MainService)
    servicemanager.StartServiceCtrlDispatcher()
