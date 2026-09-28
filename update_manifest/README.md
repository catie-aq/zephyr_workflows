---
titre: Mise à jour d'un manifeste Zephyr
---

# Mise à jour d'un manifeste Zephyr

Met à jour les révisions d'un manifeste `west.yml` avec le dernier commit de la branche par défaut de chaque dépôt `catie-aq` qu'il référence, puis publie en artefacts le résumé des changements, les matrices des dépôts modifiés et un manifeste de test. À utiliser dans un workflow de montée de version automatique d'un manifeste 6TRON.

Fichier : `update_manifest/action.yml` · Type : action composite

## Utilisation

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: catie-aq/zephyr_workflows/update_manifest@main
    with:
      manifest: ${{ github.workspace }}/west.yml
      personal_access_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
```

## Entrées

| Nom | Type | Description | Requis | Défaut |
| ------------------------- | ------- | ---------------------------------------- | ----- | ------------ |
| `manifest` | string | Chemin du manifeste à mettre à jour (modifié en place) ; chemin absolu conseillé, voir « Points d'attention ». | oui | |
| `personal_access_token` | string | Jeton d'accès personnel GitHub utilisé pour interroger l'API GitHub. | oui | |

## Sorties

| Nom | Description |
| ------------ | ---------------------------------------- |

Aucune. L'action publie quatre artefacts :

- `change` : `change.md`, une ligne « Bumps catie-aq/<dépôt> from <ancien> to <nouveau> » par dépôt modifié ;
- `matrix` : `matrix.json`, `{"repo": [<path>, ...]}` des dépôts modifiés hors dépôts dont le nom contient `core` ;
- `matrix_core` : `matrix_core.json`, même format pour les dépôts dont le nom contient `core` ;
- `west` : `test_manifest.yml`, le manifeste mis à jour augmenté du projet `zephyr` à la dernière release de `zephyrproject-rtos/zephyr` (`import: true`).

## Fonctionnement

Étapes :

1. Dans le dossier de l'action : `pip install poetry` puis `poetry install` (Python `^3.9`, `click`, `pyyaml`, `requests`).
2. `poetry run update --manifest <manifest> --token <personal_access_token>` (script `update_manifest/update_manifest/update.py`) :
   - lecture des projets du manifeste (clés `repo-path`, `revision`, `path` requises pour chacun) ;
   - pour chaque projet, lecture de la branche par défaut de `catie-aq/<repo-path>` et de son dernier commit via l'API GitHub ;
   - écriture de `change.md`, `matrix.json` et `matrix_core.json` ;
   - remplacement des anciennes révisions par les nouvelles dans le manifeste ;
   - écriture de `test_manifest.yml`.
3. `actions/upload-artifact@v4` pour `change`, `matrix`, `west` et `matrix_core`.

## Dépendances

- `actions/upload-artifact@v4`
- Python, `pip` et l'accès à PyPI sur le runner (installation de Poetry à chaque exécution).

## Points d'attention

- Les chemins des fichiers produits sont exposés par `echo "::set-output ..."`, syntaxe dépréciée ; ces valeurs ne sont pas des sorties de l'action (`action.yml` ne déclare pas de `outputs:`).
- Le script tourne dans le dossier de l'action (`cd ${GITHUB_ACTION_PATH}`) : un `manifest` relatif est résolu depuis ce dossier, pas depuis l'espace de travail.
- Le jeton est passé en argument de ligne de commande (`--token`).
- La mise à jour du manifeste remplace chaque ancienne révision par une recherche-remplacement sur tout le fichier : une révision identique ailleurs dans le fichier est aussi remplacée.
- Un projet sans `repo-path` ou `path` fait échouer le script (`KeyError`).
- L'appel à l'API des releases Zephyr ne vérifie pas le code de retour HTTP.
