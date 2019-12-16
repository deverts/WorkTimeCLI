from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class AsanaCredentials:
    token: str
    user_id: str
    workspace_id: str
    time_taken_field_id: str


APP_NAME = ".worktimecli"
TASK_DB_NAME = "task_db.json"
ASANA_CREDENTIAL_FILE_NAME = "asana.json"

APP_HOME = Path.home().joinpath(APP_NAME)

LOCAL_DB_PATH = str(APP_HOME.joinpath(TASK_DB_NAME))
ASANA_CREDENTIAL_PATH = str(APP_HOME.joinpath(ASANA_CREDENTIAL_FILE_NAME))

if not APP_HOME.exists():
    APP_HOME.mkdir()

with open(ASANA_CREDENTIAL_PATH, "r") as f:
    asana_conf = json.load(f)

    ASANA_CREDENTIALS = AsanaCredentials(
        asana_conf.get("token"),
        asana_conf.get("user_id"),
        asana_conf.get("workspace_id"),
        asana_conf.get("time_taken_field_id"),
    )
