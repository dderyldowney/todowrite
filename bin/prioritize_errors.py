
import re
from collections import Counter
import os

LOG_FILE = "logs/static_analysis.log"
ERROR_PATTERN = re.compile(r"^([A-Z]+\d+)\s")

def prioritize_errors():
    if not os.path.exists(LOG_FILE):
        print(f"Log file '{LOG_FILE}' not found.")
        return

    with open(LOG_FILE, "r") as f:
        content = f.readlines()

    errors = []
    for line in content:
        match = ERROR_PATTERN.match(line)
        if match:
            errors.append(match.group(1))

    error_counts = Counter(errors)

    if not error_counts:
        print("No errors found in the log file.")
        return

    print("Prioritized list of errors:")
    for error, count in error_counts.most_common():
        print(f"- {error}: {count} occurrences")

if __name__ == "__main__":
    prioritize_errors()
