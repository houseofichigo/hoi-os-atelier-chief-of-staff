# Étape 13 — Connecter les outils et lancer les automatisations

**Pourquoi.** Jusqu'ici, on a tout fait à la main. Les deux derniers leviers du harness font travailler l'assistant sans qu'on le lui demande. Les outils (Gmail, Agenda, Spark, Pennylane) amènent les données, en lecture seule d'abord : un outil connecté n'est pas une autorisation. Les automatisations déclenchent une compétence à heure fixe (le lundi matin, chaque soir) ou à un événement (un nouvel email). Dans cette démonstration, les outils sont simulés par leurs exports : en production, la connexion se fait en lecture seule et les données arrivent au même endroit.

**Ce qu'on fait.** Envoyer le premier prompt. Puis déposer `01-kit-de-depart/arrivee-16h28/Wifi et comptes atelier.eml` dans `inbox/gmail/` et envoyer le second : c'est l'automatisation « nouvel email » qui se déclenche.

**Connecter les outils et définir les automatisations**

```text
Utilise la compétence hoi-connect.

1. Vérifie quels connecteurs sont réellement disponibles dans cette session : Gmail, Google Agenda, Spark, Pennylane. Pour chacun, réponds « disponible » ou « non disponible ». Ne te connecte à rien sans mon accord.
2. Pour cette démonstration, ces outils sont simulés par leurs exports, déjà rangés dans sources/. Crée les dossiers d'arrivée inbox/gmail, inbox/agenda, inbox/spark et inbox/pennylane pour les prochains fichiers.
3. Mets à jour TOOLS.md : pour chaque outil, ce qui est permis sans demander, avec validation, et jamais (section 9 de ABOUT_US.md), en lecture seule d'abord. Ajoute une ligne : les automatisations utilisent les mêmes droits que moi, jamais plus.
4. Décris les automatisations dans AUTOMATIONS.md. Pour chacune : le déclencheur (heure fixe ou événement), la compétence utilisée, ce qu'elle produit, où le résultat apparaît dans l'application, et ce qu'elle n'a jamais le droit de faire. Au minimum :
   - chaque lundi à 8 h : analyse de la semaine (hoi-chief-of-staff) ;
   - chaque soir à 18 h : promesses et tâches du jour (hoi-task-intake) ;
   - la veille de chaque rendez-vous client : brief (hoi-meeting-prep) ;
   - à chaque nouveau fichier dans inbox/gmail : ingestion, mise à jour du wiki et du brief concerné.
5. Si cette session permet de programmer des tâches, propose-moi de les activer ; sinon, explique comment les lancer à la main.
Montre-moi TOOLS.md et AUTOMATIONS.md.
```

**Déclencher l'automatisation « nouvel email »**

```text
Un nouvel email vient d'arriver dans inbox/gmail. Exécute l'automatisation prévue pour ce cas dans AUTOMATIONS.md : ingère-le, mets à jour le wiki et le brief de mon appel de demain. Dis-moi ce qui a changé et où le voir dans l'application.
```

**Ce qu'on doit voir.** Un tableau des connecteurs (probablement « non disponible » en démo), TOOLS.md à jour, AUTOMATIONS.md avec quatre automatisations. Après le nouvel email : le trou sur le Wi-Fi se referme (accès ouvert pour Copilot et ChatGPT Enterprise le 15, comptes créés le 14, identifiants envoyés à Sarah Martin) et le brief de demain est mis à jour.

_Vidéo de référence : « Step 13 - connect tools and run automations »._

---
← [Toutes les étapes](README.md) · [SOP complète](../SOP.md)
