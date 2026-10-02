# Étape 11 — Construire l'application

**Pourquoi.** La carte montre ce que l'assistant sait. L'application montre ce qu'il fait pour vous : le brief de demain, les tâches, l'agenda de la semaine, les brouillons à relire, ce qui attend votre décision. On la construit d'abord vide : chaque compétence lancée ensuite remplit son écran.

**Ce qu'on fait.** Envoyer le prompt, puis garder l'application ouverte dans le navigateur pendant les étapes 12 et 13.

```text
Construis l'application « Chief of Staff — Basira Conseil » autour de la carte 3D que nous venons de créer. C'est l'interface de travail de Yasmine : tout ce que produisent les compétences doit y apparaître.

FORME
- Un dossier app/ avec un script de génération (app/generer.py) qui lit les fichiers du dossier et écrit app/index.html : un seul fichier, qui s'ouvre dans le navigateur et fonctionne sans internet.
- Un script de surveillance qui régénère l'application dès qu'un fichier change dans wiki/, work/, .hoi/, PROPOSED.md, MEMORY.md ou EVALS.md.
- Les données viennent toujours des fichiers au moment de la génération, jamais d'une copie faite à la main.
- Design sobre et lisible en vidéo-projection : barre latérale de navigation, grande zone de contenu, police lisible, mode sombre.

ÉCRANS (menu à gauche)
1. Aujourd'hui — jeudi 8 octobre 2026 : les rendez-vous du jour et de demain, les tâches urgentes, les échéances des 7 prochains jours, les alertes (factures en retard, emails suspects, trous dans les sources).
2. Carte — la carte 3D existante, intégrée telle quelle, avec son panneau latéral et ses citations cliquables.
3. Clients — une fiche par client tirée du wiki : contacts, mission en cours, situation de facturation, contradictions, questions ouvertes. Chaque fait garde sa citation cliquable.
4. Agenda — la semaine du 12 octobre, jour par jour, avec les alertes produites par la compétence hoi-chief-of-staff.
5. Tâches — le contenu de work/taches.md, avec les statuts : proposée, acceptée, faite, probablement faite.
6. Briefs — les briefs de rendez-vous de work/briefs/.
7. Brouillons — les brouillons d'email de work/brouillons/, avec la mention visible « Brouillon — jamais envoyé ».
8. Validations — le contenu de PROPOSED.md : ce qui attend ma décision.
9. Mémoire — MEMORY.md, en lecture seule.
10. Évaluations — le dernier résultat de EVALS.md.

RÈGLES
- Partout, une citation [src-XXXX ¶n] est cliquable et ouvre le passage exact, comme sur la carte.
- Un écran sans données affiche un état vide clair, par exemple « Aucun brief pour l'instant — lancez hoi-meeting-prep », jamais des données inventées.
- L'application n'envoie rien, ne modifie aucun fichier et ne contient rien de _restreint/.

À la fin, lance la surveillance, ouvre l'application dans mon navigateur et montre-moi les écrans qui sont encore vides.
```

**Ce qu'on doit voir.** L'application ouverte. Aujourd'hui, Carte, Clients et Mémoire sont déjà remplis ; Briefs, Tâches, Agenda, Brouillons et Évaluations sont vides.

_Vidéo de référence : « Step 11 - Build the app »._

---
← [Toutes les étapes](README.md) · [SOP complète](../SOP.md)
