"""A simple script that collects issues from a repo and generate a markdown
file (Report.md).

A personal access token will need to be configured. Also the repo name will
need to be provided. Add these in `config.py`.

Requirements: pygithub.

`pip install --user pygithub`
"""
from github import Github

import config

REPO = config.REPO
github = Github(config.TOKEN)

issue_dict = {}

labels = ['3 (High Risk)', '2 (Med Risk)', '1 (Low Risk)', '0 (Non-critical)', 'G (Gas Optimization)']

def highest_label(all_labels: [str]) -> str:
    indices = [labels.index(label) for label in all_labels if label in labels]
    return labels[min(indices)] if indices != [] else 'Unlabeled'

# The C4 issues are like
#     # Handle
#     name
#     # Description.
# We want to make it into
#     ### Handle
#     name
#     ### Description
#     ...
# Ugly hack
def format_body(body: str) -> str:
    return body.replace("# ", "### ")

for issue in github.get_repo(REPO).get_issues():
    label = highest_label(map(lambda l: l.name, issue.labels))
    if label not in issue_dict:
        issue_dict[label] = []
    issue_dict[label].append(f"## {issue.title} \n{format_body(issue.body)}\n")

with open("Report.md", "w") as report:
    for label in labels + ['Unlabeled']:
        report.write(f"# {label} \n\n")
        if label in issue_dict:
            for content in issue_dict[label]:
                report.write(content.replace("\r\n", "\n"))
