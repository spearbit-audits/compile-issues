"""A simple script that collects issues from a repo and generate a markdown
file (report.md).

A personal access token will need to be configured. Also the repo name will
need to be provided. Add these in `config.py`.

Requirements: pygithub.

`pip install --user pygithub`
"""
from github import Github

import config

REPO = config.REPO
github = Github(config.TOKEN)

SEVERITY_LABELS = ['Severity: Critical Risk', 'Severity: High Risk', 'Severity: Medium Risk', 'Severity: Low Risk', 'Severity: Gas Optimization', 'Severity: Informational']

issue_dict : dict[str, list[str]] = {}

# TODO catch get_repo() 404 errors and produce a gentle suggestion on what's wrong.
# "GitHub's REST API v3 considers every pull request an issue"--need to filter them out.
for issue in github.get_repo(REPO).get_issues():
    if issue.state == 'open' and issue.pull_request is None:
        # filter issue labels for only severity labels
        severity_labels_in_issue = [label.name for label in issue.labels if label.name in SEVERITY_LABELS]

        assert len(severity_labels_in_issue) == 1, f"Issue {issue.html_url} has more than one (or no) severity label."
        label = issue.labels[0].name
        if label not in issue_dict:
           issue_dict[label] = []
        issue_dict[label].append(f"### {issue.title} \n{issue.body}\n")

with open("report.md", "w") as report:
    for label in SEVERITY_LABELS:
        report.write(f"## {label[10:]}\n\n")
        for content in issue_dict[label]:
            report.write(content.replace("\r\n", "\n"))
