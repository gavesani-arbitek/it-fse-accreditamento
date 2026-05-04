#!/usr/bin/env python3
"""Conta il totale dei documenti inviati e dei documenti non validati (con errori)."""

import json
import glob
import os
import sys

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "GATEWAY")


def count_documents(base_dir):
    data_files = glob.glob(os.path.join(base_dir, "**", "data.json"), recursive=True)

    total_sent = 0
    total_ko = 0

    for filepath in data_files:
        try:
            with open(filepath, encoding="utf-8") as fp:
                data = json.load(fp)
            results = data.get("results") or []
            total_sent += len(results)
            for result in results:
                files = result.get("files") or []
                # Documents not validated are identified by the "_KO" suffix in
                # their filename, which is the naming convention used throughout
                # this repository to mark test cases that expect an error
                # response from the gateway (no dedicated status field exists in
                # the data.json schema).
                if any("_KO" in fname.upper() for fname in files):
                    total_ko += 1
        except Exception as e:
            print(f"Attenzione: impossibile leggere {filepath}: {e}", file=sys.stderr)

    return total_sent, total_ko


if __name__ == "__main__":
    total_sent, total_ko = count_documents(BASE_DIR)
    print(f"total_sent={total_sent}")
    print(f"total_ko={total_ko}")
