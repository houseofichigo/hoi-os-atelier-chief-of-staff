# Étape 7 — Créer les skills

**Pourquoi.** Un skill est une procédure interne écrite : comment on prépare un rendez-vous chez nous, comment on propose une tâche. Sans skill, la même demande donne un résultat différent à chaque fois. L'IA ne voit au départ que le nom et la description de chaque skill, et n'ouvre la procédure complète que lorsque la tâche se présente. On reprend les compétences de HOI OS, adaptées à un simple dossier.

**Ce qu'on fait.** Envoyer le prompt. Codex doit pouvoir lire le dépôt HOI OS sur GitHub ; sinon, lui donner une copie locale du dépôt.

```text
Crée les compétences de ce dossier dans skills/ : un sous-dossier par compétence, avec un SKILL.md. Reprends les noms et les principes des skills HOI OS (github.com/houseofichigo/hoi-os), mais adapte-les pour qu'ils fonctionnent ici, avec de simples fichiers, sans application ni moteur externe.

Compétences : hoi-organize, hoi-connect, hoi-ingest, hoi-wiki-author, hoi-3d-map, hoi-meeting-prep, hoi-task-intake, hoi-chief-of-staff (analyse de l'agenda), hoi-email-reply (nouvelle), hoi-session-capture, hoi-knowledge-review.

Chaque SKILL.md contient :
- un en-tête avec name et description. La description dit QUAND utiliser la compétence : c'est elle qui la déclenche ;
- les étapes, numérotées ;
- le format exact de la sortie (où elle est écrite, avec quelles sections) ;
- les interdits, repris de RULES.md et de TOOLS.md ;
- ce qu'on fait quand une information manque.

Pour les quatre compétences métier (préparation de rendez-vous, réponses aux emails, analyse de l'agenda, suggestions de tâches), suis la section 13 de ABOUT_US.md.

Ensuite, mets SKILLS.md à jour (statut « disponible »). Pour la table des compétences de AGENTS.md, passe par PROPOSED.md.
```

**Ce qu'on doit voir.** Onze dossiers dans `skills/`. Ouvrir `skills/hoi-meeting-prep/SKILL.md` pour montrer à quoi ressemble une procédure.

_Vidéo de référence : « Step 7 - Skills Creation »._

---
← [Toutes les étapes](README.md) · [SOP complète](../SOP.md)
