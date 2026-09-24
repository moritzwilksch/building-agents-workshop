"""Fetch the workshop OpenAI API key from the instructor's secret endpoint."""

import getpass
import sys
import urllib.error
import urllib.request

SECRET_NAME = "openai_api_key"
SECRET_URL = f"http://server.m0ritz.de:8000/secret/{SECRET_NAME}"

# The endpoint returns the raw secret on 200 and an error status otherwise.
ERRORS = {
    403: "Wrong password.",
    404: f"The server has no secret named '{SECRET_NAME}'; ask the instructor to check it.",
    422: "The server rejected the request; the password prompt and the endpoint disagree.",
}


def fetch_secret(password: str) -> str:
    """Return the secret for `password`, or raise RuntimeError with a readable reason."""
    request = urllib.request.Request(SECRET_URL, headers={"X-Password": password})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            secret = response.read().decode("utf-8").strip()
        if not secret:
            raise RuntimeError("The server returned an empty secret. Ask the instructor.")
        return secret
    except urllib.error.HTTPError as error:
        reason = ERRORS.get(error.code, f"The server returned HTTP {error.code} {error.reason}.")
        raise RuntimeError(reason) from error
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Could not reach {SECRET_URL} ({error.reason}); check your internet connection."
        ) from error


def main() -> int:
    password = getpass.getpass("Instructor password (input hidden): ").strip()
    try:
        secret = fetch_secret(password)
    except RuntimeError as error:
        print(f"🚫 {error}", file=sys.stderr)
        return 1
    print("✅ Your OpenAI API key:")
    print()
    print(f"    {secret}")
    print()
    print("Keep it private. Paste it into .env as OPENAI_API_KEY, then run `pixi run check-setup`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
