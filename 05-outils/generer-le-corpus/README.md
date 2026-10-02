# Régénérer le corpus

Ces deux scripts recréent les 45 fichiers du dossier en vrac et l'email de 16 h 28, à l'identique (mêmes noms, mêmes contenus, mêmes montants).

```bash
pip install python-docx openpyxl reportlab pillow
python3 fichiers_texte.py
python3 fichiers_binaires.py
```

Les fichiers sont écrits dans `sortie/fichiers-en-vrac/` et `sortie/arrivee-16h28/`. Pour un autre dossier : variables d'environnement `OUT` et `WAVE2`.

Pour adapter le cas (autres clients, autres dates), modifiez les textes dans les deux scripts et gardez la cohérence avec `ABOUT_US.md` et `04-presentateur/CORPUS_CLE.md`.

Les polices DejaVu (`polices/`) sont fournies pour que les PDF s'affichent pareil sur tous les systèmes ; leur licence libre est dans `polices/LICENCE-DejaVu.txt`.
