import json
import typing
from pathlib import Path


class DictConfig(dict):
    def __init__(self, conf_path: (Path, str),
                 default_config: dict,
                 quiet: bool = False,
                 save_indent: int = 4):

        super(DictConfig, self).__init__()
        self.conf_path = Path(conf_path)
        self.save_indent = save_indent

        if data := self.load():
            self.update(data)
        else:
            if not quiet:
                print(f'[!] Recreated fresh config in: "{conf_path}"')
            self.update(default_config)
            self.save()

    def load(self) -> (typing.Dict[str, str], bool):
        try:
            with self.conf_path.open() as f:
                return json.load(f)
        except FileNotFoundError:
            return False
        except json.JSONDecodeError:
            return False

    def save(self) -> None:
        with self.conf_path.open('w') as f:
            json.dump(self, f, indent=self.save_indent)
