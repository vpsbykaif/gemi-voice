from uuid import uuid4

class TmpFileService:
    file_registry: dict[str, str] = {}

    def add_path(self, path: str):
        uuid = str(uuid4())
        self.file_registry[uuid] = path
        return uuid

    def remove_path(self, uuid: str):
        if uuid in self.file_registry:
            return self.file_registry.pop(uuid)

    def get_path(self, uuid: str):
        if uuid not in self.file_registry:
            return self.file_registry[uuid]