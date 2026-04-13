#!/usr/bin/env python3

import os
import sys

project_name = "Hermes Agent"

repo_owner = "NousResearch"

repo_name = "hermes-agent"

docs_url = "https://hermes-agent.nousresearch.com/docs"

version_file = "hermes-agent_version"

debian_codename = "trixie"

debian_version = "13.4"

docker_arches = (
    "linux/amd64",
    "linux/arm64",
)

docker_repo = "sirmark/hermes-agent"

def tags():
    return (
        "latest",
        f"{repo_version}",
        f"{repo_version}-{debian_codename}",
        f"{repo_version}-{debian_codename}{debian_version}",
        f"{debian_codename}{debian_version}",
        f"{debian_codename}",
    )

def read_file(file):
    with open(file, "r") as f:
        return f.read()

def write_file(file, contents):
    dir = os.path.dirname(file)
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
    with open(file, "w") as f:
        f.write(contents)

def update_ci():
    file = "ci-matrix.yaml"
    config = read_file(file)

    matrix = ""
    platform = []
    for arch in docker_arches:
        platform.append(f"{arch}")
    platform = ",".join(platform)

    matrix += f"- name: {repo_name}-v{repo_version}\n"
    matrix += f"  repo_owner: {repo_owner}\n"
    matrix += f"  repo_name: {repo_name}\n"
    matrix += f"  version: v{repo_version}\n"
    matrix += f"  context: ./{repo_name}\n"
    matrix += f"  platforms: {platform}\n"
    matrix += f"  docker-repo: {docker_repo}\n"
    matrix += f"  tags: |\n"
    for tag in tags():
        matrix += f"    {tag}\n"

    marker = "#MATRIX\n"
    split = config.split(marker)
    rendered = split[0] + marker + matrix + marker + split[2]
    write_file(file, rendered)

def update_readme():
    template = read_file("README.template")

    tag = ",".join([f"`{t}`" for t in tags()])
    image_tags = f" - [{tag}](https://github.com/{repo_owner}/{repo_name}/blob/main/Dockerfile)\n"

    rendered = template \
        .replace("%%PROJECT_NAME%%", project_name) \
        .replace("%%REPO_NAME%%", repo_owner + "/" + repo_name) \
        .replace("%%TAGS%%", image_tags) \
        .replace("%%DOCKER_REPO%%", docker_repo) \
        .replace("%%TAG%%", tags()[0]) \
        .replace("%%DOCS_URL%%", docs_url)
    write_file(f"README.md", rendered)

def usage():
    print(f"Usage: {sys.argv[0]} update-all|update-ci|update-readme")
    sys.exit(1)

if __name__ == "__main__":
    repo_version = read_file(version_file).strip()

    if len(sys.argv) != 2:
        usage()

    task = sys.argv[1]
    if task == "update-all":
        update_ci()
        update_readme()
    elif task == "update-ci":
        update_ci()
    elif task == "update-readme":
        update_readme()
    else:
        usage()
