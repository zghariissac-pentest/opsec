import hashlib
import random


class FingerprintAnalyzer:

    def __init__(self):
        self.weights = {
            "browser_uniqueness": 30,
            "behavior_consistency": 25,
            "network_repetition": 20,
            "metadata_leakage": 25
        }

    def simulate_signal(self):
        return {
            "browser_uniqueness": random.randint(0, 100),
            "behavior_consistency": random.randint(0, 100),
            "network_repetition": random.randint(0, 100),
            "metadata_leakage": random.randint(0, 100)
        }

    def calculate_score(self, signals):
        score = 100

        for key, value in signals.items():
            penalty = (value / 100) * self.weights[key]
            score -= penalty

        return round(score, 2)

    def risk_level(self, score):
        if score > 80:
            return "low traceability"
        elif score > 50:
            return "moderate traceability"
        else:
            return "high traceability risk"

    def hash_identity(self, data):
        return hashlib.sha256(str(data).encode()).hexdigest()


if __name__ == "__main__":
    analyzer = FingerprintAnalyzer()

    signals = analyzer.simulate_signal()
    score = analyzer.calculate_score(signals)

    print("Signals")
    print(signals)

    print("Score")
    print(score)

    print("Risk")
    print(analyzer.risk_level(score))
