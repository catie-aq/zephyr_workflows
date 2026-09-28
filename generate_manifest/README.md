---
titre: Génération d'un manifeste Zephyr
---

# Génération d'un manifeste Zephyr

Écrit un manifeste `workdir/west.yml` qui assemble Zephyr (sans les HAL listées en blocklist), le dépôt courant et, en option, le manifeste 6TRON. À placer avant `zephyr_init`, qui fait `west init -l workdir`.

Fichier : `generate_manifest/action.yml` · Type : action composite

## Utilisation

```yaml
steps:
  - uses: catie-aq/zephyr_workflows/generate_manifest@main
    with:
      zephyr_revision: "v4.3.0"
      repository_revision: ${{ github.ref_name }}
      sixtron_connector_revision: "main"
```

## Entrées

| Nom | Type | Description | Requis | Défaut |
| ---------------------------- | ------- | ---------------------------------------- | ----- | ------------ |
| `sixtron_revision` | string | Révision du manifeste 6TRON (`zephyr_6tron-manifest`) à importer ; rien n'est ajouté si vide. | non | |
| `sixtron_module_allowlist` | string | Modules du manifeste 6TRON à importer, séparés par des virgules ; import complet (`import: true`) si vide. | non | |
| `zephyr_revision` | string | Révision de Zephyr (tag ou branche). | non | |
| `repository_revision` | string | Révision du dépôt courant (`github.event.repository.name`) ajouté au manifeste. | oui | |
| `repo_board` | string | Dépôt de carte (déclaré, non utilisé par l'action). | non | |
| `sixtron_connector_revision` | string | Révision du manifeste 6TRON importé uniquement pour le module `6tron_connector` ; rien n'est ajouté si vide. | non | |

## Sorties

| Nom | Description |
| ------------ | ---------------------------------------- |

Aucune. Le résultat est le fichier `workdir/west.yml`.

## Fonctionnement

Étapes (toutes en `bash`) :

1. Création de `workdir/west.yml`.
2. En-tête du manifeste : remotes `zephyrproject-rtos` (`https://github.com/zephyrproject-rtos`) et `catie-6tron` (`https://github.com/catie-aq`) ; projet `zephyr` à `zephyr_revision` avec une `name-blocklist` de HAL (`hal_altera`, `hal_ambiq`, `hal_atmel`, `hal_espressif`, `hal_ethos_u`, `hal_gigadevice`, `hal_infineon`, `hal_intel`, `hal_microchip`, `hal_nuvoton`, `hal_nxp`, `hal_openisa`, `hal_quicklogic`, `hal_renesas`, `hal_rpi_pico`, `hal_silabs`, `hal_st`, `hal_telink`, `hal_ti`, `hal_wurthelektronik`, `hal_xtensa`).
3. Si `repository_revision` est renseigné : projet `<nom du dépôt courant>` (remote `catie-6tron`) à cette révision.
4. Si `sixtron_revision` est renseigné et `sixtron_module_allowlist` vide : projet `6tron-manifest` (dépôt `zephyr_6tron-manifest`, chemin `6tron/6tron-manifest`) avec `import: true`.
5. Si `sixtron_revision` et `sixtron_module_allowlist` sont renseignés : même projet avec `import.name-allowlist` limité aux modules listés.
6. Si `sixtron_connector_revision` est renseigné : projet `6tron_manifest` (dépôt `zephyr_6tron-manifest`, chemin `6tron/6tron_manifest`) avec `name-allowlist: [6tron_connector]`.

## Dépendances

- Aucune.

## Points d'attention

- `repo_board` est déclaré mais jamais lu.
- `zephyr_revision` est facultatif sans défaut : s'il manque, le manifeste contient `revision:` vide.
- `sixtron_revision` et `sixtron_connector_revision` ensemble ajoutent deux projets (`6tron-manifest` et `6tron_manifest`) pointant vers le même dépôt `zephyr_6tron-manifest`, dans deux chemins différents.
- La condition `if: ${{ inputs.repository_revision }}` de l'étape 3 est toujours vraie puisque l'entrée est requise.
- L'ancien README citait les entrées `6tron_revision` et `repo_board` comme requises ; le code utilise `sixtron_revision` et seule `repository_revision` est requise.
- Les workflows `driver.yml` et `shield.yml` n'utilisent pas cette action : ils génèrent leur manifeste par un script propre (allowlist).
