---
titre: Compilation Zephyr (action)
---

# Compilation Zephyr (action)

Compile une application Zephyr avec `west build`, avec carte, shield, arguments et overlay en option. À placer après `zephyr_init`, dans un conteneur qui fournit `west` et la chaîne de compilation.

Fichier : `zephyr_build/action.yml` · Type : action composite

## Utilisation

```yaml
steps:
  - uses: catie-aq/zephyr_workflows/zephyr_build@main
    with:
      application: workdir/hello_world
      board: zest_core_stm32l4a6rg
```

## Entrées

| Nom | Type | Description | Requis | Défaut |
| ------------- | ------- | ---------------------------------------- | ----- | ------------ |
| `application` | string | Chemin de l'application à compiler. | oui | |
| `board` | string | Carte cible (`-b`) ; omise si vide. | non | `""` |
| `shield` | string | Shield (`--shield`) ; omis si vide. | non | `""` |
| `extra_args` | string | Arguments ajoutés en fin de commande, après `-p`. | non | `""` |
| `overlay` | string | Contenu écrit dans `<application>/app.overlay` pendant la compilation, puis supprimé. | non | `""` |

## Sorties

| Nom | Description |
| ------------ | ---------------------------------------- |

Aucune. Le résultat de la compilation reste dans le dossier `build/` du répertoire courant.

## Fonctionnement

Étapes (toutes en `bash`) :

1. Si `overlay` est renseigné : `echo "<overlay>" > <application>/app.overlay`.
2. Une seule des quatre commandes suivantes, selon `board` et `shield` :
   - `west build -b <board> --shield <shield> <application> -p <extra_args>` ;
   - `west build -b <board> <application> -p <extra_args>` ;
   - `west build --shield <shield> <application> -p <extra_args>` ;
   - `west build <application> -p <extra_args>`.
3. Si `overlay` est renseigné : suppression de `<application>/app.overlay`.

## Dépendances

- Aucune.

## Points d'attention

- `type: string` sur les entrées n'est pas une clé reconnue par GitHub pour une action composite (toutes les entrées sont des chaînes) ; elle est ignorée.
- L'overlay écrase un `app.overlay` existant de l'application, puis le supprime.
- La suppression de l'overlay n'a pas de `if: always()` : si la compilation échoue, `app.overlay` reste en place.
- `extra_args` suit directement `-p`, qui accepte une valeur facultative (`auto`, `always`, `never`) : un premier argument de cette forme serait lu comme valeur de `-p`.
- Les entrées sont insérées sans guillemets dans les commandes shell.
