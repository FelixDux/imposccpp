from pathlib import Path

from file_makers import unique_file_name, files_size

class LibErrors:

    def __init__(self, _directory: str = "errors"):
        errors_path = Path(_directory).absolute()

        if not errors_path.exists():
            errors_path.mkdir()

        self._log = errors_path / unique_file_name("txt")

    @property
    def errorFile(self):
        return str(self._log)

    @property
    def errorPath(self):
        return self._log

    def read(self):
        if self._log.exists():
            return self._log.read_text()
        else:
            return ""

    def put(self, message):
        with self._log.open(mode='a') as stream:
            stream.writelines([message])