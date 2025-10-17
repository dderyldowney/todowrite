import subprocess
import time


def test_git_working_directory_cleanliness():
    """
    Tests that the git working directory is clean (no uncommitted changes).
    This test assumes it runs in a context where the working directory should be clean.

    Uses retry logic to handle timing issues during large test suite execution
    where temporary files may not be cleaned up immediately.
    """
    # Common temporary files that might appear during test execution
    # These are typically cleaned up quickly and shouldn't block release
    temp_file_patterns = [
        ".pytest_cache/",
        "__pycache__/",
        ".coverage",
        ".mypy_cache/",
        "*.pyc",
        "*.pyo",
        ".DS_Store",
        "*.tmp",
    ]

    def filter_temp_files(file_list: str) -> str:
        """Filter out known temporary files that don't affect release readiness."""
        if not file_list.strip():
            return file_list

        lines = file_list.strip().split('\n')
        filtered_lines = []

        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

            # Check if this line matches any temporary file pattern
            is_temp = False
            for pattern in temp_file_patterns:
                if pattern in line or line.endswith(pattern.replace('*', '')):
                    is_temp = True
                    break

            if not is_temp:
                filtered_lines.append(line)

        return '\n'.join(filtered_lines)

    # Retry logic to handle timing issues during test execution
    max_retries = 3
    retry_delay = 0.5  # seconds

    for attempt in range(max_retries):
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Filter out temporary files from git status
        filtered_status = filter_temp_files(result.stdout)

        # Check for untracked files
        result_untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Filter out temporary files from untracked files
        filtered_untracked = filter_temp_files(result_untracked.stdout)

        # If both filtered results are clean, test passes
        if not filtered_status.strip() and not filtered_untracked.strip():
            return

        # If this is not the last attempt, wait and retry
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
            continue

        # Final attempt failed - provide detailed error message
        error_parts = []
        if filtered_status.strip():
            error_parts.append(f"Uncommitted changes:\n{filtered_status}")
        if filtered_untracked.strip():
            error_parts.append(f"Untracked files:\n{filtered_untracked}")

        # Also show what was filtered out for debugging
        original_status = result.stdout.strip()
        original_untracked = result_untracked.stdout.strip()
        if original_status != filtered_status.strip() or original_untracked != filtered_untracked.strip():
            error_parts.append("\nFiltered out temporary files:")
            if original_status != filtered_status.strip():
                temp_status = '\n'.join(line for line in original_status.split('\n')
                                      if line not in filtered_status.split('\n') and line.strip())
                if temp_status:
                    error_parts.append(f"  Temp status files: {temp_status}")
            if original_untracked != filtered_untracked.strip():
                temp_untracked = '\n'.join(line for line in original_untracked.split('\n')
                                         if line not in filtered_untracked.split('\n') and line.strip())
                if temp_untracked:
                    error_parts.append(f"  Temp untracked files: {temp_untracked}")

        error_message = f"Git working directory is not clean after {max_retries} attempts:\n" + '\n'.join(error_parts)
        raise AssertionError(error_message)


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
