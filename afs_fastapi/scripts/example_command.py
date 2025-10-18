import sys


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "fail":
        print("ERROR: This is a simulated failure with a clear message.", file=sys.stderr)
        sys.exit(1)
    print("Command executed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
