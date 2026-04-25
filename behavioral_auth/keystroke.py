import time
import statistics

class KeystrokeAuth:

    def __init__(self):
        self.patterns = {}

    # =========================
    # CAPTURE TIMINGS
    # =========================
    def capture_pattern(self, text):
        print(f"Type this text: {text}")

        timings = []
        last_time = None

        for char in text:
            input(f"Press '{char}' and ENTER")

            now = time.time()

            if last_time is not None:
                timings.append(now - last_time)

            last_time = now

        return timings  

    # =========================
    # TRAIN
    # =========================
    def train(self, username, text, samples=3):
        collected = []

        print("\n=== TRAINING KEYSTROKE ===")

        for i in range(samples):
            print(f"Sample {i+1}")
            pattern = self.capture_pattern(text)

            if len(pattern) > 0:
                collected.append(pattern)

        if not collected:
            print("Training failed!")
            return

        avg_pattern = [
            statistics.mean(values)
            for values in zip(*collected)
        ]

        self.patterns[username] = avg_pattern

        print("Training completed!")

    # =========================
    # VERIFY
    # =========================
    def verify(self, username, text):
        print("\n=== VERIFY KEYSTROKE ===")

        new_pattern = self.capture_pattern(text)
        stored = self.patterns.get(username)

        if not stored:
            return False

        min_len = min(len(stored), len(new_pattern))

        diffs = [
            abs(stored[i] - new_pattern[i])
            for i in range(min_len)
        ]

        score = sum(diffs)

        print("Difference score:", score)

        return score < 5
    
