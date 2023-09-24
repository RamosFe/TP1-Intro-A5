import os
import math
from alive_progress import alive_bar


class FileSystemUploader:
    def __init__(self, chunk_size: int):
        self._chunk_size = chunk_size

    def get_file_size(self, path: str) -> int:
        return os.path.getsize(path)

    def upload_file(self, sender, addr, path: str, name: str, verbose: bool):
        # TODO Handle Errors
        with open(path, "rb") as file:
            steps = math.ceil(self.get_file_size(path) / self._chunk_size)
            if verbose:
                print(f"-> Uploading file {name}")

            with alive_bar(steps, bar="bubbles", title=f"↑ {name}") as bar:
                for chunk in iter(lambda: file.read(self._chunk_size), b""):
                    sender.sendto(chunk, addr)
                    bar()

            bar.text("✔ Done ✔")
