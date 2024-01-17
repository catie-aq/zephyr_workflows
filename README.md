# Zephyr Workflows

Ce dépôt contient une collection de workflows réutilisables, spécifiquement conçus pour la construction et les tests de Zephyr, utilisables dans
le cadre d'Actions Github.

## Workflows Disponibles

TODO

## Utilisation

Vous pouvez utiliser ce workflow dans votre dépôt en ajoutant le bloc de code suivant à votre fichier `.github/workflows/<name>.yml` :

```yaml
name: "Zephyr Application CI/CD"
on:
  push:

jobs:
  ros:
    uses: catie-aq/zephyr_workflows/.github/workflows/application.yml@main
```

Remarque : Vous pouvez également utiliser un tag spécifique pour le workflow, par exemple `application.yml@v1.0.0`.
Voir les [releases displonibles](https://github.com/catie-aq/zephyr_workflows/releases).

## Licence

Ce projet est sous licence Apache 2.0, une licence open source permissive qui vous permet d'utiliser, de modifier, de distribuer et de vendre
librement vos propres produits qui incluent ce logiciel. Le texte intégral de la licence peut être obtenu sur
le [site web d'Apache](https://www.apache.org/licenses/LICENSE-2.0).