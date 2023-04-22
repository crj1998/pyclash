import json

from .utils import get_file_path


def write_config(cfg, output):
    with open(get_file_path("config.json"), "r") as f:
        template = json.load(f)

    template["remote_addr"] = cfg["server"]
    template["remote_port"] = cfg["port"]
    template["password"][0] = cfg["password"]
    template["ssl"]["sni"] = cfg["sni"]

    with open(output, "w") as f:
        json.dump(template, f, ensure_ascii=True, indent=4)





