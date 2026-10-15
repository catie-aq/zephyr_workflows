---
titre: Test d'un driver Zephyr
---

# Test d'un driver Zephyr

Génère un manifeste `west.yml` qui assemble Zephyr, les cartes demandées, le connecteur 6TRON et le dépôt du driver, puis lance Twister en mode intégration sur ses exemples. À utiliser dans le dépôt d'un driver ou d'un module Zephyr.

Fichier : `.github/workflows/driver.yml` · Déclencheur : `workflow_call` · Runner : `sonu-github-arc`

## Utilisation

```yaml
name: "Zephyr Driver CI/CD"

on: [push, workflow_dispatch]

jobs:
  zephyr-driver:
    uses: catie-aq/zephyr_workflows/.github/workflows/driver.yml@main
    with:
      boards: "zest_core_stm32l4a6rg,zest_core_nrf5340"
      zephyr_modules: "hal_stm32,hal_nordic"
    secrets:
      personal_access_token: ${{ secrets.PAT }}
```

## Entrées

| Nom | Type | Description | Requis | Défaut |
| ---------------- | ------- | ---------------------------------------- | ----- | ------------ |
| `boards` | string | Cartes séparées par des virgules ; chacune ajoute le dépôt `zephyr_<carte>` (les `_` deviennent `-`) au manifeste. | non | `zest_core_stm32l4a6rg` |
| `shields` | string | Shields séparés par des virgules ; chacun ajoute le dépôt `zephyr_<shield>` (les `_` deviennent `-`) au manifeste. | non | `""` |
| `container` | string | Image Docker du job Twister. | non | `ghcr.io/catie-aq/zephyr_docker:v4.4.0-202605-ci` |
| `zephyr_version` | string | Révision de Zephyr (tag ou branche) écrite dans le manifeste `west.yml` ; à garder cohérente avec l'image `container`. | non | `v4.4.0` |
| `extra_cmd` | string | Commande exécutée en premier si elle est renseignée (description du code : « Extra command to run before build »). | non | `""` |
| `path` | string | Dossier des tests, relatif au dépôt du driver (`-T <dépôt>/<path>`). | non | `samples` |
| `zephyr_modules` | string | Modules Zephyr ajoutés à la `name-allowlist`, séparés par des virgules (ex. `cmsis,cmsis_6,hal_stm32`). | non | `hal_stm32` |
| `has_manifest` | boolean | Ajoute `import: true` au projet du driver pour importer son propre `west.yml`. | non | `false` |

## Secrets

| Nom | Description | Requis |
| ------------------------- | ---------------------------------------- | ----- |
| `personal_access_token` | Jeton d'accès personnel GitHub utilisé par `west update` pour cloner les dépôts privés. | oui |

## Sorties

| Nom | Description |
| ------------ | ---------------------------------------- |

Aucune.

## Fonctionnement

Job `pre-commit` : appel de `catie-aq/generic_workflows/.github/workflows/pre-commit.yaml@main`.

Job `twister` (runner `sonu-github-arc`, conteneur `${{ inputs.container }}` sans option, variables `CMAKE_PREFIX_PATH=/opt/toolchains`, `TWISTER_OPTIONS=--force-color --inline-logs -v --clobber-output --integration`) :

1. `extra_cmd` exécutée si elle est renseignée.
2. `tj-actions/branch-names@v8` : nom de la branche courante.
3. Génération de `workdir/west.yml` (script shell dans le workflow, sans l'action `generate_manifest`) :
   - remotes `zephyrproject-rtos` (`https://github.com/zephyrproject-rtos`) et `catie-6tron` (`https://github.com/catie-aq`) ;
   - projet `zephyr` à `zephyr_version`, `name-allowlist` : `cmsis`, `cmsis_6` puis chaque module de `zephyr_modules` ;
   - un projet `zephyr_<carte>` (révision `main`) par carte de `boards` ;
   - un projet `zephyr_<shield>` (révision `main`) par shield de `shields` ;
   - `zephyr_6tron-connector` (révision `main`) ;
   - le dépôt appelant (`github.event.repository.name`) à la branche courante, avec `import: true` si `has_manifest` vaut `true`.
4. `catie-aq/zephyr_workflows/zephyr_init@main` : `west init -l workdir` puis `west update`.
5. `catie-aq/zephyr_workflows/zephyr_twister@main` avec `path: <dépôt>/<path>` et `TWISTER_OPTIONS` (sans carte ni tags : Twister retient les plateformes d'intégration déclarées par les tests).

## Dépendances

- `catie-aq/generic_workflows/.github/workflows/pre-commit.yaml@main`
- `catie-aq/zephyr_workflows/zephyr_init@main`
- `catie-aq/zephyr_workflows/zephyr_twister@main`
- `tj-actions/branch-names@v8` (action tierce)

## Points d'attention

- Pas de `actions/checkout` : le driver testé est celui que `west update` récupère sur GitHub, à la branche courante (`catie-aq/<nom du dépôt>`), pas le commit exact de l'exécution.
- Contrairement aux autres workflows du dépôt : pas de bloc `permissions: read-all`, et conteneur lancé sans `--user root --privileged`.
- `boards` ne sert qu'à ajouter les dépôts de cartes au manifeste ; il n'est pas passé à Twister.
- Le manifeste est généré ici par un script propre, distinct de l'action `generate_manifest` (allowlist au lieu de blocklist) : deux logiques à maintenir.
- Le job `twister` n'a pas de `needs: pre-commit` : les deux jobs tournent en parallèle.
- `tj-actions/branch-names` est une action tierce référencée par un tag mutable (`@v8`).
