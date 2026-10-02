# Résultat de référence

Le dossier `dossier-basira-apres-etape-10/` montre **un** état correct du dossier après les étapes 5 (rangement), 8 (ingestion), 9 (wiki) et 10 (carte). Il sert à deux choses :

1. **Comparer** : vos résultats seront formulés autrement (chaque exécution de Codex est différente), mais les faits et les citations doivent correspondre.
2. **Reprendre en cas de problème** : copier ce dossier, puis continuer à partir de l'étape 11.

## Ce qu'il contient

| Élément | Contenu |
| --- | --- |
| `sources/` | Les originaux rangés par provenance (gmail, agenda, spark, pennylane, fichiers) |
| `_restreint/`, `_doublons/`, `_a-trier/` | Le RIB, les 3 doublons, le bruit |
| `.hoi/manifeste.json`, `.hoi/extraits/` | 34 sources ingérées, découpées en passages ¶ ; 1 trou (le scan) |
| `wiki/` | 20 pages : clients, personnes, missions, réunions, décisions |
| `carte.html` | La carte 3D, à ouvrir dans un navigateur (hors ligne) |

## Ce qu'il ne contient pas

Les fichiers des étapes 6 et 7 (AGENTS.md, RULES.md, skills…), l'application (étape 11) et les livrables des étapes 12 et 13 : ils dépendent de votre exécution. Le dossier `.hoi/` est caché sur macOS : touches Cmd + Maj + . pour l'afficher.

Pour régénérer la carte : `python3 ../../05-outils/hoi-3d-map/scripts/carte.py construire --racine .` depuis ce dossier.
