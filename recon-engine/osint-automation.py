import requests
import json
import time


class OsintAutomation:

    def __init__(self):
        # Basic sources used for footprint checks
        # These are public endpoints that respond with profile existence signals
        self.platforms = {
            "github": "https://github.com/{username}",
            "twitter": "https://twitter.com/{username}",
            "instagram": "https://www.instagram.com/{username}"
        }

    def check_username_existence(self, username):
        """
        This function checks if a username exists on multiple platforms.

        Why this matters:
        If the same username appears on multiple platforms,
        it can be used to link identities together.
        """

        results = {}

        for platform, url in self.platforms.items():

            target_url = url.format(username=username)

            try:
                response = requests.get(target_url, timeout=5)

                # Status code 200 usually means account exists
                if response.status_code == 200:
                    results[platform] = "exists"
                else:
                    results[platform] = "not found or private"

            except Exception:
                # If request fails, we treat it as unknown state
                results[platform] = "error or blocked request"

            time.sleep(1)  # small delay to avoid aggressive requests

        return results

    def analyze_risk(self, results):
        """
        Simple risk scoring based on how many platforms expose the same identity
        """

        score = 0

        for platform, status in results.items():
            if status == "exists":
                score += 1

        if score == 0:
            return "low exposure"
        elif score <= 2:
            return "medium exposure"
        else:
            return "high exposure risk (identity linkable)"

    def run_scan(self, username):
        """
        Full scan pipeline:
        1 check username presence
        2 evaluate exposure risk
        3 return structured report
        """

        print("starting recon scan for username")

        results = self.check_username_existence(username)
        risk = self.analyze_risk(results)

        report = {
            "username": username,
            "platform_results": results,
            "risk_level": risk,
            "timestamp": time.ctime()
        }

        return report


if __name__ == "__main__":

    scanner = OsintAutomation()

    # example target username
    username = "testuser"

    report = scanner.run_scan(username)

    print(json.dumps(report, indent=4))
