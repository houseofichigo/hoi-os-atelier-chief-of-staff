# Étape 9 — Construire le wiki

**Pourquoi.** Les sources sont des pièces d'archive : utiles comme preuves, pénibles à relire. Le wiki en fait des fiches de synthèse, une par client, personne, mission, réunion et décision, comme le dossier qu'un bon assistant tient sur chaque sujet. Chaque phrase garde sa citation. Quand deux documents ne disent pas la même chose, la fiche montre les deux au lieu de choisir en silence.

**Ce qu'on fait.** Envoyer le prompt.

```text
À partir des sources ingérées dans .hoi/extraits/, construis le wiki dans wiki/. Le wiki est une synthèse ; les sources restent les seules preuves.

Structure :
- wiki/clients/ : une page par client (Transports Ardelis, Al Rawiya Holding, Maison Corvelle, Dar Al Rimal)
- wiki/personnes/ : une page par personne (contacts clients et équipe Basira)
- wiki/missions/ : une page par mission ou opportunité
- wiki/reunions/ : une page par réunion passée ou à venir
- wiki/decisions/ : une page par décision importante
- wiki/index.md : la page d'accueil, avec la liste de toutes les pages par catégorie

Chaque page contient :
- en tête : titre, type, statut « brouillon », alias, date de mise à jour ;
- un résumé de trois lignes ;
- « Faits » : chaque fait suivi de sa source au format [src-XXXX ¶n]. Pas de source, pas de fait ;
- « Contradictions » : quand deux sources ne disent pas la même chose, montre les deux avec leurs dates, sans trancher en silence ;
- « Questions ouvertes » : ce que les sources ne disent pas ;
- « Liens » : les pages liées, au format [[nom-de-la-page]].

Règles :
- un document signé l'emporte sur un brouillon, et un document plus récent sur un plus ancien ; dis-le explicitement ;
- un résumé automatique ne suffit jamais : vérifie dans la transcription complète ;
- deux personnes qui ont le même prénom ont chacune leur page, avec le nom complet et l'entreprise ;
- les montants et la facturation d'un client ne figurent que sur sa propre page ;
- aucune information de _restreint/.

À la fin : vérifie que chaque citation [src-XXXX ¶n] renvoie à un passage qui existe et que chaque lien [[...]] renvoie à une page qui existe. Corrige ce qui ne va pas, puis donne-moi le nombre de pages par catégorie et la liste des contradictions trouvées.
```

**Ce qu'on doit voir.** Une vingtaine de pages. Sur la fiche Transports Ardelis : le prix signé de 16 500 € HT (et non les 18 000 € du brouillon), la contradiction sur le nombre de participants (12, puis 15, puis 14), et deux pages distinctes pour Sarah Martin et Sarah Al-Mansouri.

_Vidéo de référence : « Step 9 - Wiki creation »._

---
← [Toutes les étapes](README.md) · [SOP complète](../SOP.md)
