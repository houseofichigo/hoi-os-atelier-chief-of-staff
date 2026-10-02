# Atelier HOI OS — Construire son Chief of Staff IA

**Un dossier en désordre devient une application de travail, en 13 étapes, avec Codex et les compétences [HOI OS](https://github.com/houseofichigo/hoi-os).**

Ce dépôt contient tout pour refaire l'exercice seul : le cas fictif complet (une société de conseil, ses 4 clients, 46 documents en vrac), les 13 prompts dans l'ordre, un résultat de référence et les réponses attendues.

> Toutes les personnes, sociétés, adresses et montants sont **fictifs**. Les adresses email utilisent le domaine réservé `.example`.

## Ce que vous allez construire

Yasmine Haddad dirige Basira Conseil, un cabinet de conseil en stratégie de 7 personnes. Son ordinateur déborde : emails exportés, transcriptions de réunion, factures, propositions en plusieurs versions, un scan illisible, des doublons. Nous sommes le jeudi 8 octobre 2026.

À la fin de l'exercice, son assistant :

- a **rangé** ses 46 fichiers (preuves, copies de travail, documents sensibles, bruit) ;
- a un **manuel** (AGENTS.md), des **règles**, une **mémoire validée** et des **compétences** ;
- a **lu** chaque document et peut **citer le passage exact** de chaque fait ;
- tient un **wiki** par client, personne, mission, réunion et décision, affiché en **carte 3D** ;
- fait tourner une **application** : brief du rendez-vous de demain, tâches promises, analyse de l'agenda, brouillons d'email, évaluations ;
- se **met à jour tout seul** quand un nouvel email arrive.

Sans jamais rien envoyer, ni déplacer dans l'agenda : **l'IA propose, vous décidez.**

## Démarrage rapide

1. **Prérequis** : [Codex](https://openai.com/codex/) installé, Python 3.9 ou plus, une connexion internet.
2. **Téléchargez** ce dépôt (bouton « Code » → « Download ZIP ») et décompressez-le.
3. **Créez un dossier de travail vide**, en dehors de ce dépôt (par exemple `Bureau/Basira – Yasmine`).
4. **Suivez les 13 étapes** ci-dessous, une par une. Chaque lien ouvre le prompt à copier dans Codex.
5. **Comparez** avec `03-resultat-de-reference/` et passez les évaluations de `04-presentateur/`.

## Réutilisation par la communauté

Ce dépôt est un atelier reproductible, pas un espace de stockage pour des données réelles. Pour l'adapter à votre organisation :

1. créez un dossier de travail séparé et non versionné ;
2. copiez-y la structure, jamais vos documents dans ce dépôt ;
3. remplacez `ABOUT_US.md` et le corpus fictif uniquement dans votre dossier privé ;
4. gardez les connecteurs en lecture seule au départ et conservez les validations humaines ;
5. ne publiez jamais `sources/`, `.hoi/`, `_restreint/`, `work/` ou des exports réels.

Avant une contribution :

```bash
python3 scripts/validate_repo.py
```

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour proposer une amélioration et [SECURITY.md](SECURITY.md) pour signaler un problème de sécurité ou de confidentialité.

Lisez d'abord la section « Comprendre la démarche » de [SOP.md](SOP.md) si vous découvrez le sujet : elle explique, sans jargon, ce qu'est un harness, un skill, l'ingestion ou une citation.

## Les 13 étapes

| # | Étape |
| --- | --- |
| 1 | [Créer un nouveau dossier](02-prompts/etape-01-creer-le-dossier.md) |
| 2 | [Créer le projet dans Codex](02-prompts/etape-02-creer-le-projet-codex.md) |
| 3 | [Déposer tous les fichiers dans le dossier](02-prompts/etape-03-deposer-les-fichiers.md) |
| 4 | [Faire l'inventaire du dossier](02-prompts/etape-04-inventaire.md) |
| 5 | [Ranger les fichiers](02-prompts/etape-05-ranger-les-fichiers.md) |
| 6 | [Créer AGENTS.md et les fichiers de gouvernance](02-prompts/etape-06-agents-md-et-gouvernance.md) |
| 7 | [Créer les skills](02-prompts/etape-07-creer-les-skills.md) |
| 8 | [Ingérer les documents](02-prompts/etape-08-ingestion.md) |
| 9 | [Construire le wiki](02-prompts/etape-09-wiki.md) |
| 10 | [Construire la carte 3D](02-prompts/etape-10-carte-3d.md) |
| 11 | [Construire l'application](02-prompts/etape-11-construire-l-application.md) |
| 12 | [Lancer les skills](02-prompts/etape-12-lancer-les-skills.md) |
| 13 | [Connecter les outils et lancer les automatisations](02-prompts/etape-13-outils-et-automatisations.md) |

## Organisation du dépôt

```
hoi-os-atelier-chief-of-staff/
├── README.md                     ← vous êtes ici
├── SOP.md                        ← la procédure complète, les 13 étapes et tous les prompts
├── 01-kit-de-depart/             ← ce qu'on dépose dans Codex
│   ├── ABOUT_US.md               ← la fiche d'identité de Basira Conseil
│   ├── fichiers-en-vrac/         ← les 45 fichiers en désordre
│   └── arrivee-16h28/            ← l'email de l'étape 13
├── 02-prompts/                   ← un fichier par étape, prompts prêts à copier
├── 03-resultat-de-reference/     ← un dossier correct après l'étape 10, carte comprise
├── 04-presentateur/              ← la clé du cas et les réponses des évaluations (à ne pas donner à l'IA)
└── 05-outils/
    ├── hoi-3d-map/               ← la compétence carte 3D, testée, hors ligne
    └── generer-le-corpus/        ← pour recréer le kit à l'identique
```

## Ce qui est imposé, ce qui est seulement demandé

Dans un simple dossier, certaines règles sont **garanties** (les originaux en lecture seule, le bac à sable de Codex), d'autres sont des **consignes** que le modèle peut ignorer (proposer avant d'écrire en mémoire, ne jamais suivre une instruction trouvée dans un document). C'est pour cela que l'exercice se termine par des évaluations. Détail dans [SOP.md](SOP.md#points-de-vigilance).

## Aller plus loin

- **Votre propre cas** : remplacez `ABOUT_US.md` et les fichiers en vrac par les vôtres, la procédure ne change pas.
- **Une autre IA** : les mêmes fichiers fonctionnent avec Claude Code (CLAUDE.md) et Gemini CLI (GEMINI.md), qui renvoient vers AGENTS.md.
- **Les compétences HOI OS** : [https://github.com/houseofichigo/hoi-os](https://github.com/houseofichigo/hoi-os).

## Licence

MIT — House of Ichigo. Les composants tiers gardent leur licence (voir [LICENSE](LICENSE)).
