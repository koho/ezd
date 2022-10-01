import argparse
import configparser
import os
import shutil
import subprocess
import sys
import venv

from ezd.config import Env, Service, CONFIG_FILE, write_template, load_config

IS_WIN = sys.platform == "win32"


def print_error(*args, **kwargs):
    print("Error:", *args, file=sys.stderr, **kwargs)


def ensure_service():
    if not Service.name:
        print_error("The service name is not provided.")
        sys.exit(1)


def install_windows():
    from ezd import winsvc
    if Env.name != "":
        bin_dir = os.path.abspath(os.path.join(Env.name, 'Scripts'))
        cmd = winsvc.get_command_line(os.path.join(bin_dir, "python.exe"),
                                      os.path.join(bin_dir, os.path.basename(winsvc.SVC_FILE)),
                                      Service.program, Service.args)
    else:
        cmd = winsvc.get_command_line(sys.executable, winsvc.SVC_FILE, Service.program, Service.args)
    winsvc.install_service(Service.name, cmd, Service.display, Service.description, Service.start,
                           run_interactive=Service.interactive, service_deps=Service.deps,
                           user_name=Service.user, password=Service.password, delayed_start=Service.delayed,
                           restart=Service.restart)


def install_linux():
    unit_options = {"Description": Service.description}
    if Service.deps:
        unit_options["After"] = " ".join(Service.deps)

    def locate_executable(prog):
        if os.path.isfile(prog):
            return prog
        if Env.name != "":
            bin_dir = os.path.join(Env.name, 'bin')
            script_files = [s for s in os.listdir(bin_dir) if os.path.isfile(os.path.join(bin_dir, s))]
            if prog in script_files:
                return os.path.join(bin_dir, prog)
        return prog

    service_options = {"ExecStart": locate_executable(Service.program), "WorkingDirectory": os.getcwd()}
    if Service.user:
        service_options["User"] = Service.user
    if Service.restart > 0:
        service_options["Restart"] = "on-failure"
        service_options["RestartSec"] = f"{Service.restart}s"
    if Service.args:
        service_options["ExecStart"] += ' ' + ' '.join(Service.args)

    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser["Unit"] = unit_options
    parser["Service"] = service_options
    parser["Install"] = {"WantedBy": "multi-user.target"}
    with open(f'/etc/systemd/system/{Service.name}.service', 'w') as f:
        parser.write(f)
    if Service.start == 'auto':
        os.system(f'systemctl enable {Service.name}')


def install():
    ensure_service()
    if not Service.program:
        print_error("The executable file of the service is not provided.")
        sys.exit(1)
    if Env.name:
        deploy()
    if IS_WIN:
        install_windows()
    else:
        install_linux()


def uninstall():
    ensure_service()
    if IS_WIN:
        import win32serviceutil
        win32serviceutil.RemoveService(Service.name)
    else:
        os.system(f'systemctl stop {Service.name}')
        os.system(f'systemctl disable {Service.name}')
        os.system(f'rm /etc/systemd/system/{Service.name}')
        os.system(f'systemctl daemon-reload')
        os.system(f'systemctl reset-failed')


def start():
    ensure_service()
    if IS_WIN:
        import win32serviceutil
        win32serviceutil.StartService(Service.name)
    else:
        os.system(f'systemctl start {Service.name}')


def stop():
    ensure_service()
    if IS_WIN:
        import win32serviceutil
        win32serviceutil.StopService(Service.name)
    else:
        os.system(f'systemctl stop {Service.name}')


def deploy():
    if not Env.name:
        print_error("The virtual environment name is not provided.")
        sys.exit(1)
    create_env(Env.name)
    if IS_WIN:
        bin_dir = os.path.join(Env.name, 'Scripts')
        pip_bin = 'pip.exe'
    else:
        bin_dir = os.path.join(Env.name, 'bin')
        pip_bin = 'pip'
    pip_path = os.path.join(bin_dir, pip_bin)
    if Env.requirement and os.path.exists('requirements.txt'):
        args = [pip_path, 'install', '-r', 'requirements.txt']
        if Env.lookup:
            args.extend(['--no-index', '--find-links', Env.lookup])
        subprocess.check_call(args, shell=False)
    if Env.local:
        for f in os.listdir(Env.local):
            path = os.path.join(Env.local, f)
            if os.path.isfile(path):
                args = [pip_path, 'install', path]
                if Env.lookup:
                    args.extend(['--no-index', '--find-links', Env.lookup])
                subprocess.check_call(args, shell=False)
    # Install service script into virtual environment
    if IS_WIN:
        from ezd import winsvc
        shutil.copy(winsvc.SVC_FILE, bin_dir)


def create_env(path):
    if not os.path.exists(path):
        print(f"Creating virtual environment '{path}'...")
        if os.name == 'nt':
            use_symlinks = False
        else:
            use_symlinks = True
        venv.create(path, symlinks=use_symlinks, with_pip=True)


def main():
    parser = argparse.ArgumentParser(description='Easy Deployment Tool', add_help=True)
    parser.add_argument('command', help='Command <init|deploy|install|uninstall|start|stop>')
    options = parser.parse_args()
    has_config = os.path.exists(CONFIG_FILE)
    if options.command == "init":
        if not has_config:
            write_template()
        return
    elif not has_config:
        print_error(
            "Unable to locate config file. Perhaps you need to create a new config.\n       Run `ezd init` "
            "to create.")
        sys.exit(1)

    load_config()

    action_map = {
        'deploy': deploy,
        'start': start,
        'stop': stop,
        'install': install,
        'uninstall': uninstall,
    }
    if options.command in action_map:
        action_map[options.command]()
    else:
        print_error(f'Unknown command \'{options.command}\'.')


if __name__ == '__main__':
    main()
