import json
import os
import uuid
import datetime


class AliasManager:

    def __init__(self, storage_file):
        self.storage_file = storage_file
        self.aliases = self.load_aliases()

    def load_aliases(self):
        if not os.path.exists(self.storage_file):
            return {}
        with open(self.storage_file, "r") as file:
            return json.load(file)

    def save_aliases(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.aliases, file, indent=4)

    def create_alias(self, label, context):
        alias_id = str(uuid.uuid4())

        self.aliases[alias_id] = {
            "label": label,
            "context": context,
            "created": str(datetime.datetime.utcnow()),
            "status": "active"
        }

        self.save_aliases()
        return alias_id

    def get_alias(self, alias_id):
        return self.aliases.get(alias_id, None)

    def list_aliases(self):
        return self.aliases

    def deactivate_alias(self, alias_id):
        if alias_id in self.aliases:
            self.aliases[alias_id]["status"] = "inactive"
            self.save_aliases()
            return True
        return False


if __name__ == "__main__":
    manager = AliasManager("aliases.json")

    new_id = manager.create_alias(
        "research persona",
        "isolated environment for OSINT analysis"
    )

    print("Created alias id")
    print(new_id)
    print(manager.get_alias(new_id))
