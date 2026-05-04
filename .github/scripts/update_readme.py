#!/usr/bin/env python3
"""Aggiorna il README.md con le statistiche dei documenti."""

import re
import sys
import os

README_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "README.md")

STATS_BLOCK_START = "<!-- STATS:START -->"
STATS_BLOCK_END = "<!-- STATS:END -->"


def build_stats_block(total_sent, total_ko):
    return (
        f"{STATS_BLOCK_START}\n"
        f"| Metrica | Valore |\n"
        f"|---|---|\n"
        f"| Totale documenti inviati | **{total_sent}** |\n"
        f"| Totale documenti non validati (con errori nella risposta) | **{total_ko}** |\n"
        f"{STATS_BLOCK_END}"
    )


def update_readme(total_sent, total_ko):
    with open(README_PATH, encoding="utf-8") as fp:
        content = fp.read()

    new_block = build_stats_block(total_sent, total_ko)

    pattern = re.compile(
        re.escape(STATS_BLOCK_START) + r".*?" + re.escape(STATS_BLOCK_END),
        re.DOTALL,
    )

    if pattern.search(content):
        updated = pattern.sub(new_block, content)
    else:
        # If the block does not exist yet, insert it before the first level-2
        # heading so the stats always appear near the top of the page.
        anchor = "\n## Procedura di caricamento dei risultati"
        if anchor not in content:
            raise RuntimeError(
                "Impossibile trovare il punto di inserimento nel README. "
                "Aggiungere manualmente il blocco STATS:START/STATS:END."
            )
        updated = content.replace(
            anchor,
            f"\n## Statistiche\n\n{new_block}\n\n## Procedura di caricamento dei risultati",
            1,
        )

    with open(README_PATH, "w", encoding="utf-8") as fp:
        fp.write(updated)

    print(f"README aggiornato: {total_sent} documenti inviati, {total_ko} non validati")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <total_sent> <total_ko>", file=sys.stderr)
        sys.exit(1)
    update_readme(int(sys.argv[1]), int(sys.argv[2]))
