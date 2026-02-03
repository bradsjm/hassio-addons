#!/usr/bin/env python3
import argparse
import base64
import secrets


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a 32-byte base64 pre-shared key for ESPHome/HA transport encryption.",
    )
    parser.add_argument(
        "--yaml",
        action="store_true",
        help="Print as an ESPHome YAML snippet (api.encryption.key).",
    )
    args = parser.parse_args()

    key_bytes = secrets.token_bytes(32)
    key_b64 = base64.b64encode(key_bytes).decode("ascii")

    if args.yaml:
        print("api:")
        print("  encryption:")
        print(f"    key: \"{key_b64}\"")
    else:
        print(key_b64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

