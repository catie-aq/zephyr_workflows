---
titre: Zephyr Workflows
---

# Zephyr Workflows

Ce dépôt contient des workflows GitHub Actions réutilisables et des actions composites pour compiler et tester des applications, cartes, drivers et shields Zephyr. Vue d'ensemble de tous les workflows `catie-aq` : dépôt `catie-aq/sonu_workflow` (REF-001).

## Workflows réutilisables

| Workflow | Rôle | Doc |
| -------------------- | ---------------------------------------- | ---- |
| `application.yml` | Compile une application Zephyr (signature MCUboot, blobs, artefact en option). | [Compilation d'une application Zephyr](docs/application.md) |
| `board.yml` | Lance Twister sur une carte, filtré par tags de périphériques. | [Test d'une carte Zephyr](docs/board.md) |
| `driver.yml` | Assemble un manifeste avec les cartes demandées et lance Twister en mode intégration. | [Test d'un driver Zephyr](docs/driver.md) |
| `lib.yml` | Squelette : affiche « Hello world », ne compile rien. | [Bibliothèque Zephyr (squelette)](docs/lib.md) |
| `shield.yml` | Compile `blinky` sur `zest_core_stm32l4a6rg` avec le shield du dépôt. | [Test d'un shield Zephyr](docs/shield.md) |

## Actions composites

| Action | Rôle | Doc |
| -------------------- | ---------------------------------------- | ---- |
| `generate_manifest` | Écrit `workdir/west.yml` (Zephyr, dépôt courant, manifeste 6TRON en option). | [generate_manifest](generate_manifest/README.md) |
| `update_manifest` | Met à jour les révisions d'un manifeste et publie les changements en artefacts. | [update_manifest](update_manifest/README.md) |
| `zephyr_build` | Compile une application avec `west build` (carte, shield, overlay). | [zephyr_build](zephyr_build/README.md) |
| `zephyr_init` | Configure les identifiants Git, puis `west init -l workdir` et `west update`. | [zephyr_init](zephyr_init/README.md) |
| `zephyr_twister` | Lance `west twister` (tags, carte, dossier, options). | [zephyr_twister](zephyr_twister/README.md) |

## Licence

Ce projet est sous licence Apache 2.0, une licence open source permissive qui vous permet d'utiliser, de modifier, de distribuer et de vendre
librement vos propres produits qui incluent ce logiciel. Le texte intégral de la licence peut être obtenu sur
le [site web d'Apache](https://www.apache.org/licenses/LICENSE-2.0).
