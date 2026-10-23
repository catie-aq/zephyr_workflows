---
titre: Test d'un shield Zephyr
---

# Test d'un shield Zephyr

Compile l'exemple Zephyr `blinky` sur la carte `zest_core_stm32l4a6rg` avec le shield défini dans le dépôt appelant, pour vérifier que sa définition est valide. À utiliser dans le dépôt de définition d'un shield 6TRON.

Fichier : `.github/workflows/shield.yml` · Déclencheur : `workflow_call` · Runner : `sonu-github-arc`

## Utilisation

```yaml
name: "Zephyr Shield CI"
on:
  push:

jobs:
  zephyr-shield:
    uses: catie-aq/zephyr_workflows/.github/workflows/shield.yml@main
    with:
      shield: "zest_sensor_p_t_rh"
    secrets:
      personal_access_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
```

## Entrées

| Nom | Type | Description | Requis | Défaut |
| ------------ | ------- | ---------------------------------------- | ----- | ------------ |
| `shield` | string | Nom du shield passé à `west build --shield`. | oui | |
| `container` | string | Image Docker du job de compilation. | non | `ghcr.io/catie-aq/zephyr_docker:v4.4.0-202605-ci` |
| `zephyr_revision` | string | Révision de Zephyr (tag ou branche) écrite dans le manifeste `west.yml` ; à garder cohérente avec l'image `container`. | non | `v4.4.0` (aussi si chaîne vide) |
| `extra_cmd` | string | Commande exécutée en premier (description du code : « Extra command to run before build »). | non | `echo ''` |

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

Job `build` (runner `sonu-github-arc`, conteneur `${{ inputs.container }}` avec `--user root --privileged`, variable `CMAKE_PREFIX_PATH=/opt/toolchains`) :

1. `extra_cmd` exécutée (toujours, `echo ''` par défaut).
2. `tj-actions/branch-names@v8` : nom de la branche courante.
3. Génération de `workdir/west.yml` (script shell dans le workflow) : projet `zephyr` à `zephyr_revision` avec `name-allowlist` `cmsis`, `cmsis_6`, `hal_stm32` ; `zephyr_zest-core-stm32l4a6rg` et `zephyr_6tron-connector` en révision `main` ; le dépôt appelant à la branche courante.
4. `catie-aq/zephyr_workflows/zephyr_init@main` : `west init -l workdir` puis `west update`.
5. Transformation du nom du shield en majuscules, `-` remplacés par `_` (ex. `zest_sensor_p_t_rh` devient `ZEST_SENSOR_P_T_RH`), stockée dans `transformed_shield` via `$GITHUB_ENV`.
6. `catie-aq/zephyr_workflows/zephyr_build@main` avec `board: zest_core_stm32l4a6rg`, `application: zephyr/samples/basic/blinky`, `shield` et `overlay: <SHIELD>(1)` (contenu écrit dans `app.overlay` le temps de la compilation).

## Dépendances

- `catie-aq/generic_workflows/.github/workflows/pre-commit.yaml@main`
- `catie-aq/zephyr_workflows/zephyr_init@main`
- `catie-aq/zephyr_workflows/zephyr_build@main`
- `tj-actions/branch-names@v8` (action tierce)

## Points d'attention

- Carte (`zest_core_stm32l4a6rg`), exemple (`blinky`) et modules (`hal_stm32`) codés en dur : un shield n'est testé que sur cette carte STM32.
- Pas de `actions/checkout` : le shield testé est celui que `west update` récupère sur GitHub, à la branche courante, pas le commit exact de l'exécution.
- L'étape de transformation porte un `id: transform-shield` inutilisé (la valeur passe par `$GITHUB_ENV`).
- Le job `build` n'a pas de `needs: pre-commit` : les deux jobs tournent en parallèle.
- `tj-actions/branch-names` est une action tierce référencée par un tag mutable (`@v8`).
