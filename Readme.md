# Compile issues from a spearbit audit github repo

## Requirements

[PyGithub](https://pypi.org/project/PyGithub/)

```bash
pip install --user pygithub
```

## Configuration

You will need to generate a personal access token that can access private repositories. [GitHub docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

Check the "repo" option: full control of private repositories.

After that update the [`config.py`](./config.py) file locally with the token and a reference to the GithHub repo.

## Running

```bash
python3 compile.py
```

The file `report.md` would contain the generated report.

## Notes

- The original GitHub issues can be edited and the report can be regenerated with the updates!
