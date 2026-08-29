"""Command line interface.

Run ``earlywarn --help`` for the commands, or ``python -m earlywarn`` if the
package is on the path but the console script is not installed.
"""

import argparse
import sys
from pathlib import Path

from earlywarn import __version__, paths
from earlywarn.catalog import CATALOG, by_idea, ideas, validate
from earlywarn.export import export_catalog
from earlywarn.fetch import fetch_catalog
from earlywarn.page import build_page

STATUS_LABELS = {
    "fetched": "fetched ",
    "failed": "FAILED  ",
    "skipped": "skipped ",
    "planned": "would fetch",
}


def cmd_list(args: argparse.Namespace) -> int:
    """Print the catalog as a summary table.

    Args:
        args: Parsed arguments.

    Returns:
        int: Exit status.
    """
    sources = by_idea(args.idea)
    if args.access:
        sources = [s for s in sources if s.access_class == args.access]

    width = max((len(s.dataset_id) for s in sources), default=0)
    for source in sources:
        coverage = f"{source.coverage_start or '?'}-{source.coverage_end}"
        print(f"{source.dataset_id:<{width}}  {source.access_class:<6}  "
              f"{coverage:<14}  {source.dataset_name}")

    counts = {}
    for source in sources:
        counts[source.access_class] = counts.get(source.access_class, 0) + 1
    summary = ", ".join(f"{count} {name}" for name, count in sorted(counts.items()))
    print(f"\n{len(sources)} of {len(CATALOG)} sources" + (f" ({summary})" if summary else ""))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Check the catalog for structural mistakes.

    Args:
        args: Parsed arguments.

    Returns:
        int: 0 when the catalog is sound, 1 otherwise.
    """
    problems = validate()
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f"\n{len(problems)} problem(s) found", file=sys.stderr)
        return 1
    print(f"{len(CATALOG)} sources across {len(ideas())} ideas: no problems")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    """Write the catalog to CSV and JSON.

    Args:
        args: Parsed arguments.

    Returns:
        int: Exit status.
    """
    for path in export_catalog(args.data_dir):
        print(f"wrote {path}")
    return 0


def cmd_page(args: argparse.Namespace) -> int:
    """Render the catalog page.

    Args:
        args: Parsed arguments.

    Returns:
        int: Exit status.
    """
    page_path = build_page(args.data_dir, fragment_path=args.fragment)
    print(f"wrote {page_path}")
    if args.fragment:
        print(f"wrote {args.fragment}")
    print(f"open it with: python -m webbrowser {page_path}")
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    """Download the sources that can be fetched unattended.

    Args:
        args: Parsed arguments.

    Returns:
        int: 0 unless every attempted download failed.
    """
    outcomes = fetch_catalog(idea=args.idea, dry_run=args.dry_run, data_dir=args.data_dir)
    width = max((len(o.source.dataset_id) for o in outcomes), default=0)

    for outcome in outcomes:
        label = STATUS_LABELS[outcome.status]
        detail = outcome.detail
        if outcome.status == "skipped":
            detail = f"manual step: {detail}"
        stream = sys.stderr if outcome.status == "failed" else sys.stdout
        print(f"{label} {outcome.source.dataset_id:<{width}}  {detail}", file=stream)

    attempted = [o for o in outcomes if o.status in ("fetched", "failed")]
    failed = [o for o in attempted if o.status == "failed"]
    if attempted:
        print(f"\n{len(attempted) - len(failed)} of {len(attempted)} downloads succeeded")
    return 1 if attempted and len(failed) == len(attempted) else 0


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser.

    Returns:
        argparse.ArgumentParser: The configured parser.
    """
    parser = argparse.ArgumentParser(
        prog="earlywarn",
        description="Catalog of open data sources for early-warning apps in Bangladesh.",
    )
    parser.add_argument("--version", action="version", version=f"earlywarn {__version__}")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=paths.DEFAULT_DATA_DIR,
        help="directory the generated files live in (default: ./data)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="print the catalog as a table")
    list_parser.add_argument("--idea", choices=ideas())
    list_parser.add_argument("--access", choices=["auto", "key", "manual"],
                             help="only sources needing this much work to obtain")
    list_parser.set_defaults(func=cmd_list)

    validate_parser = subparsers.add_parser("validate", help="check the catalog is sound")
    validate_parser.set_defaults(func=cmd_validate)

    export_parser = subparsers.add_parser("export", help="write the catalog to CSV and JSON")
    export_parser.set_defaults(func=cmd_export)

    page_parser = subparsers.add_parser("page", help="render the browsable HTML page")
    page_parser.add_argument("--fragment", type=Path,
                             help="also write a copy without the document skeleton")
    page_parser.set_defaults(func=cmd_page)

    fetch_parser = subparsers.add_parser("fetch", help="download the open datasets")
    fetch_parser.add_argument("--idea", choices=ideas())
    fetch_parser.add_argument("--dry-run", action="store_true",
                              help="report what would be downloaded, without downloading")
    fetch_parser.set_defaults(func=cmd_fetch)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI.

    Args:
        argv: Arguments to parse, or None to read from the command line.

    Returns:
        int: Process exit status.
    """
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
