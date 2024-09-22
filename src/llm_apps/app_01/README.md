# LLM App #1, Job Search Assistant

The intended use case is to provide assistance for an indvidual in their job search. The default persona of the LLM assistant is one of a sceptical wannabe film noir detective; this is a paramater [that can be changed](https://github.com/sball-uk/llm_labs/tree/main/src/llm_apps/common_lib/llms.py). The app comprises two separate but complementary tools.
- '1.1': The LLM reviews one or more job descriptions and outputs a summary based on several questions. This includes: basic information retrieval (e.g. role name, company name, location, ...); questions on whether certain skills or responsibilities are involved (e.g. Does the role require a specialism in MLOps?, ...); more speculative questions (e.g. Are the role responsibilities expecting too much for one person?, ...); and asking the LLM's opinion (e.g. What is the best thing about this job?, Would you want to work there?, ...). The later questions in particular were chosen to be challenging for a machine to answer.
- '1.2': The LLM compares one CV against job descriptions to assess the compatibility and offers suggestions to tailor the CV. This includes: comparison questions (e.g. Do I have all the required skills/qualifactions?, ...); speculative questions (e.g. What's my chance?, ...); suggestions for amendments to the CV (What should be modified or added in the CV?, ...); support in drafting a cover letter (e.g. What are my top three selling points that are relevant to the role?, Write a brief draft cover letter., ...).

In exploring the outputs, I have found these tools quite helpful and it has also offered me surprising insights into the capabilities of LLMs.

## Usage

### 1.1: Summarise job descriptions and identify a shortlist

#### a) Get input ready: all job descriptions
 - Save one or more job descriptions in docx format (one file per job description).
 - Add the url of the job description on the first line; you can probably delete all the tracking info after the first '?', e.g. 'https://www.linkedin.com/jobs/view/4003606487'
 - Move the docx files to `[clone_location]/data/app_01__job_search_assistant/1.1.1__to_review/`

#### b) Run Python script
- Activate the new Python environment, navigate to `cd [clone_location]/src/` and then run:
```
python -m llm_apps.app_01.app_1_1__shortlist
```

#### c) Output
- This does a full refresh of the json output file `1.1.9__shortlist.json` in `/1.1.9__output_summary/`.
- It also populates the pipe-delimited output file `1.1.9__shortlist.txt` in the same folder; the new data is appended to output from previous runs.
- The '.txt' output file can be opened in the tool of your choice to view the outputs, delimiting by pipe, '|'.
- [optional] You may want to modify elements of the prompt then run the script again to assess how the model outputs vary.

#### d) Clean-up
- Once you are happy with the outputs, move the input files from `/1.1.1__to_review/` to `/1.1.2__reviewed/` so that you don't process them again next time you run it.


### 1.2: Compare shortlisted job descriptions to a CV

#### a) Get input ready: subset of job descriptions and CV
- After reviewing the output of 1.1, manually identify a shortlisted subset of the job descriptions and copy them to `/1.2.1__to_review/`
- Put your CV as a docx file in `/1.2.3__cv_to_compare/`

#### b) Run Python script
- Activate the new Python environment, navigate to `cd [clone_location]/src/` and then run:
```
python -m llm_apps.app_01.app_1_2__compare
```

#### c) Output
- This populates the pipe-delimited output file `1.2.9__compare_cv_vs_job.txt` in `/1.2.9__output_comparison/`.

#### d) Clean-up
- Once you are happy with the outputs, move the input files from `/1.2.1__to_review/` to `/1.2.2__reviewed_job_desc/` so that you don't process them again next time you run it.
