---
titre: Compilation d'une application Zephyr
---

# Compilation d'une application Zephyr

Compile une application Zephyr dans un conteneur Zephyr, avec signature MCUboot, téléchargement de blobs et publication d'un artefact en option. À utiliser dans le dépôt d'une application qui porte son propre manifeste `west.yml` à la racine.

Fichier : `.github/workflows/application.yml` · Déclencheur : `workflow_call` · Runner : `sonu-github-arc`

## Utilisation

```yaml
name: "Zephyr Application CI/CD"
on:
  push:

jobs:
  zephyr-application:
    uses: catie-aq/zephyr_workflows/.github/workflows/application.yml@main
    with:
      board: "zest_core_stm32l4a6rg"
      application: "hello_world"
      artifact: "build/zephyr/zephyr.hex"
    secrets:
      personal_access_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
```

Le dépôt appelant doit contenir un `west.yml` à sa racine (utilisé par `west init -l`) et un `.pre-commit-config.yaml` (job `pre-commit`).

## Entrées

| Nom | Type | Description | Requis | Défaut |
| ------------------ | ------- | ---------------------------------------- | ----- | ------------ |
| `application` | string | Chemin de l'application à compiler, relatif à la racine du dépôt. | oui | |
| `blobs` | string | Arguments de `west blobs fetch` (ex. `hal_espressif`) ; étape sautée si vide. | non | |
| `board` | string | Carte cible passée à `west build -b` ; sans carte, `west build` sans `-b`. | non | |
| `build_extra_args` | string | Arguments ajoutés en fin de `west build` (ex. `-- -DCONFIG_...=y`). | non | |
| `container` | string | Image Docker du job de compilation. | non | `ghcr.io/catie-aq/zephyr_docker:v4.4.0-202605-ci` |
| `pem_key_path` | string | Chemin, relatif au dépôt, où écrire la clé de signature MCUboot `pem_key` ; active la signature. | non | |
| `extra_cmd` | string | Commande exécutée avant toute autre étape (description du code : « Extra command to run before build »). | non | |
| `artifact` | string | Chemin du ou des fichiers à publier comme artefact ; aucun artefact si vide. | non | |

## Secrets

| Nom | Description | Requis |
| ------------------------- | ---------------------------------------- | ----- |
| `personal_access_token` | Jeton d'accès personnel GitHub utilisé par `west update` pour cloner les dépôts privés du manifeste. | oui |
| `pem_key` | Contenu de la clé PEM de signature MCUboot, écrite dans `pem_key_path`. | non |

## Sorties

| Nom | Description |
| ------------ | ---------------------------------------- |

Aucune.

## Fonctionnement

Job `pre-commit` : appel de `catie-aq/generic_workflows/.github/workflows/pre-commit.yaml@main` (`pre-commit run --all-files`).

Job `build` (runner `sonu-github-arc`, conteneur `${{ inputs.container }}` avec `--user root --privileged`, variable `CMAKE_PREFIX_PATH=/opt/toolchains`) :

1. `extra_cmd` exécutée si elle est renseignée.
2. `actions/checkout@v4` dans le dossier `workdir`.
3. Si `pem_key_path` est renseigné : écriture du secret `pem_key` dans `workdir/<pem_key_path>`, puis remplacement de `CONFIG_MCUBOOT_SIGNATURE_KEY_FILE` dans `workdir/<application>/prj.conf` par ce chemin (`sed`).
4. `catie-aq/zephyr_workflows/zephyr_init@main` : identifiants Git et `west init -l workdir` puis `west update`.
5. `west blobs fetch <blobs>` si `blobs` est renseigné.
6. `catie-aq/zephyr_workflows/zephyr_build@main` avec `application: workdir/<application>`, `board` et `extra_args: <build_extra_args>`.
7. Calcul du nom d'artefact : `application` dont les `/` sont remplacés par `_`.
8. `actions/upload-artifact@v4` si `artifact` est renseigné, sous ce nom.

## Dépendances

- `catie-aq/generic_workflows/.github/workflows/pre-commit.yaml@main`
- `catie-aq/zephyr_workflows/zephyr_init@main`
- `catie-aq/zephyr_workflows/zephyr_build@main`

## Points d'attention

- Le nom d'artefact est produit par `echo "::set-output name=application::..."`, syntaxe dépréciée par GitHub (remplacée par `$GITHUB_OUTPUT`).
- Le job `build` n'a pas de `needs: pre-commit` : les deux jobs tournent en parallèle et un échec de pre-commit n'empêche pas la compilation.
- Le job `pre-commit` n'a aucune condition sur la présence de `.pre-commit-config.yaml` (l'ancien README disait le contraire).
- La clé `pem_key` est écrite par `echo "${{ secrets.pem_key }}"` : le secret est interpolé directement dans le script shell.
- L'étape `replace` suppose que `workdir/<application>/prj.conf` existe et contient déjà une ligne `CONFIG_MCUBOOT_SIGNATURE_KEY_FILE=`.
- Les dépendances internes sont référencées par `@main` et non par un tag.
