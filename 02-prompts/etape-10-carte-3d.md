# Étape 10 — Construire la carte 3D

**Pourquoi.** Une liste de vingt fiches et trente-quatre sources ne se lit pas d'un coup d'œil. La carte montre la base de connaissances comme un réseau : les clients, les personnes, les réunions, et les preuves sur lesquelles tout repose. Un clic sur une fiche l'ouvre ; un clic sur une citation affiche le passage exact. Une source en rouge est un document qu'on n'a pas pu lire.

**Ce qu'on fait.** Envoyer le prompt. Plan B si Codex peine : copier `05-outils/hoi-3d-map/` dans `skills/` et lui demander de suivre cette compétence (déjà testée, fonctionne hors ligne).

```text
Utilise l'approche de la compétence hoi-3d-map de HOI OS (github.com/houseofichigo/hoi-os) pour créer une carte 3D interactive de ma base de connaissances. Ici, il n'y a pas d'application HOI OS : tu construis la carte toi-même, à partir des fichiers du dossier, en respectant les mêmes principes : la carte montre le wiki et ses preuves, elle n'invente rien.

Le résultat est un seul fichier carte.html à la racine du dossier, qui s'ouvre dans le navigateur.

ÉTAPE 1 — Vérifier le wiki avant de construire
- Chaque lien [[...]] doit renvoyer à une page qui existe dans wiki/.
- Chaque citation [src-XXXX ¶n] doit renvoyer à une source de .hoi/manifeste.json et à un passage qui existe dans .hoi/extraits/src-XXXX.md.
- Aucune page ne doit citer un passage d'une source marquée « trou ».
Corrige les pages du wiki qui posent problème (jamais les sources), puis donne-moi la liste de ce que tu as corrigé.

ÉTAPE 2 — Construire la carte
Contenu :
- un nœud par page du wiki, coloré par type (client, personne, mission, réunion, décision), avec une légende ;
- un nœud gris par source, rouge si la source est un « trou » ;
- un lien entre deux pages quand l'une cite l'autre avec [[...]] ;
- un lien plus discret entre une page et chaque source qu'elle cite.

Interactions :
- on peut faire pivoter, zoomer et se déplacer ;
- au clic sur une page : un panneau latéral affiche son contenu mis en forme ; les liens [[...]] et les citations [src-XXXX ¶n] y sont cliquables ;
- au clic sur une citation : le panneau affiche la source avec le passage exact surligné, et un lien pour ouvrir le fichier original ;
- pour chaque source, la liste des pages qui la citent ;
- un bouton « Retour » pour revenir à l'élément précédent ;
- une barre de recherche (titres, contenu des pages et texte des sources) et des filtres par type ;
- une liste des pages à gauche, pour naviguer sans la 3D.

Contraintes :
- utilise la bibliothèque 3d-force-graph ; télécharge-la dans le dossier et intègre-la dans carte.html pour que la carte fonctionne sans internet ;
- les données viennent du wiki et de .hoi/ au moment de la génération, jamais d'une copie faite à la main ;
- écris un script (par exemple scripts/carte.py) qui génère carte.html, et un second script qui surveille wiki/ et .hoi/ et régénère carte.html dès qu'un fichier change ;
- n'invente aucun nœud, aucun lien, aucune date, aucun passage : si quelque chose manque sur la carte, c'est que ça manque dans le wiki ;
- rien de _restreint/ n'apparaît sur la carte.

ÉTAPE 3 — Ouvrir et expliquer
Ouvre carte.html dans mon navigateur, lance le script de surveillance, puis décris-moi en trois lignes ce qu'on y voit : ce que représentent les couleurs, ce que signifient les nœuds rouges, et comment ouvrir une page ou une source.
```

**Plan B — avec la compétence fournie**

```text
Utilise la compétence hoi-3d-map (skills/hoi-3d-map/SKILL.md) pour afficher ma base de connaissances en 3D.
Suis-la étape par étape : vérifie le wiki, corrige ce qui doit l'être, construis la carte, ouvre-la dans mon navigateur, puis décris-moi en trois lignes ce qu'on y voit.
Ensuite, lance la surveillance pour que la carte se mette à jour quand le wiki change.
```

**Ce qu'on doit voir.** La carte dans le navigateur. Démonstration conseillée : cliquer sur Transports Ardelis, puis sur la citation du prix signé : la proposition s'affiche, le passage « 16 500 € HT » surligné. Puis cliquer sur le nœud rouge : le scan illisible et son avertissement.

_Vidéo de référence : « step 10 - 3D Map »._

---
← [Toutes les étapes](README.md) · [SOP complète](../SOP.md)
