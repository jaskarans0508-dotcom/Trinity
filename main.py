"""
Trinity — Main Entry Point
Run this to start the Trinity shell.
"""

import argparse

from core.activation import run_activation
from core.config_loader import load_config
from core.shell import start_shell
from core.status import ProviderStatus


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trinity — Multi-Provider AI Shell")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check local config and key format without calling provider APIs.",
    )
    parser.add_argument(
        "--no-shell",
        action="store_true",
        help="Validate providers only, then exit without starting TrinityFlow.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = run_activation(dry_run=args.dry_run)

    if args.dry_run:
        print("[Trinity] Dry run only. Run without --dry-run to perform live provider validation.\n")
        return

    # Check if any provider is valid before continuing
    active = [p for p, (s, _) in results.items() if s == ProviderStatus.VALID]

    if not active:
        print("[Trinity] No valid providers. Exiting.\n")
        return

    print("[Trinity] Ready. Active providers:", ", ".join(active))

    if args.no_shell:
        print("[Trinity] Provider check complete. Shell skipped because --no-shell was used.\n")
        return

    config = load_config()
    start_shell(config, results)


if __name__ == "__main__":
    main()
