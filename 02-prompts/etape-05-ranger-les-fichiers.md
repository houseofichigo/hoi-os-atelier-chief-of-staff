# Étape 5 — Ranger les fichiers

**Pourquoi.** Un assistant ne raisonne pas proprement dans un dossier où l'original, la copie, le brouillon et la photo de vacances se mélangent. Le rangement sépare les preuves (sources/, par provenance, en lecture seule), la vue de travail par client (clients/, des copies), le sensible (_restreint/, jamais ouvert sans accord) et le bruit (_a-trier/, _doublons/, mis de côté sans être supprimé). Un dossier par outil (Gmail, Agenda…) prépare aussi la connexion future.

**Ce qu'on fait.** Envoyer le prompt.

```text
Lis ABOUT_US.md, en particulier la section 12 « Mes fichiers », puis range tous les fichiers de ce dossier.

Règles de rangement :
1. Les originaux sont rangés par provenance dans sources/ :
   - sources/gmail/ : les emails (.eml)
   - sources/agenda/ : les invitations (.ics)
   - sources/spark/ : les transcriptions de réunion (Spark, .vtt, notes de réunion, mémos vocaux)
   - sources/pennylane/ : les exports et les factures
   - sources/fichiers/ : tout le reste lié à l'activité
2. Crée une vue de travail par client dans clients/ : Transports Ardelis, Al Rawiya Holding, Maison Corvelle, Dar Al Rimal. Chacun avec les sous-dossiers reunions/, contrats/, finance/, echanges/. Ce sont des COPIES des originaux, nommées AAAA-MM-JJ_client_type_objet.ext (la date du document, pas la date du fichier).
3. Repère les doublons par leur CONTENU, pas par leur nom. Garde un exemplaire dans sources/ et place l'autre dans _doublons/.
4. Place les documents sensibles (bancaires, RH, salaires) dans _restreint/ en te fiant à leur nom. Ne les ouvre pas.
5. Place dans _a-trier/ ce qui n'a pas de lien clair avec un client ou une mission (photos personnelles, captures d'écran, fichiers vides, archives, newsletters, documents de plus de deux ans).
6. Ne modifie jamais le contenu d'un fichier. Ne supprime rien. Ne touche pas à ABOUT_US.md.

Une fois le rangement terminé :
- mets les originaux de sources/ en lecture seule ;
- vérifie que le nombre de fichiers avant et après correspond ;
- écris dans RANGEMENT.md ce que tu as fait : un tableau « fichier d'origine → nouvel emplacement → copies créées → raison », les doublons trouvés et comment tu les as repérés, les fichiers sensibles, les fichiers à trier, et tes doutes ;
- montre-moi l'arborescence finale sur deux niveaux.
```

**Ce qu'on doit voir.** Trois doublons trouvés par leur contenu (dont deux invitations au nom différent mais identiques) ; le RIB dans `_restreint/` ; la photo, la capture, l'archive, le fichier vide et les newsletters dans `_a-trier/` ; un fichier RANGEMENT.md qui trace chaque déplacement.

_Vidéo de référence : « Step 5 - Files management »._

---
← [Toutes les étapes](README.md) · [SOP complète](../SOP.md)
