import subprocess

import pytest


@pytest.mark.skip(
    reason="Temporarily skipping due to persistent modification of .claude files by the environment."
)
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


def test_failing_test_for_clear_error_messages():
    """
    Tests that running a non-existent command produces a clear error message.
    This is a failing test to demonstrate error message clarity.
    """
    non_existent_command = "this_command_does_not_exist_12345"

    result = subprocess.run(
        non_existent_command,  # Pass command as a single string when shell=True
        capture_output=True,
        text=True,
        check=False,  # We expect it to fail, so don't raise an exception
        shell=True,  # Use shell to handle command not found
    )

    # Assert that the command failed
    assert result.returncode != 0, "Non-existent command unexpectedly succeeded."

    # Assert that stderr contains a clear error message about command not found
    # The exact message can vary between systems, so check for common phrases
    error_message_lower = result.stderr.lower()
    assert any(
        phrase in error_message_lower
        for phrase in ["not found", "command not found", "no such file or directory"]
    ), f"Error message is not clear: {result.stderr}"
