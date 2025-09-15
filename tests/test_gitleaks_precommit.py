from pathlib import Path

import pytest

from test_example import copy_project, make_venv

# --- Stable patterns gitleaks flags out-of-the-box (should FAIL) ---
STABLE_LEAK_CASES = [
    ("github_token.txt", "ghp_1234567890abcdefghijklmnopqrstuvwx12AB"),
    (
        "slack_webhook.txt",
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
    ),
    ("stripe_secret.txt", "sk_test_4eC39HqLyjWDarjtT1zdp7dcFAKE"),
]


@pytest.mark.parametrize("fname, content", STABLE_LEAK_CASES)
def test_gitleaks_stable_patterns_fail(tmp_path: Path, fname: str, content: str):
    """
    Generate a project, add a known-leaky pattern, stage it,
    and verify tox -e pre-commit (gitleaks) fails.
    """
    copy_project(tmp_path)
    run = make_venv(tmp_path)

    (tmp_path / fname).write_text(content)
    run("git add -A")  # pre-commit's gitleaks scans the staged index

    with pytest.raises(AssertionError, match=r"(?i)(leak|gitleaks|secret)"):
        run("./venv/bin/tox -e pre-commit")


# --- Sealed-secrets: YAML/YML allowlisted; non-YAML should be flagged ---
def _fake_sealed_secret_blob(n: int = 800, seed: str = "sealed-secrets-test") -> str:
    """
    Generate a deterministic, base64-looking ciphertext that resembles a SealedSecret.
    - Always starts with 'Ag'
    - Uses a realistic base64 alphabet mix (via sha256-derived bytes)
    - Adds '=' padding only if required by base64 length
    - Deterministic for stable tests (change `seed` to vary appearance)
    """
    import base64
    import hashlib

    # Build a deterministic byte stream from the seed, not random
    chunk = hashlib.sha256(seed.encode("utf-8")).digest()  # 32 bytes
    raw = (chunk * ((n // len(chunk)) + 4))[: n + 64]  # extra slack, then trim

    # Base64-encode -> realistic distribution of A–Z a–z 0–9 + /
    b64 = base64.b64encode(raw).decode("ascii")

    # Compose with 'Ag' prefix and keep length near n
    body = b64.replace("=", "")  # remove padding from the body
    s = "Ag" + body[:n]  # ensure 'Ag' at start

    # Fix padding so total length is a multiple of 4 (valid base64-looking)
    rem = len(s) % 4
    if rem:
        s += "=" * (4 - rem)
    return s


def test_gitleaks_yaml_allowlist_for_sealed_secrets_yaml(tmp_path: Path):
    """
    Case 1: .yaml (allowlisted => PASS)
    """
    blob = _fake_sealed_secret_blob()

    sealed_yaml = f"""\
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: demo
  namespace: default
spec:
  encryptedData:
    token: "{blob}"
"""

    proj_yaml = tmp_path / "proj_yaml"
    proj_yaml.mkdir()
    copy_project(proj_yaml)
    run_yaml = make_venv(proj_yaml)
    (proj_yaml / "secret.yaml").write_text(sealed_yaml)
    run_yaml("git add -A")
    run_yaml("./venv/bin/tox -e pre-commit")


def test_gitleaks_yaml_allowlist_for_sealed_secrets_yml(tmp_path: Path):
    """
    Case 2: .yml (allowlisted => PASS)
    """
    blob = _fake_sealed_secret_blob()

    sealed_yaml = f"""\
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: demo
  namespace: default
spec:
  encryptedData:
    token: "{blob}"
"""

    proj_yml = tmp_path / "proj_yml"
    proj_yml.mkdir()
    copy_project(proj_yml)
    run_yml = make_venv(proj_yml)
    (proj_yml / "secret.yml").write_text(sealed_yaml)
    run_yml("git add -A")
    run_yml("./venv/bin/tox -e pre-commit")


def test_leaky_code_fails_gitleaks(tmp_path: Path):
    """
    Case 3: non-YAML (should be flagged => FAIL)
    """
    blob = _fake_sealed_secret_blob()

    proj_code = tmp_path / "proj_code"
    proj_code.mkdir()
    copy_project(proj_code)
    run_code = make_venv(proj_code)
    (proj_code / "leaky.py").write_text(f'api_key = "{blob}"\n')
    run_code("git add -A")
    with pytest.raises(AssertionError, match=r"(?i)(leak|gitleaks|secret)"):
        run_code("./venv/bin/tox -e pre-commit")
