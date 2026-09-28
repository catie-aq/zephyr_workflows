---
titre: Test d'une carte Zephyr
---

# Test d'une carte Zephyr

Lance les tests Twister de Zephyr sur une carte définie dans le dépôt appelant, filtrés par tags de périphériques. À utiliser dans le dépôt de définition d'une carte (`zephyr_<carte>`).

Fichier : `.github/workflows/board.yml` · Déclencheur : `workflow_call` · Runner : `sonu-github-arc`

## Utilisation

```yaml
name: "Zephyr Board CI"
on:
  push:

jobs:
  zephyr-board:
    uses: catie-aq/zephyr_workflows/.github/workflows/board.yml@main
    with:
      board: "zest_core_stm32l4a6rg"
    secrets:
      personal_access_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
```

## Entrées

| Nom | Type | Description | Requis | Défaut |
| ------------ | ------- | ---------------------------------------- | ----- | ------------ |
| `board` | string | Carte passée à Twister (`-p <board>`). | oui | |
| `container` | string | Image Docker du job Twister. | non | `ghcr.io/catie-aq/zephyr_docker:v4.4.0-202605-ci` |
| `tags` | string | Tags Twister séparés par des virgules (un `-t` par tag). | non | `DAC,ieee802154,counter,gpio,serial,i2c,i3c,UART,qspi,pwm,button,usb,spi,lora,i2s,mipi_dbi,wifi,ethernet,nvs,uart,dma,clock_control,usbc,watchdog,dac,w1,input,peci,can,bluetooth,adc,clock` |
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

Job `twister` (runner `sonu-github-arc`, conteneur `${{ inputs.container }}` avec `--user root --privileged`, variables `CMAKE_PREFIX_PATH=/opt/toolchains`, `ZEPHYR_VERSION=v4.4.0`, `TWISTER_OPTIONS=--force-color --inline-logs -v --clobber-output`) :

1. `extra_cmd` exécutée (toujours, `echo ''` par défaut).
2. `tj-actions/branch-names@v8` : nom de la branche courante.
3. `catie-aq/zephyr_workflows/generate_manifest@main` : `workdir/west.yml` avec Zephyr `v4.4.0`, le dépôt appelant à la branche courante et le manifeste `zephyr_6tron-manifest` (révision `main`) limité au module `6tron_connector`.
4. `catie-aq/zephyr_workflows/zephyr_init@main` : `west init -l workdir` puis `west update`.
5. `catie-aq/zephyr_workflows/zephyr_twister@main` avec `board`, `tags` et `TWISTER_OPTIONS`.

## Dépendances

- `catie-aq/generic_workflows/.github/workflows/pre-commit.yaml@main`
- `catie-aq/zephyr_workflows/generate_manifest@main`
- `catie-aq/zephyr_workflows/zephyr_init@main`
- `catie-aq/zephyr_workflows/zephyr_twister@main`
- `tj-actions/branch-names@v8` (action tierce)

## Points d'attention

- Pas de `actions/checkout` : le code testé est celui que `west update` récupère sur GitHub, à la branche courante (`catie-aq/<nom du dépôt>`), pas le commit exact de l'exécution. Une branche d'un fork n'existe pas chez `catie-aq`.
- La version de Zephyr (`ZEPHYR_VERSION: "v4.4.0"`) est codée en dur, sans entrée pour la changer ; elle doit rester cohérente avec l'image par défaut.
- Le job `twister` n'a pas de `needs: pre-commit` : les deux jobs tournent en parallèle.
- La liste de tags par défaut contient des doublons de casse (`DAC`/`dac`, `UART`/`uart`).
- `tj-actions/branch-names` est une action tierce référencée par un tag mutable (`@v8`) ; les dépendances internes sont en `@main`.
