EXPECTED_SUM = 2


def test_smoke() -> None:
    """A simple smoke test to check if the test suite is running."""
    # This test will always pass, and is used to check if the test suite is running.
    assert 1 + 1 == EXPECTED_SUM  # noqa: SIM300
