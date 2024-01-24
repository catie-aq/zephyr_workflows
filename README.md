# Zephyr Workflows

Ce dépôt contient une collection de workflows réutilisables, spécifiquement conçus pour la construction et les tests de Zephyr, utilisables dans
le cadre d'Actions Github.

## Workflows Disponibles

### Application

Ce workflow applique les étapes suivantes :

- Vérification de pre-commit si le fichier `.pre-commit-config.yaml` est présent dans le dépôt
- Test de compilation de l'application avec les commandes suivantes :
  - `west init -l workdir`
  - `west update`
  - `west build -b <target>`

Le workflow possèdes les paramètres suivants :

- `container` : Image Docker à utiliser pour l'exécution des commandes. Par défaut : `zephyrprojectrtos/ci`
- `board` : Cible à utiliser pour la compilation. **Obligatoire**.
- `application` : Nom de l'application à compiler. **Obligatoire**.
- `extra_cmd` : Commandes supplémentaires à exécuter avant la compilation. Par défaut : ``
- `personal_access_token` : Token d'accès personnel (PAT) à utiliser pour cloner les dépôts privés. **Obligatoire**.

## Utilisation

Vous pouvez utiliser ce workflow dans votre dépôt en ajoutant le bloc de code suivant à votre fichier `.github/workflows/<name>.yml` :

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

Remarque : Vous pouvez également utiliser un tag spécifique pour le workflow, par exemple `application.yml@v1.0.0`.
Voir les [releases displonibles](https://github.com/catie-aq/zephyr_workflows/releases).

## Licence

Ce projet est sous licence Apache 2.0, une licence open source permissive qui vous permet d'utiliser, de modifier, de distribuer et de vendre
librement vos propres produits qui incluent ce logiciel. Le texte intégral de la licence peut être obtenu sur
le [site web d'Apache](https://www.apache.org/licenses/LICENSE-2.0).
