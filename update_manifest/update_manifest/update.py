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
                    "path": project["path"],
                }

    def get_remote_revisions(self):
        """
        Get the latest revisions of the repositories in the `to_check` dictionary from the GitHub.
        If a local revision is different from the remote revision, update revision in `to_check`.
        """
        headers = {"Authorization": f"token {self.token}"}
        to_change = []
        for project, details in self.to_check.items():
            repo_path = details["repo-path"]
            local_revision = details["revision"]
            path = details["path"]

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
                to_change.append((repo_path, local_revision, remote_revision, path))
                self.to_check[project]["revision"] = remote_revision

        with open("change.md", "w", encoding="utf-8") as f:
            with open("matrix.json", "w", encoding="utf-8") as f_json:
                f_json.write('{ \n "repo": [\n')
                for repo_path, local_revision, remote_revision, path in to_change:
                    f.write(
                        f"- Bumps [catie-aq/{repo_path}](https://github.com/catie-aq/{repo_path}) "
                        f"from {local_revision} to {remote_revision}.\n"
                    )
                    if "core" not in repo_path:
                        f_json.write(f'"{path}",\n')

                f_json.write("]}\n")
            with open("matrix_core.json", "w", encoding="utf-8") as f_json:
                f_json.write('{ \n "repo": [\n')
                for repo_path, local_revision, remote_revision, path in to_change:
                    f.write(
                        f"- Bumps [catie-aq/{repo_path}](https://github.com/catie-aq/{repo_path}) "
                        f"from {local_revision} to {remote_revision}.\n"
                    )
                    if "core" in repo_path:
                        f_json.write(f'"{path}",\n')

                f_json.write("]}\n")

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

    def generate_test_manifest(self):
        with open(self.manifest, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Add new remote
        new_remote = {
            "name": "zephyrproject-rtos",
            "url-base": "https://github.com/zephyrproject-rtos",
        }
        data["manifest"]["remotes"].insert(0, new_remote)
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(
            "https://api.github.com/repos/zephyrproject-rtos/zephyr/releases/latest",
            headers=headers,
            timeout=5,
        )
        rev = response.json()["tag_name"]
        # Add new project
        new_project = {
            "name": "zephyr",
            "remote": "zephyrproject-rtos",
            "revision": rev,
            "import": True,
        }
        data["manifest"]["projects"].insert(0, new_project)
        with open("test_manifest.yml", "w", encoding="utf-8") as f:
            yaml.dump(data, f)

    def update(self):
        """
        Update the manifest file with the latest revisions of the repositories.
        """
        self.parse_manifest()
        self.get_remote_revisions()
        self.update_manifest()
        self.generate_test_manifest()


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
