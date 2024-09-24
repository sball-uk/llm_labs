"""This module asks an LLM to compare a CV against one or more job descriptions.
See app_01/README.md
"""

from ..common_lib import llms as cll
from ..common_lib import misc_utils as clm

# Specify input and output directories
DIR_INPUT_DOCX_JOB = "../data/app_01__job_search_assistant/1.2.1__to_review/"
DIR_INPUT_DOCX_CV = "../data/app_01__job_search_assistant/1.2.3__cv_to_compare/"
DIR_OUTPUT = "../data/app_01__job_search_assistant/1.2.9__output_comparison/"

# Specify output filename (json and txt)
FNAME_OUTPUT = "1.2.9__compare_cv_vs_job"

# Import API key as environment variable
clm.load_dotenv_all()


if __name__ == "__main__":

    # Load the CV
    cv_filename = clm.list_files_in_dir(path_dir=DIR_INPUT_DOCX_CV, file_type=".docx")[0]
    cv_text = clm.load_docx_to_str(DIR_INPUT_DOCX_CV + cv_filename)[1]

    # Get list of filenames in input directory
    list_docs_to_review = clm.list_files_in_dir(path_dir=DIR_INPUT_DOCX_JOB, file_type=".docx")

    # Use the first 7 characters of the filename as an id, e.g. 'job-001'
    dict_docs_to_review = {filename[:7]: filename for filename in list_docs_to_review}

    # Ask the LLM the prompt, looping over all files in the input directory
    if len(dict_docs_to_review) == 0:
        print(f"No docx files in input directory: '{DIR_INPUT_DOCX_JOB}'")
    else:
        output_list_of_dicts = []
        for job_id, job_filename in dict_docs_to_review.items():
            print("")
            print(f"Key: {job_id}, Value: {job_filename}")

            job_link, job_text = clm.load_docx_to_str(DIR_INPUT_DOCX_JOB + job_filename)

            # Set the prompt
            prompt = f"""
                Given the job description below, compare the CV against it and consider the following questions.
                Use British spelling instead of American spelling.
                Provide output as a Python dictionary with the number as the key and your response as the value.
                Use double quotes and start and end with curly braces.
                It is very important that you do not add introductory remarks.
                If you add introductory remarks I will fire you, kid.
                Do NOT add introductory remarks in any circumstances.
                1. Do I have all the required skills?
                2. Do I have all the required qualifactions?
                3. Is this job a good fit for me based on my CV?
                4. Am I over-qualified for this?
                5. Give me just an integer on a scale of 1 to 10 for how well my CV meets the requirements.
                6. Give me just an integer on a scale of 1 to 10 for how likely it is that I would be succesful.
                7. Speculate: what's my chance of getting the gig if I apply with this CV, kid?
                8. Do you think I should I even apply?
                9. What (if anything) should be modified or added in the CV?
                10. What are my top three selling points that are relevant to the role?
                11. Write a brief draft cover letter.
                12. Write a very brief cover email for an online application.

            CV:
            {cv_text}

            JOB DESCRIPTION:
            {job_text}

            """

            # Send the prompt to the LLM and choose which context to use
            response_str = cll.llm_response(
                prompt=prompt,
                system_context=cll.llm_contexts()["Film Noir"],
                temperature=0.4)

            # Convert response to dict
            response_dict = cll.convert_llm_response_to_dict(response_str)
            del response_str

            # Append to output
            tmp_dict = {
                "job_id": job_id,
                "job_filename": job_filename,
                "job_link": job_link,
                "cv_filename": cv_filename,
                "llm_response": response_dict}
            output_list_of_dicts.append(tmp_dict)

        # Overwrite json file
        cll.export_this_run_to_json(output_list_of_dicts, DIR_OUTPUT + FNAME_OUTPUT)

        # Incrementally add output to pipe-delimited txt file
        cll.insert_into_txt_from_json(DIR_OUTPUT + FNAME_OUTPUT)
