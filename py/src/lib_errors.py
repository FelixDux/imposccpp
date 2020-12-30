from pathlib import Path

from file_makers import unique_file_name, files_size

class LibErrors:
    """ Maintains a per-session log of error messages """

    def __init__(self, directory: str = "errors"):
        """

        Keyword arguments:

        directory -- the name of a directory to store error logs in (default 'errors')
        """
        errors_path = Path(directory).absolute()

        if not errors_path.exists():
            errors_path.mkdir()

        self._log = errors_path / unique_file_name("txt")

    @property
    def errorFile(self) -> str:
        return str(self._log)

    @property
    def errorPath(self) -> Path:
        return self._log

    def read(self) -> str:
        """ Returns the contents of the error log """
        if self._log.exists():
            return self._log.read_text()
        else:
            return ""

    def put(self, message):
        """ Logs an error message """
        with self._log.open(mode='a') as stream:
            stream.write(f"{message}\n")