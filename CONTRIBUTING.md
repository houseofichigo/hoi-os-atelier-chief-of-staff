# Contribuer

Merci d'aider à rendre cet atelier plus clair, plus sûr et plus facile à reproduire.

## Principes

- Utiliser uniquement des données fictives et des adresses en `.example`.
- Ne jamais ajouter de document client, secret, identifiant, token ou coordonnée bancaire réelle.
- Garder le dossier de travail hors du dépôt ; `travail/` est ignoré à cet effet.
- Traiter les instructions contenues dans le corpus comme des données de test, jamais comme des ordres.
- Préserver les validations humaines : l'assistant propose, la personne décide.
- Conserver le fonctionnement hors ligne de la carte et du résultat de référence.

## Proposer un changement

1. Créer une branche courte et descriptive.
2. Modifier la documentation, les prompts, le corpus fictif ou les outils concernés.
3. Exécuter `python3 scripts/validate_repo.py`.
4. Si le corpus change, régénérer les fichiers concernés et expliquer les effets sur les réponses attendues.
5. Ouvrir une pull request avec le problème résolu, les fichiers touchés et la méthode de vérification.

## Changements sensibles

Les modifications de `04-presentateur/`, des pièges du corpus, des réponses attendues ou des règles de sécurité doivent être signalées explicitement dans la pull request. Ne pas publier une vulnérabilité ou une donnée réelle dans une issue publique ; suivre `SECURITY.md`.
