import random
import json
import string
import time


class PersonaGenerator:

    def __init__(self):
        self.codename_pool = [
            "atlas", "nova", "cipher", "echo", "nyx",
            "vanta", "orbit", "phantom", "lumen", "drift"
        ]

        self.risk_levels = [
            "minimal exposure",
            "moderate exposure",
            "isolated environment",
            "high isolation mode"
        ]

        self.context_roles = [
            "research analyst",
            "security tester",
            "data observer",
            "system evaluator",
            "network inspector"
        ]

    def generate_seed(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

    def generate_codename(self):
        base = random.choice(self.codename_pool)
        suffix = str(random.randint(10, 99))
        return base + suffix

    def generate_timestamp(self):
        return int(time.time())

    def create_persona(self):
        persona = {
            "codename": self.generate_codename(),
            "role": random.choice(self.context_roles),
            "risk_profile": random.choice(self.risk_levels),
            "session_seed": self.generate_seed(),
            "created_at": self.generate_timestamp(),
            "operational_rule": "no identity overlap between sessions",
            "separation_status": "active isolation enforced"
        }
        return persona

    def export_persona(self, persona, filename):
        with open(filename, "w") as file:
            json.dump(persona, file, indent=4)


if __name__ == "__main__":
    generator = PersonaGenerator()

    persona = generator.create_persona()
    print(json.dumps(persona, indent=4))

    generator.export_persona(persona, "persona_output.json")
