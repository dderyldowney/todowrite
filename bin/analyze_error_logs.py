
import os

LOG_DIR = "logs/collected_logs"
ERROR_KEYWORDS = ["error", "exception", "failed"]

def analyze_logs():
    found_errors = False
    if not os.path.exists(LOG_DIR):
        print(f"Log directory '{LOG_DIR}' not found.")
        return

    for filename in os.listdir(LOG_DIR):
        if filename.endswith(".log"):
            filepath = os.path.join(LOG_DIR, filename)
            with open(filepath) as f:
                for i, line in enumerate(f):
                    for keyword in ERROR_KEYWORDS:
                        if keyword in line.lower():
                            print(f"Potential error in {filepath} at line {i+1}: {line.strip()}")
                            found_errors = True
    
    if not found_errors:
        print("No errors found in the logs.")

if __name__ == "__main__":
    analyze_logs()
