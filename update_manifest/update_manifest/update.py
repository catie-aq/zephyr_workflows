"""
This module provides a class for updating a manifest file with the latest revisions of GitHub.

Usage:
    python update.py --token <github_token> --manifest <manifest_path>

Arguments:
    --token (str): The GitHub token to use for authentication.
    --manifest (str): The path to the manifest file to update.

Example:
    python update.py --token abcdef123456 --manifest /path/to/manifest.yaml
"""

import click
import requests
import yaml


class UpdateManifest:
    """
    A class to update a manifest file with the latest revisions of GitHub.
    """

    def __init__(self, token, manifest):
        self.token = token
        self.manifest = manifest
        self.to_check = {}

    def parse_manifest(self):
        """
        Parse the manifest file and store the projects to check in the `to_check` dictionary.
        Each project is represented by its name and contains the repository path and revision.
        """
        with open(self.manifest, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            for project in data["manifest"]["projects"]:
                self.to_check[project["name"]] = {
                    "repo-path": project["repo-path"],
                    "revision": project["revision"],
                }

    def get_remote_revisions(self):
        """
        Get the latest revisions of the repositories in the `to_check` dictionary from the GitHub.
        If a local revision is different from the remote revision, update revision in `to_check`.
        """
        headers = {"Authorization": f"token {self.token}"}
        for project, details in self.to_check.items():
            repo_path = details["repo-path"]
            local_revision = details["revision"]

            repo_info_response = requests.get(
                f"https://api.github.com/repos/catie-aq/{repo_path}",
                headers=headers,
                timeout=5,
            )
            repo_info_response.raise_for_status()
            default_branch = repo_info_response.json()["default_branch"]

            response = requests.get(
                f"https://api.github.com/repos/catie-aq/{repo_path}/commits/{default_branch}",
                headers=headers,
                timeout=5,
            )
            response.raise_for_status()
            remote_revision = response.json()["sha"]

            if local_revision != remote_revision:
                print(
                    f"- Bumps [catie-aq/{repo_path}](https://github.com/catie-aq/{repo_path}) "
                    f"from {local_revision} to {remote_revision}. \n"
                )
                self.to_check[project]["revision"] = remote_revision

    def update_manifest(self):
        """
        Update the manifest file with the latest revisions from the `to_check` dictionary.
        """
        content = ""
        with open(self.manifest, "r", encoding="utf-8") as f:
            content = f.read()
            data = yaml.safe_load(content)
            for project in data["manifest"]["projects"]:
                new_revision = self.to_check[project["name"]]["revision"]
                content = content.replace(f"{project['revision']}", f"{new_revision}")
        with open(self.manifest, "w", encoding="utf-8") as f:
            f.write(content)

    def update(self):
        """
        Update the manifest file with the latest revisions of the repositories.
        """
        self.parse_manifest()
        self.get_remote_revisions()
        self.update_manifest()


@click.command()
@click.option("--token", help="The token to use")
@click.option("--manifest", help="The path to the manifest to update")
def main(token, manifest):
    """
    Update the manifest file with the latest revisions of the repositories.
    """
    update = UpdateManifest(token, manifest)
    update.update()


if __name__ == "__main__":
    main(token="abcdef123456", manifest="/path/to/manifest.yaml")
