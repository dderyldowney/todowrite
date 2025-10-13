import argparse
import re
from collections import defaultdict


def parse_ruff_output(ruff_output_path: str, error_codes: list[str]) -> dict[str, list[str]]:
    file_errors = defaultdict(list)
    with open(ruff_output_path) as f:
        lines = f.readlines()

    current_error_line = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if it's an error line (e.g., "D104 Missing docstring in public package")
        # and if it matches one of the target error codes
        match = re.match(r"([A-Z]{1,3}\d{3,4}) (.*)", line)
        if match:
            error_code = match.group(1)
            if error_code in error_codes:
                current_error_line = line
            else:
                current_error_line = None  # Reset if not a target error
            continue

        # Check if it's a file path line (e.g., "--> bin/__init__.py:1:1")
        if line.startswith("--> ") and current_error_line:
            file_path_match = re.match(r"--> (.*?):\d+:\d+", line)
            if file_path_match:
                file_path = file_path_match.group(1)
                file_errors[file_path].append(current_error_line)
            current_error_line = None  # Reset after processing file path
            continue

        # If it's a context line (like the code snippet), reset current_error_line
        if current_error_line and (line.startswith(" |") or line.startswith("  |")):
            current_error_line = None

    return file_errors


def main():
    parser = argparse.ArgumentParser(description="Parse ruff output for specific error codes.")
    parser.add_argument("ruff_output_path", type=str, help="Path to the ruff output file.")
    parser.add_argument(
        "error_codes", nargs="+", help="List of ruff error codes to filter by (e.g., D100 D104)."
    )
    args = parser.parse_args()

    errors = parse_ruff_output(args.ruff_output_path, args.error_codes)

    for file_path, error_list in errors.items():
        print(f"--- {file_path} ---")
        for error in error_list:
            print(error)
        print()


if __name__ == "__main__":
    main()
