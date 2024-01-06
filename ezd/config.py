import json

# Default config file
CONFIG_FILE = "deploy.json"

TEMPLATE = """{
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
"""


class Config:
    @classmethod
    def load(cls, values: dict):
        for k, v in values.items():
            setattr(cls, k, v)


class Env(Config):
    name: str = ""
    lookup: str = ""
    local: str = ""
    requirement: bool = True


class Service(Config):
    name: str = ""
    cmd: list = []
    display: str = ""
    description: str = None
    start: str = "auto"
    restart: int = 30
    restart_policy: str = "on-failure"
    runtime_max_sec: int = 0
    deps: list = None
    interactive: bool = False
    user: str = None
    password: str = None
    delayed: bool = None


def load_config():
    with open(CONFIG_FILE, encoding='utf8') as f:
        config = json.load(f)
        Env.load(config.get("env", {}))
        Service.load(config.get("service", {}))


def write_template():
    with open(CONFIG_FILE, "w", encoding="utf8") as f:
        f.write(TEMPLATE)
