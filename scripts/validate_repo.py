#!/usr/bin/env python3
"""Contrôles locaux avant publication du kit communautaire."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "SOP.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "01-kit-de-depart/ABOUT_US.md",
    "02-prompts/etape-13-outils-et-automatisations.md",
    "03-resultat-de-reference/dossier-basira-apres-etape-10/carte.html",
    "04-presentateur/EVALS_reponses-attendues.md",
    "05-outils/hoi-3d-map/vendor/3d-force-graph.min.js",
]
TEXT_SUFFIXES = {
    ".md", ".txt", ".eml", ".ics", ".csv", ".json", ".py", ".yml",
    ".yaml", ".toml", ".html", ".css", ".js",
}
SECRET_PATTERNS = {
    "clé privée": re.compile(r"BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY"),
    "secret explicite": re.compile(r"(?i)(?:api[_-]?key|secret[_-]?key|access[_-]?token|password)\s*[:=]\s*[^\s<]{8,}"),
    "chemin local macOS": re.compile(r"/Users/[^/\s]+/"),
}
EMAIL = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(errors, f"fichier requis absent : {relative}")

    if any(path.is_dir() and path != ROOT / ".git" for path in ROOT.rglob(".git")):
        fail(errors, "un dépôt .git imbriqué est présent")

    oversized = [path.relative_to(ROOT) for path in ROOT.rglob("*") if path.is_file() and path.stat().st_size > 25 * 1024 * 1024]
    for path in oversized:
        fail(errors, f"fichier supérieur à 25 Mio : {path}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if "vendor" in path.parts or "polices" in path.parts or path.name == "validate_repo.py":
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(ROOT)
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                fail(errors, f"{label} détecté dans {relative}")
        for address in EMAIL.findall(content):
            if not address.lower().endswith(".example"):
                fail(errors, f"adresse non fictive dans {relative} : {address}")

    loose = ROOT / "01-kit-de-depart" / "fichiers-en-vrac"
    arrivals = ROOT / "01-kit-de-depart" / "arrivee-16h28"
    if loose.is_dir() and len([p for p in loose.iterdir() if p.is_file()]) != 45:
        fail(errors, "le kit de départ ne contient pas exactement 45 fichiers en vrac")
    if arrivals.is_dir() and len([p for p in arrivals.iterdir() if p.is_file()]) != 1:
        fail(errors, "arrivee-16h28 ne contient pas exactement un email")

    if errors:
        print("VALIDATION ÉCHOUÉE")
        for error in errors:
            print(f"- {error}")
        return 1

    files = sum(
        1
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.relative_to(ROOT).parts
        and "__pycache__" not in path.relative_to(ROOT).parts
    )
    print(f"VALIDATION OK — {files} fichiers, corpus fictif et structure communautaire vérifiés.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
