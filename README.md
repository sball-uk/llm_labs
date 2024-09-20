# LLM Apps

This repo contains some simple applications that use Large Language Models (LLMs) via an API.
- <b>App #1, Job Search Assistant</b> [README](https://github.com/sball-uk/llm_labs/tree/main/src/llm_apps/app_01): reviews job descriptions and outputs a summary based on several questions; also compares one CV against job descriptions to assess the compatibility and offers suggestions to the user to tailor their CV.
- <b>App #2, Skills Toolbox</b> [README](https://github.com/sball-uk/llm_labs/tree/main/src/llm_apps/app_02): summarises key points from skills and/or knowledge articles for topics on data science, machine learning and artificial intelligence.

These are use cases that I've found helpful to me personally and I will share additional applications here as I create them. All of these use publicly available data for inputs.

<p><b>If you plan to use or modify this code for your own use cases, before you do PLEASE(!) think about whether it is appropriate, ethical and legal to do so.</b></p>

- Example - It would be technically possible to ask the LLM to summarise source data from non-public sources e.g. confidential company information or private medical records etc. However, depending on the nature of such data, sending it to the LLM API could likely be a breach of privacy. You may instead want to explore alternative methods for interacting with an LLM (e.g. host your own LLM) and you should discuss and consider the ethical and legal risks with relevant experts.
- Another example - It would be technically possible to modify 'App 1.2' to compare multiple CVs with one job description (rather than comparing your own CV with multiple job descriptions). This could be a valuable use case, e.g. if you are a hiring manager or recruitment consultant. However, this would be quite a different use case and introduces several new ethical and legal risks that would need to be considered: e.g. what level of social bias is present in the model outputs?; what employment regulations are applicable and would the use of this technique be compliant?; would you first need to redact personal information from the candidate CVs? etc

## Setup

#### a) This repo uses Anthropic's LLM, ['Claude 3.5 Sonnet'](https://www.anthropic.com/news/claude-3-5-sonnet)
- You will need to get an API key and buy some credits; e.g. see [this helpful blog post](https://zapier.com/blog/claude-api).
- Store your key in `.env`

#### b) Create and activate a new Python environment.
- Using conda:
```
conda create -n py311_some_env python=3.11
conda activate py311_some_env
```

- Alternatively, using virtualenv:
```
virtualenv some_env
.\some_env\Scripts\activate
```

#### c) Install packages
- Install the [Anthropic package](https://docs.anthropic.com/en/docs/initial-setup#install-the-sdk) along with the other required packages.
```
cd [clone_location]
pip install -r requirements.txt
```

## [Optional] Additional setup

#### d) If you want to try using a different LLM provider
- Modify the `llm_response()` function in `src/llm_apps/common_lib/llms.py` as appropriate.

#### e) Set up Python development environment
- For linting, if using VS Code as your IDE install the Flake8 and Pylint extensions (alternatively install via Pip). Modify `setup.cfg` and `.pylintrc` as required; [further info](https://code.visualstudio.com/docs/python/linting).
- Pre-commit is a tool that runs automatic checks before a user is able to commit to git. Install for your cloned repo with the command `pre-commit install`, which will add the hooks to your .git directory. To run it on all files, use `pre-commit run --all-files` and check the console output for any failures.  Modify `.pre-commit-config.yaml` as required; [further info](https://pypi.org/project/pre-commit).
- Increment the version number in `.version` and `__init__.py` using bump2version, e.g. `bump2version minor`.
