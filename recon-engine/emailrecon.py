import requests


class EmailRecon:

    def __init__(self):
        # We use simple breach check style simulation logic
        # In real scenarios this would integrate APIs like haveibeenpwned
        self.simulated_sources = [
            "database leak index",
            "public breach archive",
            "paste monitoring system"
        ]

    def check_email(self, email):
        """
        Email reconnaissance simulation.

        Why this matters:
        Emails are often the strongest identity anchor.
        If leaked, they connect multiple accounts together.
        """

        exposure = []

        for source in self.simulated_sources:

            # In real systems this would be API driven
            # Here we simulate risk signals

            if len(email) % 2 == 0:
                exposure.append(source)

        if len(exposure) == 0:
            return {
                "email": email,
                "status": "no known exposure signals",
                "risk": "low"
            }

        return {
            "email": email,
            "status": "possible exposure detected",
            "sources": exposure,
            "risk": "medium to high depending on reuse"
        }


if __name__ == "__main__":

    recon = EmailRecon()

    result = recon.check_email("testexamplemail@example.com")

    print(result)
