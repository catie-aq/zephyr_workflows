---
titre: Tests Twister Zephyr (action)
---

# Tests Twister Zephyr (action)

Lance `west twister` avec des tags, une carte, un dossier de tests et des options facultatifs. À placer après `zephyr_init`, dans un conteneur qui fournit `west` et la chaîne de compilation.

Fichier : `zephyr_twister/action.yml` · Type : action composite

## Utilisation

```yaml
steps:
  - uses: catie-aq/zephyr_workflows/zephyr_twister@main
    with:
      board: zest_core_stm32l4a6rg
      tags: "gpio,i2c,spi"
      options: "--inline-logs -v"
```

## Entrées

| Nom | Type | Description | Requis | Défaut |
| ------------ | ------- | ---------------------------------------- | ----- | ------------ |
| `tags` | string | Tags Twister séparés par des virgules (un `-t <tag>` par tag). | non | |
| `options` | string | Options ajoutées en fin de commande Twister. | non | `""` |
| `board` | string | Plateforme de test (`-p <board>`). | non | |
| `path` | string | Dossier des tests (`-T <path>`). | non | |

## Sorties

| Nom | Description |
| ------------ | ---------------------------------------- |

Aucune.

## Fonctionnement

Une étape `bash` : construction des arguments `-t`, `-p` et `-T` à partir des entrées renseignées, puis `west twister $test $board $path <options>`.

## Dépendances

- Aucune.

## Points d'attention

- `type: string` sur les entrées n'est pas une clé reconnue par GitHub pour une action composite ; elle est ignorée.
- Les variables shell `test`, `board` et `path` ne sont pas initialisées quand l'entrée correspondante est vide : une variable d'environnement de même nom serait reprise dans la commande.
- Les entrées sont insérées sans guillemets dans la commande shell.
