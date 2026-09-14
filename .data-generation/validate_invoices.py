"""Validate generated `invoice.json` files against the invoice schema.

Each file is parsed with the archetype schema and then run through
`invoice_problems` - the same arithmetic checks the generation agent applies to
its own output (line items multiply out, subtotals sum, taxes and tips add up
to `total_amount`). The appended `charges` list is checked too.

Usage: python validate_invoices.py ../data
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from generate_invoice import ChargeLine, invoice_adapter, invoice_problems, validate_charges

charges_adapter = TypeAdapter(list[ChargeLine])


def validate_file(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    charges = data.pop("charges", None)
    try:
        invoice = invoice_adapter.validate_python(data)
    except ValidationError as error:
        return [f"{err['loc']}: {err['msg']}" for err in error.errors()]

    problems = invoice_problems(invoice)
    if charges is None:
        return problems + ["missing `charges` list"]
    return problems + validate_charges(invoice, charges_adapter.validate_python(charges))


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate invoice JSON files for schema and arithmetic errors.")
    parser.add_argument("paths", nargs="+", type=Path, help="invoice.json files, or directories to search")
    args = parser.parse_args()

    files: list[Path] = []
    for path in args.paths:
        files += sorted(path.rglob("invoice.json")) if path.is_dir() else [path]

    failed = 0
    for file in files:
        problems = validate_file(file)
        if problems:
            failed += 1
            print(f"FAIL {file}")
            for problem in problems:
                print(f"       {problem}")
        else:
            print(f"ok   {file}")

    print(f"\n{len(files) - failed}/{len(files)} valid")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
