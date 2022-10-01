import os.path
import warnings
import win32service

SVC_FILE = os.path.join(os.path.dirname(__file__), "scrt.py")

START_TYPE_MAP = {
    "demand": win32service.SERVICE_DEMAND_START,
    "auto": win32service.SERVICE_AUTO_START,
    "boot": win32service.SERVICE_BOOT_START,
    "disabled": win32service.SERVICE_DISABLED,
    "system": win32service.SERVICE_SYSTEM_START,
}


def add_quote(a):
    return '"{0}"'.format(a)


def get_command_line(py, svc, exe_name, exe_args):
    if " " in exe_name:
        exe_name = add_quote(exe_name)
    cmd = f'{add_quote(py)} {add_quote(svc)} {add_quote(os.getcwd())} {exe_name}'
    if exe_args:
        cmd += f' {" ".join(exe_args)}'
    return cmd


def install_service(service_name, cmd, display_name='', description=None,
                    start_type='demand', error_control=win32service.SERVICE_ERROR_NORMAL,
                    run_interactive=False, service_deps=None, user_name=None, password=None, delayed_start=None,
                    restart=0):
    service_type = win32service.SERVICE_WIN32_OWN_PROCESS
    if run_interactive:
        service_type = service_type | win32service.SERVICE_INTERACTIVE_PROCESS

    scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    try:
        hs = win32service.CreateService(scm, service_name, display_name, win32service.SERVICE_ALL_ACCESS,
                                        service_type, START_TYPE_MAP[start_type], error_control, cmd, None, 0,
                                        service_deps, user_name, password)
        if description is not None:
            try:
                win32service.ChangeServiceConfig2(hs, win32service.SERVICE_CONFIG_DESCRIPTION, description)
            except NotImplementedError:
                pass
        if delayed_start is not None:
            try:
                win32service.ChangeServiceConfig2(hs, win32service.SERVICE_CONFIG_DELAYED_AUTO_START_INFO,
                                                  delayed_start)
            except (win32service.error, NotImplementedError):
                if delayed_start:
                    warnings.warn('Delayed Start not available on this system')
        if restart > 0:
            failure_actions = {
                'ResetPeriod': 86400,
                'RebootMsg': '',
                'Command': '',
                'Actions': [(win32service.SC_ACTION_RESTART, restart * 1000)] * 3
            }
            try:
                win32service.ChangeServiceConfig2(hs, win32service.SERVICE_CONFIG_FAILURE_ACTIONS, failure_actions)
                win32service.ChangeServiceConfig2(hs, win32service.SERVICE_CONFIG_FAILURE_ACTIONS_FLAG, True)
            except win32service.error:
                warnings.warn("fail to set restart actions")
        win32service.CloseServiceHandle(hs)
    finally:
        win32service.CloseServiceHandle(scm)
