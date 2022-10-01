# Easy Deployment

Easy deployment tool for Python application. Deploy your application with one command that triggers two steps:

- Create a virtual environment (Optional).
- Install your application as a service.

## Install

Download and install the `ezd` package for Python.

```
pip install ezd
```

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
    "program": "",
    "args": [],
    "display": "",
    "description": ""
  }
}
```

A list of full parameters:

| Parameter           | Type         | Description                                                                  | Windows            | Linux              |
|---------------------|--------------|------------------------------------------------------------------------------|--------------------|--------------------|
| env.name            | string       | The name of virtual environment.                                             | :heavy_check_mark: | :heavy_check_mark: |
| env.lookup          | string       | Offline package lookup directory used by pip.                                | :heavy_check_mark: | :heavy_check_mark: |
| env.local           | string       | A directory contains local package file.                                     | :heavy_check_mark: | :heavy_check_mark: |
| env.requirement     | bool         | Whether to install dependencies in `requirements.txt`. Default is `true`.    | :heavy_check_mark: | :heavy_check_mark: |
| service.name        | string       | The name of service.                                                         | :heavy_check_mark: | :heavy_check_mark: |
| service.program     | string       | Executable file of service.                                                  | :heavy_check_mark: | :heavy_check_mark: |
| service.args        | list[string] | Arguments to be passed to executable.                                        | :heavy_check_mark: | :heavy_check_mark: |
| service.display     | string       | Display name of service.                                                     | :heavy_check_mark: | :x:                |
| service.description | string       | Description of service.                                                      | :heavy_check_mark: | :heavy_check_mark: |
| service.start       | string       | Start type of service (demand/auto/boot/disabled/system). Default is `auto`. | :heavy_check_mark: | :heavy_check_mark: |
| service.restart     | int          | Restart delay (seconds) when service failed. Default is `30`.                | :heavy_check_mark: | :heavy_check_mark: |
| service.deps        | list[string] | Dependencies of service.                                                     | :heavy_check_mark: | :heavy_check_mark: |
| service.interactive | bool         | Run service in interactive mode. Default is `false`.                         | :heavy_check_mark: | :x:                |
| service.user        | string       | Run service with given user.                                                 | :heavy_check_mark: | :heavy_check_mark: |
| service.password    | string       | Password of the user.                                                        | :heavy_check_mark: | :x:                |
| service.delayed     | bool         | Delayed start of service.                                                    | :heavy_check_mark: | :x:                |

### Commands

Run `ezd -h` to see all commands.

```
usage: ezd [-h] command

Easy Deployment Tool

positional arguments:
  command     Command <init|deploy|install|uninstall|start|stop>

optional arguments:
  -h, --help  show this help message and exit
```

Available commands:

| Command   | Description                                                   |
|-----------|---------------------------------------------------------------|
| init      | Create an example config file `deploy.json`.                  |
| deploy    | Create virtual environment and install dependencies.          |
| install   | Install a service (Automatically run `deploy` command first). |
| uninstall | Remove service.                                               |
| start     | Start service.                                                |
| stop      | Stop service.                                                 |

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
    "program": "jupyter-notebook",
    "args": [],
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
    "program": "ping",
    "args": [
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
