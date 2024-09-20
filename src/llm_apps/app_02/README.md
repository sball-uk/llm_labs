# LLM App #2, Skills Toolbox

The intended use case is to summarise key points from skills and/or knowledge articles for topics on data science, machine learning and artificial intelligence. The app comprises two separate but complementary tools.
- '2.1': Source data comes in many formats from various public sources, including academic papers, reports, blogs, webinar transcripts, product websites etc. This first tool automatically captures text from web pages to local copies in '.docx' format. This is a non-trivial task and for some websites this tool may not work well. The approach used to retrieve web page data is somewhat rudimentary and could be improved with additional effort. Where the tool doesn't work or where it is very important to ensure accuracy of the output, the user should instead manually copy the desired text into a 'docx' file.
- '2.2': The LLM synthesises the key points from each document, including: basic information retrieval (e.g. Who is the author?, Are there any code examples?, ...); summarisation tasks (e.g. Summarise the article in seven sentences., ...); 'Kolb' questions (e.g. Why?, What?, How?, What If?); identify the main topic (What is the primary technique / tool / domain?).

Support on 'knowledge tasks' such as this is perhaps one of the most promising applications for LLMs in general. This tool has enabled me to keep a more organised library of information with documents summarised and categorised by technique, tool and/or domain. This approach has helped me to be more productive with faster synthesis of these documents, allowing me to identify the sources that are more relevant. I still read many of the documents myself, but this is now based on a more focused prioritised reading list. Another benefit is in having a searchable database of knowledge articles to be able to easily revisit them in the future and share as appropriate.

## Usage

### 2.1: Copy and save text from web pages

#### a) Populate csv: website links of articles
 - Populate the csv file `2.1.1__input_sources.csv` in `[clone_location]/data/app_02__skills_toolbox/2.1.1__input_sources/`.
 - You should not include websites in the csv where it is not permitted to automatically download content.
 - There are three fields:
   - `tb_id`: a 7-character unique identifier, e.g. 'tb_0001'
   - `to_get`: a boolean (0 or 1) where 1 indicates that the row should be included and 0 indicates it should be filtered out.
   - `tb_url`: the website link of the source text, e.g. https://en.wikipedia.org/wiki/Large_language_model

#### b) Run Python script
- Activate the new Python environment, navigate to `cd [clone_location]/src/` and then run:
```
python -m llm_apps.app_02.app_2_1__text_from_web_page
```

#### c) Check output and modify if necessary
- Check the automatically generated output files in `/2.1.9__output_downloaded/`.
- Remove any unwanted text; it might work reasonably well for some websites, but won't work for some.
- For any websites that didn't work, instead manually save the relevant text to docx, ensuring that the url of the article is on the first line.
- You can also manually create documents for text with no websites, e.g. personal lecture notes etc.

### 2.2: Summarise key points from skills and/or knowledge articles

#### a) Get input ready: articles
- The required input format is one '.docx' file per source. These documents can be either manually populated or generated automatically by the tool above. The first line should be the website url (or put 'N/A' if there is no website).
- Move the docx files to `/2.2.1__to_review/`

#### b) Run Python script
- Activate the new Python environment, navigate to `cd [clone_location]/src/` and then run:
```
python -m llm_apps.app_02.app_2_2__toolbox_summary
```

#### c) Output
- This populates the pipe-delimited output file `2.2.9__toolbox_summary.txt` in `/2.2.9__output_summary/`.
- You may want to open this file in the tool of your choice to view the outputs.

#### d) Clean-up
- Once you are happy with the outputs, move the input files from `/2.2.1__to_review/` to `/2.2.2__reviewed/` so that you don't process them again next time you run it.
