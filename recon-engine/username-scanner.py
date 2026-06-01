import requests
import json


class UsernameScanner:

    def __init__(self):
        # We define target platforms where usernames are commonly reused
        self.targets = [
            "https://github.com/{}",
            "https://reddit.com/user/{}",
            "https://instagram.com/{}",
            "https://twitter.com/{}"
        ]

    def scan(self, username):
        """
        This function checks username presence across multiple platforms.

        Why it matters:
        Attackers and analysts often correlate identities using reused usernames.
        """

        found = []
        missing = []

        for url in self.targets:

            target = url.format(username)

            try:
                response = requests.get(target, timeout=5)

                if response.status_code == 200:
                    found.append(target)
                else:
                    missing.append(target)

            except Exception:
                missing.append(target)

        return {
            "username": username,
            "found_profiles": found,
            "missing_profiles": missing,
            "summary": "reuse of usernames increases traceability risk"
        }


if __name__ == "__main__":

    scanner = UsernameScanner()

    result = scanner.scan("exampleuser")

    print(json.dumps(result, indent=4))
