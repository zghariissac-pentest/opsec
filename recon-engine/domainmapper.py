import socket
import json


class DomainMapper:

    def resolve_domain(self, domain):
        """
        Resolves domain to IP address.

        Why this matters:
        Infrastructure mapping helps identify hosting patterns and attack surfaces.
        """

        try:
            ip = socket.gethostbyname(domain)

            return {
                "domain": domain,
                "ip_address": ip,
                "status": "resolved successfully"
            }

        except Exception:
            return {
                "domain": domain,
                "ip_address": None,
                "status": "resolution failed"
            }

    def analyze_basic_risk(self, result):
        """
        Basic interpretation of exposure level
        """

        if result["ip_address"]:
            return "infrastructure visible"
        return "no resolution possible or hidden layer"

    def run(self, domain):
        result = self.resolve_domain(domain)
        risk = self.analyze_basic_risk(result)

        result["risk"] = risk
        return result


if __name__ == "__main__":

    mapper = DomainMapper()

    output = mapper.run("example.com")

    print(json.dumps(output, indent=4))
