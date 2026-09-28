---
titre: Bibliothèque Zephyr (squelette)
---

# Bibliothèque Zephyr (squelette)

Squelette de workflow destiné aux bibliothèques Zephyr : en l'état, il affiche seulement « Hello world » et ne compile ni ne teste rien.

Fichier : `.github/workflows/lib.yml` · Déclencheur : `workflow_call` · Runner : `group: default`

## Utilisation

```yaml
jobs:
  zephyr-lib:
    uses: catie-aq/zephyr_workflows/.github/workflows/lib.yml@main
```

## Entrées

| Nom | Type | Description | Requis | Défaut |
| ------------ | ------- | ---------------------------------------- | ----- | ------------ |

Aucune.

## Secrets

| Nom | Description | Requis |
| ------------ | ---------------------------------------- | ----- |

Aucune.

## Sorties

| Nom | Description |
| ------------ | ---------------------------------------- |

Aucune.

## Fonctionnement

Job `build_and_test_ros2_package` (runner `group: default`) :

1. `echo "Hello world"`.

## Dépendances

- Aucune.

## Points d'attention

- Workflow vide : le nom « Build & Test Zephyr Lib » promet une compilation et des tests qui n'existent pas.
- Le nom du job, `build_and_test_ros2_package`, est hérité d'un workflow ROS 2.
- Seul workflow du dépôt sur le runner `group: default` ; les autres utilisent `sonu-github-arc`.
