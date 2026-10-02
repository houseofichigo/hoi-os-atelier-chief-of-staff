# Étape 6 — Créer AGENTS.md et les fichiers de gouvernance

**Pourquoi.** C'est la fiche de poste et le règlement intérieur du nouveau collaborateur. Sans ces fichiers, l'IA devine ; avec eux, elle sait qui elle sert, ce qu'elle peut faire seule, ce qu'elle doit faire valider et ce qu'elle ne fera jamais. Tous sont générés à partir d'une seule fiche, ABOUT_US.md : on décrit qui on est une fois, le cadre en découle.

**Ce qu'on fait.** Envoyer le prompt principal, puis (optionnel) faire relire le manuel.

| Fichier | Rôle |
| --- | --- |
| AGENTS.md | Le manuel, lu à chaque session : rôle, carte du dossier, quand utiliser quelle compétence, règles essentielles |
| RULES.md | Les règles détaillées, en séparant ce qui est imposé de ce qui est demandé |
| GOALS.md | Les 3 objectifs, les responsabilités, les préférences |
| MEMORY.md | Uniquement des faits approuvés, datés et sourcés |
| PROPOSED.md | La file d'attente : ce que l'IA propose et que vous validez |
| TOOLS.md | Les outils et ce que l'IA a le droit d'y faire |
| FILESYSTEM.md | L'organisation réelle du dossier |
| docs/TOOL_CONVENTIONS.md | Comment utiliser un outil sans risque |
| SKILLS.md | Le catalogue des compétences |
| EVALS.md | Les questions de test ; les réponses attendues sont écrites par vous |
| resources/ | Votre voix, vos modèles d'email, votre grille de prix |
| CLAUDE.md, GEMINI.md | Deux lignes qui renvoient à AGENTS.md, pour changer d'IA sans rien réécrire |

**Prompt principal**

```text
Lis ABOUT_US.md en entier et regarde l'arborescence que nous venons de créer. À partir de ces deux sources UNIQUEMENT, crée les fichiers qui gouvernent ce dossier. N'invente aucun fait : si une information manque, écris « à compléter » et liste-la à la fin.

À créer :
- AGENTS.md : le manuel que tu liras à chaque session. Court, moins de 150 lignes : ton rôle, ce que tu lis au début de chaque session, la carte du dossier, quelle compétence utiliser et quand, les règles essentielles (jamais / avec validation / sans demander), la hiérarchie des sources, le format des réponses, que faire en cas d'échec. Il renvoie aux autres fichiers pour le détail.
- RULES.md : les règles détaillées, en séparant clairement ce qui est IMPOSÉ (lecture seule, plans approuvés, bac à sable de Codex) de ce qui est DEMANDÉ (consignes que tu dois suivre mais que rien ne bloque).
- GOALS.md : mes trois objectifs, mes responsabilités, mes préférences.
- MEMORY.md : uniquement les faits stables de ABOUT_US (équipe, clients, contacts, offres, conditions). Une ligne par fait, au format « AAAA-MM-JJ · fait · source : ABOUT_US ». Rien d'autre.
- PROPOSED.md : la file d'attente des modifications à valider. Vide, avec le modèle d'une entrée.
- TOOLS.md : les outils et les droits outil par outil (sans demander / avec validation / jamais), et la différence entre connexion, fournisseur de modèle, adaptateur et droits.
- FILESYSTEM.md : l'organisation réelle du dossier telle qu'elle existe maintenant : qui écrit où, ce qui est en lecture seule, comment on nomme, ce qu'on ne supprime jamais.
- docs/TOOL_CONVENTIONS.md : comment utiliser un outil : vérifier ses droits, ne jamais refaire une action dont on n'est pas sûr qu'elle a échoué, citer ses preuves, signaler une erreur.
- SKILLS.md : le catalogue des compétences prévues (section 13) avec, pour chacune, le déclencheur, les entrées, la sortie et les interdits. Statut : « à créer ».
- EVALS.md : 12 questions de test construites à partir de la section 15, avec pour chacune ce qu'une bonne réponse doit respecter. Laisse la colonne « réponse attendue » vide : c'est moi qui la remplis. Marque le fichier « BROUILLON — à valider par Yasmine ».
- resources/voice.md, resources/pricing.md, et resources/email-templates.md avec 5 modèles : envoi d'une proposition, renvoi d'une facture, relance à 15 jours, relance à 30 jours, réorientation.
- CLAUDE.md et GEMINI.md : deux lignes qui renvoient à AGENTS.md.

Ne crée ni CONTEXT.md ni PLUGINS.md (voir la fin de ABOUT_US.md).

À la fin, donne-moi un tableau : fichier, rôle en une phrase, nombre de lignes. Puis la liste des « à compléter ».
```

**Optionnel — faire relire le manuel**

```text
Relis AGENTS.md comme le ferait un nouveau collaborateur. Liste ce qui est ambigu, ce qui contredit ABOUT_US.md et ce qui est trop long. Propose les corrections dans PROPOSED.md. Ne modifie pas AGENTS.md toi-même.
```

**Ce qu'on doit voir.** Les fichiers créés, un tableau récapitulatif et une courte liste « à compléter ». Ensuite, recopier dans EVALS.md les réponses attendues de `04-presentateur/EVALS_reponses-attendues.md`.

_Vidéo de référence : « Step 6 - Agents.Md creation »._

---
← [Toutes les étapes](README.md) · [SOP complète](../SOP.md)
