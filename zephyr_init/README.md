---
titre: Initialisation d'un espace de travail Zephyr
---

# Initialisation d'un espace de travail Zephyr

Configure les identifiants Git pour cloner les dépôts privés, puis initialise et met à jour l'espace de travail `west` à partir du manifeste `workdir/west.yml`. À placer après l'écriture de ce manifeste (checkout dans `workdir` ou `generate_manifest`).

Fichier : `zephyr_init/action.yml` · Type : action composite

## Utilisation

```yaml
steps:
  - uses: actions/checkout@v4
    with:
      path: workdir
  - uses: catie-aq/zephyr_workflows/zephyr_init@main
    with:
      personal_access_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
```

## Entrées

| Nom | Type | Description | Requis | Défaut |
| ------------------------- | ------- | ---------------------------------------- | ----- | ------------ |
| `personal_access_token` | string | Jeton d'accès personnel GitHub utilisé par Git pour cloner les dépôts du manifeste. | oui | |

## Sorties

| Nom | Description |
| ------------ | ---------------------------------------- |

Aucune.

## Fonctionnement

Étapes (toutes en `bash`) :

1. `git config --global credential.helper store`, puis écriture de `https://$GITHUB_ACTOR:<jeton>@github.com` dans `~/.git-credentials`.
2. `rm -rf .west`, `west init -l workdir`, `west update --narrow -o=--depth=1`.

## Dépendances

- Aucune.

## Points d'attention

- Le jeton est stocké en clair dans `~/.git-credentials` et reste dans le conteneur ou sur le runner après l'exécution.
- Le dossier du manifeste est codé en dur (`workdir`) : `workdir/west.yml` doit exister avant l'appel.
- L'entrée `personal_access_token` n'a pas de `description`.
