from pathlib import Path


class StorageService:
    def __init__(self, base_path: str = "storage"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_file(
        self,
        contents: bytes,
        filename: str,
        issue_id: int,
    ) -> str:
        issue_directory = self.base_path / f"issue_{issue_id}"
        issue_directory.mkdir(parents=True, exist_ok=True)

        file_path = issue_directory / filename
        file_path.write_bytes(contents)

        return str(file_path)