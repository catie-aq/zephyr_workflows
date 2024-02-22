# Zephyr Workflows

Ce dépôt contient une collection de workflows réutilisables, spécifiquement conçus pour la construction et les tests de Zephyr, utilisables dans
le cadre d'Actions Github.

## Workflows Disponibles

### Application

Ce workflow applique les étapes suivantes :

- Vérification de pre-commit si le fichier `.pre-commit-config.yaml` est présent dans le dépôt
- Test de compilation de l'application en utilisant l'action Zephyr Build
Le workflow possède les paramètres suivants :

- `container` : Image Docker à utiliser pour l'exécution des commandes. Par défaut : `zephyrprojectrtos/ci`
- `board` : Cible à utiliser pour la compilation.
- `application` : Chemin de l'application à compiler. **Obligatoire**.
- `extra_cmd` : Commandes supplémentaires à exécuter avant la compilation. Par défaut : ``
- `personal_access_token` : Token d'accès personnel (PAT) à utiliser pour cloner les dépôts privés. **Obligatoire**.

| Input                   | Description                                                             | Obligatoire | Default                |
| ----------------------- | ----------------------------------------------------------------------- | ----------- | ---------------------- |
| `container`             | Image Docker à utiliser pour l'exécution des commandes.                 | Non         | `zephyrprojectrtos/ci` |
| `board`                 | Cible à utiliser pour la compilation.                                   | Non         |                        |
| `application`           | Chemin de l'application à compiler.                                     | Oui         |                        |
| `extra_cmd`             | Commandes supplémentaires à exécuter avant la compilation.              | Non         | ``                     |
| `personal_access_token` | Token d'accès personnel (PAT) à utiliser pour cloner les dépôts privés. | Oui         |                        |

```yaml
name: "Zephyr Application CI/CD"
on:
  push:

jobs:
  ros:
    uses: catie-aq/zephyr_workflows/.github/workflows/application.yml@main
    with:
      board: "zest_core_stm32l4a6rg"
      application: "hello_world"
    secrets:
      personal_access_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
```

### Driver

Ce workflow applique les étapes suivantes :

- Vérification de pre-commit si le fichier `.pre-commit-config.yaml` est présent dans le dépôt
- Génération du fichier `west.yml` pour le projet Zephyr en utilisant l'action Generate Zephyr Manifest
- Test de compilation du driver en utilisant l'action Zephyr Build

| Input                   | Description                                                             | Obligatoire | Default                          |
| ----------------------- | ----------------------------------------------------------------------- | :---------: | -------------------------------- |
| `application`           | Chemin de l'application à compiler.                                     |     Non     | `"samples"`                      |
| `board`                 | Cible à utiliser pour la compilation.                                   |     Non     | `"zest_core_stm32l4a6rg"`        |
| `repo_board`            | Le nom du tableau du dépôt.                                             |     Non     | `"zephyr_zest-core-stm32l4a6rg"` |
| `container`             | Image Docker à utiliser pour l'exécution des commandes.                 |     Non     | `"zephyrprojectrtos/ci"`         |
| `extra_cmd`             | Commandes supplémentaires à exécuter avant la compilation.              |     Non     | ``                               |
| `personal_access_token` | Token d'accès personnel (PAT) à utiliser pour cloner les dépôts privés. |     Oui     |                                  |

```yaml
name: "Zephyr Driver CI/CD"

on: [push, workflow_dispatch]

jobs:
  zephyr-driver:
    uses: catie-aq/zephyr_workflows/.github/workflows/driver.yml@main
    with:
      zephyr_revision: 'v3.4.0'
    secrets:
      personal_access_token: ${{ secrets.PAT }}
```

## Actions Disponibles

### Zephyr Build

Cette action permet de compiler une application Zephyr. Elle prend en charge les paramètres suivants :

| Input                   | Description                                                             | Obligatoire | Default |
| ----------------------- | ----------------------------------------------------------------------- | ----------- | ------- |
| `board`                 | Cible à utiliser pour la compilation.                                   | Non         |         |
| `application`           | Chemin de l'application à compiler.                                     | Oui         |         |
| `personal_access_token` | Token d'accès personnel (PAT) à utiliser pour cloner les dépôts privés. | Oui         |         |

### Generate Zephyr Manifest

Cette action génère un fichier `west.yml` pour le projet Zephyr.

| Input                 | Description                                                         | Obligatoire | Default |
| --------------------- | ------------------------------------------------------------------- | ----------- | ------- |
| `zephyr_revision`     | La révision (comme un tag ou un nom de branche) du projet Zephyr.   | Oui         |         |
| `6tron_revision`      | La révision (comme un tag ou un nom de branche) du manifest Zephyr. | Oui         |         |
| `repository_revision` | La révision du dépôt.                                               | Oui         |         |
| `repo_board`          | Le nom du tableau du dépôt.                                         | Oui         |         |

## Licence

Ce projet est sous licence Apache 2.0, une licence open source permissive qui vous permet d'utiliser, de modifier, de distribuer et de vendre
librement vos propres produits qui incluent ce logiciel. Le texte intégral de la licence peut être obtenu sur
le [site web d'Apache](https://www.apache.org/licenses/LICENSE-2.0).
