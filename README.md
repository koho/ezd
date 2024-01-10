# Easy Deployment

Easy deployment tool for Python application. There are mainly two parts:

- Create a virtual environment (Optional).
- Install your application as a service.

Deploy your application with one command!

## Install

It's recommended that you install this package in the **Global Python Environment**.

```
pip install ezd
```

On Windows, be careful if you want to uninstall this package. Make sure all services created with this tool are removed.

## Usage

### Config file

Run `ezd init` to create a config file named `deploy.json`.

```json
{
  "env": {
    "name": "venv"
  },
  "service": {
    "name": "",
    "cmd": [],
    "display": "",
    "description": ""
  }
}
```

A list of full parameters:

| Parameter                 | Type         | Description                                                                                        | Windows            | Linux              |
|---------------------------|--------------|----------------------------------------------------------------------------------------------------|--------------------|--------------------|
| env.name                  | string       | The name of virtual environment.                                                                   | :heavy_check_mark: | :heavy_check_mark: |
| env.lookup                | string       | Offline package lookup directory used by pip.                                                      | :heavy_check_mark: | :heavy_check_mark: |
| env.local                 | string       | A directory contains local package file.                                                           | :heavy_check_mark: | :heavy_check_mark: |
| env.requirement           | bool         | Whether to install dependencies in `requirements.txt`. Default is `true`.                          | :heavy_check_mark: | :heavy_check_mark: |
| service.name              | string       | The name of service.                                                                               | :heavy_check_mark: | :heavy_check_mark: |
| service.cmd               | list[string] | The command line to be executed.                                                                   | :heavy_check_mark: | :heavy_check_mark: |
| service.display           | string       | Display name of service.                                                                           | :heavy_check_mark: | :x:                |
| service.description       | string       | Description of service.                                                                            | :heavy_check_mark: | :heavy_check_mark: |
| service.start             | string       | Start type of service (demand/auto/boot/disabled/system). Default is `auto`.                       | :heavy_check_mark: | :heavy_check_mark: |
| service.restart           | int          | Restart delay (seconds) when service failed. Default is `30`.                                      | :heavy_check_mark: | :heavy_check_mark: |
| service.restart_policy    | string       | Configures whether the service shall be restarted when the service exits. Default is `on-failure`. | :x:                | :heavy_check_mark: |
| service.runtime_max_sec   | int          | Configures a maximum time for the service to run. Default is `0`.                                  | :x:                | :heavy_check_mark: |
| service.working_directory | string       | Configures the working directory of the service. Default is `.`.                                   | :heavy_check_mark: | :heavy_check_mark: |
| service.deps              | list[string] | Dependencies of service.                                                                           | :heavy_check_mark: | :heavy_check_mark: |
| service.interactive       | bool         | Run service in interactive mode. Default is `false`.                                               | :heavy_check_mark: | :x:                |
| service.user              | string       | Run service with given user.                                                                       | :heavy_check_mark: | :heavy_check_mark: |
| service.password          | string       | Password of the user.                                                                              | :heavy_check_mark: | :x:                |
| service.delayed           | bool         | Delayed start of service.                                                                          | :heavy_check_mark: | :x:                |

### Commands

Run `ezd -h` to see all commands.

```
usage: ezd [-h] command

Easy Deployment Tool

positional arguments:
  command          Command <init|deploy|install|uninstall|start|stop>

options:
  -h, --help       show this help message and exit
  --config CONFIG  config file
```

Available commands:

| Command   | Description                                                   |
|-----------|---------------------------------------------------------------|
| init      | Create an example config file `deploy.json`.                  |
| deploy    | Create virtual environment and install dependencies.          |
| install   | Install a service (Automatically run `deploy` command first). |
| uninstall | Remove service (Automatically run `stop` command first).      |
| start     | Start service.                                                |
| stop      | Stop service.                                                 |

### Update config

#### Upgrade or install packages

If you need to upgrade or install packages, just edit the `requirements.txt` file and follow the steps below:

1. Stop the service

    ```shell
    ezd stop
    ```

2. Deploy new packages

    ```shell
    ezd deploy
    ```

3. Start the service

    ```shell
    ezd start
    ```

#### Update service

If you update the service settings of the config file, you must `uninstall` the old service first.

1. Uninstall the service

    ```shell
    ezd uninstall
    ```

2. Install service

    ```shell
    ezd install
    ```

3. Start the service

    ```shell
    ezd start
    ```

## Examples

### Jupyter notebook

Create a new `nb` directory and start working in it.

```shell
cd nb
echo notebook > requirements.txt
ezd init
```

The `deploy.json` file looks like this:

```json
{
  "env": {
    "name": "venv"
  },
  "service": {
    "name": "notebook",
    "cmd": [
      "jupyter-notebook.exe"
    ],
    "display": "Jupyter Notebook",
    "description": "Jupyter Notebook Service"
  }
}
```

We are ready to deploy now.

```shell
ezd install
ezd start
```

You can now visit http://localhost:8888/ to confirm jupyter notebook is running.

### Ping test

Create a new `pingtest` directory and start working in it.

```shell
cd pingtest
ezd init
```

For non-python project, we can omit virtual environment since we don't need it. The `deploy.json` file looks like this:

```json
{
  "service": {
    "name": "pingtest",
    "cmd": [
      "ping",
      "-t",
      "1.1.1.1"
    ],
    "display": "Ping it",
    "description": "A ping test service"
  }
}
```

Deploy now!

```shell
ezd install
ezd start
```

Let's confirm ping is running:

```shell
$ tasklist | findstr PING
PING.EXE                     19564 Services                   0      4,540 K
```
