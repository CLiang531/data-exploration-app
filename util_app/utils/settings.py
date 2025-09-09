import os

import yaml
from dotenv import load_dotenv


class Settings:
    def __init__(self, env_path, yaml_path):
        self.settings = None
        self.load_files(env_path, yaml_path)

    def load_files(self, env_path, yaml_path):
        with open(yaml_path, "r") as file:
            config = yaml.safe_load(file)
        load_dotenv(env_path)
        self.settings = {
            "sql": {
                "enabled": config["sql"]["enabled"],
                "dbname": os.getenv("SQL_DBNAME"),
                "user": os.getenv("SQL_USER"),
                "password": os.getenv("SQL_PASSWORD"),
                "host": os.getenv("SQL_HOST"),
                "port": int(os.getenv("SQL_PORT", 5432)),
            }
        }
        for section in config:
            if section != "sql":
                self.settings[section] = config[section]

    def get_section(self, section):
        try:
            if self.settings is None:
                self.load_files()
            return self.settings[section]
        except:
            return None

    def disable(self, section):
        self.settings[section]["enabled"] = False


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
yaml_path = os.path.join(project_root, "config.yaml")
env_path = os.path.join(project_root, ".env")
settings = Settings(env_path, yaml_path)
