"""Compatibility entry point for users who run: python main.py."""
try:
    import chess  # noqa: F401
    import pygame  # noqa: F401
except ModuleNotFoundError as exc:
    missing = exc.name or "a required package"
    print(f"Missing dependency: {missing}")
    print("Install project dependencies with: python -m pip install -r requirements.txt")
    raise SystemExit(1)

try:
    from Main import main
except Exception as exc:
    print(f"Could not load the chess application: {exc}")
    raise

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Chess AI stopped: {type(exc).__name__}: {exc}")
        print("Run this command from the project folder: python main.py")
        raise
