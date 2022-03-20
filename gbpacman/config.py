import json
from os import (makedirs as os_makedirs,
                path as os_path,
                sep as os_sep)
from gbpacman.utils import get_global_logger

logger = get_global_logger()


def load_json(json_file) -> dict:
    with open(json_file, 'r') as file:
        return json.load(file)


def is_key_points_to_path(key: str):
    allowed_suffixes = ["dir", "filename", "filepath", "path", "exe"]
    for suffix in allowed_suffixes:
        if key.endswith(suffix):
            return True
    return False


def patch_paths(dictionary: dict, patches: dict):
    patched_dict = {}
    for key, value in dictionary.items():
        patched_value = None
        if isinstance(value, dict):
            patched_value = patch_paths(value, patches)
        else:
            if is_key_points_to_path(key):
                patched_value = value % patches
                if "." in os_path.basename(patched_value):
                    os_makedirs(os_path.dirname(patched_value),exist_ok=True)
                else:
                    os_makedirs(patched_value,exist_ok=True)
            else:
                patched_value = value
        patched_dict[key] = patched_value
    return patched_dict


class Settings:
    def __init__(self, dictionary: dict):
        self.store = dictionary

        if "BASE_DIR" not in self.store:
            self.store["BASE_DIR"] = os_path.dirname(os_path.abspath(__file__))
        self.patch_values()

    def patch_values(self):
        patches = {
            "BASE_DIR": self.store["BASE_DIR"],
            "SLASH": os_sep
        }
        self.store = patch_paths(self.store, patches)

    @classmethod
    def from_json(cls, json_file):
        store = load_json(json_file)
        return cls(store)

    def is_folder(self, path):
        return os_path.isdir(path)

    def __getitem__(self, key):
        value = self.store.get(key, None)
        if value is None:
            return value
        if key.endswith("_dir"):
            os_makedirs(value, exist_ok=True)
        return value

    def set(self, key, value):
        if key in self.store:
            logger.warning("Overwriting %(key)s in settings with %(value)s" %
                           {"key": key, "value": value})
        self.store[key] = value

    def __str__(self):
        string = ""
        for key, value in self.store.items():
            prefix = key
            orig_key = key
            orig_value = value
            if isinstance(value, dict):
                for k, v in value.items():
                    k = f"{prefix}_{k}"
                    string = f"{string}{k} : {v}\n"
            else:
                string = f"{string}{key} : {value}\n"
        return string

    def __repr__(self):
        print(f"{self.__class__.__name__}()")


curr_dir = os_path.dirname(os_path.abspath(__file__))
settings_file = "settings.json"
settings = Settings.from_json(os_path.join(curr_dir, settings_file))
