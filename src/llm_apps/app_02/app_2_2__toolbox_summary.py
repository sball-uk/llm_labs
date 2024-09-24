"""This module asks an LLM to summarise key points from one or more articles.
See app_02/README.md
"""

from ..common_lib import llms as cll
from ..common_lib import misc_utils as clm

# Specify input and output directories
DIR_INPUT_DOCX = "../data/app_02__skills_toolbox/2.2.1__to_review/"
DIR_OUTPUT = "../data/app_02__skills_toolbox/2.2.9__output_summary/"

# Specify output filename (json and txt)
FNAME_OUTPUT = "2.2.9__toolbox_summary"

# Import API key as environment variable
clm.load_dotenv_all()


if __name__ == "__main__":

    # Get list of filenames in input directory
    list_docs_to_review = clm.list_files_in_dir(path_dir=DIR_INPUT_DOCX, file_type=".docx")

    # Use the first 7 characters of the filename as an id, e.g. 'tb-0001'
    dict_docs_to_review = {filename[:7]: filename for filename in list_docs_to_review}

    # Ask the LLM the prompt, looping over all files in the input directory
    if len(dict_docs_to_review) == 0:
        print(f"No docx files in input directory: '{DIR_INPUT_DOCX}'")
    else:
        output_list_of_dicts = []
        for tb_id, tb_filename in dict_docs_to_review.items():
            print("")
            print(f"Key: {tb_id}, Value: {tb_filename}")

            tb_url, tb_text = clm.load_docx_to_str(DIR_INPUT_DOCX + tb_filename)

            # Set the prompt
            prompt = f"""
                Given the article below, extract summary information for the following pieces of information.
                Use British spelling instead of American spelling.
                Provide output as a Python dictionary with the number as the key and your response as the value.
                Use double quotes and start and end with curly braces.
                For 8 to 12, respond in one sentence.
                For 13 to 15, respond in a few words.
                It is very important that you do not add introductory remarks.
                If you add introductory remarks I will fire you.
                Do NOT add introductory remarks in any circumstances.
                    1. What is the title of the article?
                    2. Who is the author?
                    3. Which company or organisation is the author from?
                    4. What is the date of the article?
                    5. Are there any code examples (Yes or No)?
                    6. Summarise the article in one sentence.
                    7. Summarise the article in seven sentences.
                    8. What is discussed?
                    9. How does it work?
                    10. Why is this relevant?
                    11. What are the risks?
                    12. What are the opportunities?
                    13. What is the primary technique used?
                    14. What is the primary tool used?
                    15. What is the primary domain mentioned in the article?

                Return "Unknown" for a particular piece of information if it is not given.

                Article:
                {tb_text}
                """

            # Send the prompt to the LLM and choose which context to use
            response_str = cll.llm_response(
                prompt=prompt,
                system_context=cll.llm_contexts()["Normal"],
                temperature=0)

            # Convert response to dict
            response_dict = cll.convert_llm_response_to_dict(response_str)
            del response_str

            # Append to output
            tmp_dict = {
                "tb_id": tb_id,
                "tb_filename": tb_filename,
                "tb_url": tb_url,
                "llm_response": response_dict}
            output_list_of_dicts.append(tmp_dict)

        # Overwrite json file
        cll.export_this_run_to_json(output_list_of_dicts, DIR_OUTPUT + FNAME_OUTPUT)

        # Incrementally add output to pipe-delimited txt file
        cll.insert_into_txt_from_json(DIR_OUTPUT + FNAME_OUTPUT)
