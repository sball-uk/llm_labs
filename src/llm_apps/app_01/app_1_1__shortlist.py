"""This module asks an LLM to summarise key points from one or more job descriptions.
See app_01/README.md
"""

from ..common_lib import llms as cll
from ..common_lib import misc_utils as clm

# Specify input and output directories
DIR_INPUT_DOCX = "../data/app_01__job_search_assistant/1.1.1__to_review/"
DIR_OUTPUT = "../data/app_01__job_search_assistant/1.1.9__output_summary/"

# Specify output filename (json and txt)
FNAME_OUTPUT = "1.1.9__shortlist"

# Import API key as environment variable
clm.load_dotenv_all()


if __name__ == "__main__":

    # Get list of filenames in input directory
    list_docs_to_review = clm.list_files_in_dir(path_dir=DIR_INPUT_DOCX, file_type=".docx")

    # Use the first 7 characters of the filename as an id, e.g. 'job-001'
    dict_docs_to_review = {filename[:7]: filename for filename in list_docs_to_review}

    # Ask the LLM the prompt, looping over all files in the input directory
    if len(dict_docs_to_review) == 0:
        print(f"No docx files in input directory: '{DIR_INPUT_DOCX}'")
    else:
        output_list_of_dicts = []
        for job_id, job_filename in dict_docs_to_review.items():
            print("")
            print(f"Key: {job_id}, Value: {job_filename}")

            job_link, job_text = clm.load_docx_to_str(DIR_INPUT_DOCX + job_filename)

            # Set the prompt
            prompt = f"""
                Given the job description below, extract summary information for the following pieces of information.
                Use British spelling instead of American spelling.
                Provide output as a Python dictionary with the number as the key and your response as the value.
                Use double quotes and start and end with curly braces.
                It is very important that you do not add introductory remarks.
                If you add introductory remarks I will fire you, kid.
                Do NOT add introductory remarks in any circumstances.
                    1. What is the role title?
                    2. What is the recruitment consultancy?
                    3. What is the company name?
                    4. In what industry does the company operate?
                    5. How many employees does the company have?
                    6. Is it a startup environment or an established business?
                    7. Is the role remote, hybrid or onsite?
                    8. How many days onsite are expected?
                    9. What is the location?
                    10. What is the available salary range?
                    11. Does the role involve line management, if so how many people?
                    12. Does the role involve maintaining a funnel of projects including prioritisation?
                    13. Does the role require a specialism in deep learning?
                    14. Does the role require a specialism in computer vision?
                    15. Does the role require a specialism in MLOps?
                    16. How many years experience are required?
                    17. What qualifications are required?
                    18. Is the role focused more on analytics (e.g. requirements, feature engineering, model
                        training) or engineering (MLOps, model deployment and maintenance, cloud platforms)?
                    19. Are there any worrying points that would give you pause for thought?
                    20. Are there any spelling mistakes in the job description?
                    21. Give a brief summary of the main data and analytical tools used.
                    22. Which cloud platforms are used?
                    23. How many AI professionals already work there?
                    24. Is it greenfield, building their AI capability from scratch?
                    25. Speculate: what is their level of maturity for data ingestion and processing.
                    26. Speculate: are the role responsibilities expecting too much for one person?
                    27. Speculate: with the required skills and experience, do you think they are looking
                        for a (metaphorical) unicorn?
                    28. What is the sentiment on a scale of -3 to +3?
                    29. How much does it inspire you on a scale of 1 to 10?
                    30. What is the best thing about this job?
                    31. Would you want to work there?
                    32. Would this role make a positive difference?

                Feel free to read between the lines and speculate based on what you've seen, but
                return "Unknown" for a particular piece of information if it is not given.

                Job description:
                {job_text}
                """

            # Send the prompt to the LLM and choose which context to use
            response_str = cll.llm_response(
                prompt=prompt,
                system_context=cll.llm_contexts()["Film Noir"],
                temperature=1)

            # Convert response to dict
            response_dict = cll.convert_llm_response_to_dict(response_str)
            del response_str

            # Append to output
            tmp_dict = {
                "job_id": job_id,
                "job_filename": job_filename,
                "job_link": job_link,
                "llm_response": response_dict}
            output_list_of_dicts.append(tmp_dict)

        # Overwrite json file
        cll.export_this_run_to_json(output_list_of_dicts, DIR_OUTPUT + FNAME_OUTPUT)

        # Incrementally add output to pipe-delimited txt file
        cll.insert_into_txt_from_json(DIR_OUTPUT + FNAME_OUTPUT)
