#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "project"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_project(
    *,
    base_dir: Path,
    name: str,
    category: str,
    description: str = "",
    created_at: datetime | None = None,
) -> Path:
    created_at = created_at or _now()
    date_folder = created_at.strftime("%Y-%m-%d")
    timestamp = created_at.strftime("%Y%m%dT%H%M%SZ")
    project_slug = _slugify(name)
    category_slug = _slugify(category)

    project_dir = base_dir / category_slug / date_folder / f"{timestamp}-{project_slug}"
    project_dir.mkdir(parents=True, exist_ok=False)

    metadata = {
        "name": name,
        "category": category,
        "description": description,
        "created_at": created_at.isoformat(),
        "path": str(project_dir),
    }
    (project_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    return project_dir


def list_projects(base_dir: Path) -> Iterable[Path]:
    if not base_dir.exists():
        return []
    return sorted(
        (path for path in base_dir.glob("*/*/*") if path.is_dir()),
        key=lambda path: path.name,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Store projects in categorized folders with timestamps."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Create a new project entry")
    add_parser.add_argument("name", help="Project name")
    add_parser.add_argument("--category", required=True, help="Project category")
    add_parser.add_argument(
        "--description", default="", help="Optional short project description"
    )
    add_parser.add_argument(
        "--base-dir",
        default="projects",
        help="Directory where projects are stored (default: projects)",
    )

    list_parser = subparsers.add_parser("list", help="List stored projects")
    list_parser.add_argument(
        "--base-dir",
        default="projects",
        help="Directory where projects are stored (default: projects)",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    if args.command == "add":
        path = create_project(
            base_dir=base_dir,
            name=args.name,
            category=args.category,
            description=args.description,
        )
        print(path)
    elif args.command == "list":
        for path in list_projects(base_dir):
            print(path)


if __name__ == "__main__":
    main()
