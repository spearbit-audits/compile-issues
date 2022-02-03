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

# TODO catch get_repo() 404 errors and produce a gentle suggestion on what's wrong.

for issue in github.get_repo(REPO).get_issues():
    # TODO what happens when there are more than one issue labels. In that
    # case, need to put the issue into the label with highest severity.
    if len(issue.labels) != 0:
        label = issue.labels[0].name
        if label not in issue_dict:
            issue_dict[label] = []
        issue_dict[label].append(f"### {issue.title} \n{issue.body}\n")

labels = ['Severity: Critical Risk', 'Severity: High Risk', 'Severity: Medium Risk', 'Severity: Low Risk', 'Severity: Gas Optimization', 'Severity: Informational']

with open("Report.md", "w") as report:
    for label in labels:
        report.write(f"## {label[10:]}\n\n")
        for content in issue_dict[label]:
            report.write(content.replace("\r\n", "\n"))
