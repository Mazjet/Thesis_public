import argparse
import csv
import json
import re
import sys
from pathlib import Path


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_record(record: dict, idx: int, errors: list[str]) -> None:
    required = ["term", "slug", "short_definition", "full_definition", "category", "source"]
    for field in required:
        if not str(record.get(field, "")).strip():
            errors.append(f"Row {idx}: missing required field '{field}'.")

    slug = str(record.get("slug", "")).strip()
    if slug and not SLUG_RE.match(slug):
        errors.append(f"Row {idx}: invalid slug '{slug}'. Use lowercase latin, digits and hyphens only.")

    short_def = str(record.get("short_definition", "")).strip()
    full_def = str(record.get("full_definition", "")).strip()
    if short_def and len(short_def) > 180:
        errors.append(f"Row {idx}: short_definition too long ({len(short_def)} > 180).")
    if full_def and len(full_def) < 60:
        errors.append(f"Row {idx}: full_definition too short ({len(full_def)} < 60).")

    for int_field in ("category", "source"):
        value = str(record.get(int_field, "")).strip()
        if value:
            try:
                int(value)
            except ValueError:
                errors.append(f"Row {idx}: '{int_field}' must be an integer.")


def load_rows(path: Path) -> list[dict]:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON input must be a list of objects.")
        rows = []
        for item in data:
            if isinstance(item, dict) and "fields" in item:
                rows.append(item["fields"])
            elif isinstance(item, dict):
                rows.append(item)
            else:
                raise ValueError("Each JSON item must be an object.")
        return rows

    raise ValueError("Unsupported file format. Use .csv or .json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate term import files (.csv/.json).")
    parser.add_argument("path", type=Path, help="Path to CSV or JSON file with terms.")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"File not found: {args.path}")
        return 2

    try:
        rows = load_rows(args.path)
    except Exception as exc:
        print(f"Failed to read file: {exc}")
        return 2

    errors: list[str] = []
    seen_terms: set[str] = set()
    seen_slugs: set[str] = set()

    for idx, row in enumerate(rows, start=2):
        validate_record(row, idx, errors)

        term_key = str(row.get("term", "")).strip().lower()
        slug_key = str(row.get("slug", "")).strip().lower()

        if term_key:
            if term_key in seen_terms:
                errors.append(f"Row {idx}: duplicate term '{row.get('term')}'.")
            seen_terms.add(term_key)

        if slug_key:
            if slug_key in seen_slugs:
                errors.append(f"Row {idx}: duplicate slug '{row.get('slug')}'.")
            seen_slugs.add(slug_key)

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f" - {err}")
        return 1

    print(f"Validation passed. Rows checked: {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
