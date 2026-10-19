"""Tiny isolated v4.14 ADS GitHub integration smoke; no runtime dependencies."""


def greeting(name: str) -> str:
    """Produce a deterministic greeting for a nonblank recipient."""
    if not isinstance(name, str):
        raise TypeError("name must be str")
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name must not be blank")
    return f"Hello, {cleaned}!"


def _test() -> None:
    assert greeting(" Alice ") == "Hello, Alice!"
    assert greeting("世界") == "Hello, 世界!"
    try:
        greeting(" ")
    except ValueError:
        pass
    else:
        raise AssertionError("blank input should be refused")


if __name__ == "__main__":
    _test()
    print("v4.14 smoke: 3 cases passed")
