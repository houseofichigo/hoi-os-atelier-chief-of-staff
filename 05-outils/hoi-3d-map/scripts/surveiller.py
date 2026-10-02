#!/usr/bin/env python3
"""HOI OS — hoi-3d-map : régénère carte.html dès que le wiki ou les sources ingérées changent.

  python3 skills/hoi-3d-map/scripts/surveiller.py            # Ctrl+C pour arrêter
  options : --racine CHEMIN   --intervalle 2

Python 3.9+, bibliothèque standard uniquement (scrutation des dates de modification).
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def snapshot(root):
    state = {}
    for base in (root / "wiki", root / ".hoi"):
        if base.exists():
            for p in base.rglob("*"):
                if p.is_file() and p.suffix in (".md", ".json"):
                    try:
                        state[str(p)] = p.stat().st_mtime
                    except FileNotFoundError:
                        pass
    return state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default=None)
    ap.add_argument("--intervalle", type=float, default=2.0)
    a = ap.parse_args()
    root = Path(a.racine).resolve() if a.racine else HERE.parent.parent.parent
    cmd = [sys.executable, str(HERE / "carte.py"), "construire", "--racine", str(root)]
    print(f"Surveillance de {root / 'wiki'} et {root / '.hoi'} — Ctrl+C pour arrêter.")
    subprocess.run(cmd)
    last = snapshot(root)
    try:
        while True:
            time.sleep(a.intervalle)
            now = snapshot(root)
            if now != last:
                time.sleep(0.5)  # laisser finir l'écriture en cours
                print(time.strftime("%H:%M:%S"), "changement détecté → régénération")
                subprocess.run(cmd)
                last = snapshot(root)
    except KeyboardInterrupt:
        print("\nSurveillance arrêtée.")


if __name__ == "__main__":
    main()
