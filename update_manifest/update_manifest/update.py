import click
import yaml
import requests


class UpdateManifest:
    def __init__(self, token, manifest):
        self.token = token
        self.manifest = manifest
        self.to_check = {}

    def parse_manifest(self):
        with open(self.manifest, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            for project in data["manifest"]["projects"]:
                self.to_check[project["name"]] = {
                    "repo-path": project["repo-path"],
                    "revision": project["revision"],
                }

    def get_remote_revisions(self):
        headers = {"Authorization": f"token {self.token}"}
        for project, details in self.to_check.items():
            repo_path = details["repo-path"]
            local_revision = details["revision"]

            # Get repository information
            repo_info_response = requests.get(
                f"https://api.github.com/repos/catie-aq/{repo_path}", headers=headers
            )
            repo_info_response.raise_for_status()
            default_branch = repo_info_response.json()["default_branch"]

            # Get the latest commit of the default branch
            response = requests.get(
                f"https://api.github.com/repos/catie-aq/{repo_path}/commits/{default_branch}",
                headers=headers,
            )
            response.raise_for_status()
            remote_revision = response.json()["sha"]

            if local_revision == remote_revision:
                print(f"The local revision of {project} is the latest.")
            else:
                print(
                    f"The local revision of {project} is not the latest. The latest revision is {remote_revision}."
                )
                self.to_check[project]["revision"] = remote_revision

    def update_manifest(self):
        content = ""
        with open(self.manifest, "r", encoding="utf-8") as f:
            content = f.read()
            data = yaml.safe_load(content)
            for project in data["manifest"]["projects"]:
                new_revision = self.to_check[project["name"]]["revision"]
                content = content.replace(
                f"{project['revision']}",
                f"{new_revision}"
                )
        with open(self.manifest, "w", encoding="utf-8") as f:
            f.write(content)
                


    def update(self):
        print(f"Updating manifest {self.manifest}")
        self.parse_manifest()
        self.get_remote_revisions()
        self.update_manifest()


@click.command()
@click.option("--token", help="The token to use")
@click.option("--manifest", help="The path to the manifest to update")
def main(token, manifest):
    update = UpdateManifest(token, manifest)
    update.update()


if __name__ == "__main__":
    main()
