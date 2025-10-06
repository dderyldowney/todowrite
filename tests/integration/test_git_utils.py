import subprocess


def test_git_working_directory_cleanliness():
    """
    Tests that the git working directory is clean (no uncommitted changes).
    This test assumes it runs in a context where the working directory should be clean.
    """
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,  # Don't raise an exception for non-zero exit code, we want to check output
    )

    # If there's any output, the working directory is not clean
    assert result.stdout == "", f"Git working directory is not clean:\n{result.stdout}"

    # Also check for untracked files
    result_untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert (
        result_untracked.stdout == ""
    ), f"Untracked files found in working directory:\n{result_untracked.stdout}"


def test_compatible_with_various_shell_environments():
    """
    Tests that basic shell commands are compatible with various shell environments.
    """
    shells = ["bash", "zsh", "sh"]
    command_to_test = "echo 'Hello from shell'"

    for shell in shells:
        try:
            # Check if the shell executable exists
            subprocess.run([shell, "-c", ""], check=True, capture_output=True)
        except FileNotFoundError:
            print(f"Skipping test for {shell} as it is not found.", flush=True)
            continue
        except subprocess.CalledProcessError:
            # Shell exists but might have issues with empty command, continue
            pass

        print(f"Testing with shell: {shell}", flush=True)
        result = subprocess.run(
            [shell, "-c", command_to_test],
            capture_output=True,
            text=True,
            check=True,  # Raise an exception if the command fails
        )
        assert (
            result.stdout.strip() == "Hello from shell"
        ), f"Unexpected output from {shell}: {result.stdout}"
        assert result.stderr == "", f"Errors from {shell}: {result.stderr}"
