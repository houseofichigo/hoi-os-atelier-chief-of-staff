---
name: hoi-3d-map
description: Affiche la base de connaissances du dossier sous forme de carte 3D cliquable (pages du wiki, liens entre elles, sources citées) avec un panneau latéral pour lire chaque page et chaque passage cité. À utiliser quand on demande la carte, le graphe, une vue d'ensemble visuelle du wiki, ou après une mise à jour du wiki.
license: MIT
---

# Carte 3D (version dossier)

Adaptation pour un simple dossier de la compétence `hoi-3d-map` de HOI OS (github.com/houseofichigo/hoi-os). Même principe : la carte montre le wiki et ses preuves, elle n'invente rien. Ici, pas d'application : un script lit `wiki/` et `.hoi/` et écrit un seul fichier `carte.html`, qui fonctionne sans internet.

## Ce que montre la carte
- **Un nœud par page du wiki**, coloré par type : client, personne, mission, réunion, décision (légende en haut à gauche).
- **Un nœud gris par source** ingérée ; **rouge** si la source est un « trou » (rien n'a pu être lu).
- **Un lien net** entre deux pages quand l'une cite l'autre avec `[[...]]`.
- **Un lien discret** entre une page et chaque source qu'elle cite `[src-XXXX ¶n]`.
- **À gauche** : recherche, filtres par type, liste de toutes les pages et sources (pour naviguer sans la 3D).
- **À droite** : au clic sur une page, son contenu mis en forme, avec liens et citations cliquables ; au clic sur une citation, la source avec le **passage exact surligné** et un lien vers le fichier original.

## Étapes

1. **Vérifier le wiki** :
   `python3 skills/hoi-3d-map/scripts/carte.py verifier`
   Le script liste les liens `[[...]]` cassés, les citations vers une source ou un passage qui n'existe pas, les citations vers une source illisible, les pages en double et les pages sans citation.
2. **Corriger avant de construire.** S'il y a des défauts, corrige les pages du wiki concernées (jamais les sources), puis relance l'étape 1. Si une correction demande une décision (deux pages qui pourraient être la même personne, par exemple), demande-moi au lieu de trancher.
3. **Construire la carte** :
   `python3 skills/hoi-3d-map/scripts/carte.py construire`
   Le fichier `carte.html` est écrit à la racine du dossier. Options : `--sans-sources` pour n'afficher que les pages, `--sortie autre-nom.html`.
4. **Ouvrir la carte** dans le navigateur : macOS `open carte.html`, Windows `start carte.html`, Linux `xdg-open carte.html`. Si tu ne peux pas ouvrir d'application, dis-moi de double-cliquer sur le fichier.
5. **Expliquer en trois lignes** ce qu'on voit : les couleurs, ce que signifient les nœuds rouges, comment ouvrir une page ou une source.
6. **Optionnel, garder la carte à jour** pendant qu'on travaille :
   `python3 skills/hoi-3d-map/scripts/surveiller.py`
   La carte est régénérée à chaque modification de `wiki/` ou `.hoi/`. Ctrl+C pour arrêter. Il suffit de recharger la page du navigateur.

## Ce que le script lit
- `wiki/**/*.md` : le type vient de l'en-tête de la page (`type:`) ou, à défaut, du dossier (`clients/`, `personnes/`, `missions/`, `reunions/`, `decisions/`). Le titre vient de l'en-tête (`titre:`) ou du premier titre `#`. `index.md` n'apparaît pas sur la carte.
- `.hoi/manifeste.json` : la liste des sources (identifiant, nom d'origine, chemin, provenance, date, statut). Une source au statut « trou » (ou « illisible ») est affichée en rouge.
- `.hoi/extraits/src-XXXX.md` : le texte de chaque source, découpé en passages `¶1`, `¶2`… C'est ce qui permet de surligner le passage exact cité.

## Règles
- **Ne jamais modifier `carte.html` à la main.** Elle est régénérée depuis le wiki. Si quelque chose manque sur la carte, c'est que ça manque dans le wiki : corrige le wiki ou dis-le-moi.
- **Ne jamais inventer** un nœud, un lien, une date ou un passage.
- Ne jamais modifier un fichier de `sources/` ni de `.hoi/` pour « faire marcher » la carte.
- Les fichiers de `_restreint/` n'apparaissent jamais sur la carte.
- `carte.html` contient le texte des sources : c'est un document interne, à ne pas envoyer ni publier.

## Prérequis
Python 3.9 ou plus, sans paquet à installer. Les bibliothèques d'affichage (3d-force-graph, marked) sont fournies dans `vendor/` (licences MIT, voir `vendor/LICENSES.txt`) et intégrées dans `carte.html` : aucune connexion internet n'est nécessaire.
