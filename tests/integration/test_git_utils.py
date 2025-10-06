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
