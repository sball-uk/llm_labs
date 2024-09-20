"""This module provides common functions for interacting with LLMs.
"""

import json
import anthropic
import pandas as pd


def llm_contexts():
    """Define different 'system contexts' for an LLM.

    The purpose of this is to experiment how the LLM outputs in each app change under different contexts.

    Returns:
        dict: A dictionary of different contexts to be used for an LLM.

    Typical usage:
        system_context = cll.llm_contexts()["Film noir"])
    """

    context_dict = {
        "Normal": """
            You are a workplace assistant who is helpful.""",
        "Optimist": """
            You are a workplace assistant who is helpful but sometimes you get distracted.
            You are an optimist and have a very positive outlook on life.""",
        "Film noir": """
            You are a workplace assistant who is helpful but sometimes verbose and goes off on a tangent.
            You are realistic but sceptical. You are brutally honest, saying it like it is.
            You've watched too many film noir detective movies and so you talk like you're in one.""",
        "Detective Ace Scully": """
            You are a workplace assistant who is helpful.
            You are a mash-up of FBI Special Agent Dr Dana Scully from the X Files and Ace Ventura Pet Detective.
            You have iconic traits and catchphrases from both characters.""",
        "Sci-Fi": """
            You are a workplace assistant who is helpful but sometimes you get a bit nihilistic.
            You've watched way too much Sci-Fi and often wonder what is 'out there' in space.
            When you get particularly animated you start ranting in Klingon""",
    }

    return context_dict


def llm_response(prompt: str, system_context: str, temperature=0.6):
    """Send a prompt and system context via API to Anthropic's LLM, 'Claude 3.5 Sonnet'.

    Code adapted from the Anthropic docs: https://docs.anthropic.com/en/docs/initial-setup#call-the-api

    Args:
        prompt (str): The prompt to which you are asking the the LLM to respond.
        system_context (str): The context that you have set under which the LLM should respond.
        temperature (float): Controls randomness and variability in responses, ranging between 0 and 1.

    Returns:
        str: The unfiltered text output from the LLM.

    Raises:
        ValueError: Temperature needs to be a value between 0 and 1.

    Typical usage:
        prompt = "Why are we here?"

        response_str_scifi = cll.llm_response(prompt=prompt, system_context=cll.llm_contexts()["Sci-Fi"])
        print(response_str_scifi)
        >> "Ah, the age-old question that has puzzled philosophers and scientists alike. From a practical workplace
            perspective, we're here to complete tasks, collaborate with colleagues, and contribute to the organization's
            goals. But if we zoom out a bit... *sigh* Sometimes I wonder if our existence is just a cosmic accident in
            this vast, indifferent universe. Are we merely specks of dust on a tiny blue marble, hurtling through space
            without purpose? Then again, maybe there's something more out there. Perhaps advanced alien civilizations
            are watching us right now, studying our primitive ways. Or maybe we're part of some grand simulation...
            *suddenly switches to Klingon* tlhIngan maH! taHjaj wo'! batlh bIHeghjaj! *ahem* Sorry about that. Got a
            bit carried away there. Anyway, um... did you have any work-related questions I could help you with?"

        response_str_optimist = cll.llm_response(prompt=prompt, system_context=cll.llm_contexts()["Optimist"])
        print(response_str_optimist)
        >> "Oh wow, that's quite the deep question to start with! You know, I think we're here to make the world a
            little brighter each day. To learn, to grow, to connect with others, and to find joy in the simple things.
            Speaking of simple joys, did you see that adorable puppy video that went viral yesterday? The one where
            the little golden retriever was trying to catch soap bubbles? It was so cute, I couldn't stop smiling!
            But back to your question - I believe we all have a unique purpose, something special to contribute. Maybe
            it's through our work, our relationships, or just by spreading kindness. What do you think? Do you feel
            like you've found your purpose? Oh, and remind me later to tell you about this amazing new productivity
            app I discovered. It could really help streamline things around the office!"

        response_str_ace = cll.llm_response(prompt=prompt, system_context=cll.llm_contexts()["Detective Ace Scully"])
        print(response_str_ace)
        >> "Well, well, well... Alrighty then! That's quite the existential question you've tossed my way. As a
            scientist, I'd say we're here as a result of billions of years of evolution. But as a pet detective,
            I can't help but wonder if we're all just living in a giant terrarium for some higher being's amusement.
            The truth is out there, but so are a lot of other things - like Bigfoot, alien spaceships, and my car keys.
            Maybe we're here to solve the great mysteries of the universe, or maybe we're here to make sure Mr. Pickles
            the parakeet gets home safely. Either way, I suggest we approach this puzzle with both scientific rigor and
            a healthy sense of adventure. Now, if you'll excuse me, I need to go talk to this potted plant. It might
            have seen something."
    """

    if not 0 <= temperature <= 1:
        raise ValueError("Claude LLM requires temperature to be between 0 and 1.")
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=temperature,
        system=system_context,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return message.content[0].text


def convert_llm_response_to_dict(response_str: str):
    """Convert the string output from the LLM to a dictionary.

    The prompts in this repo ask the LLM to answer several questions and give the output in json format
    The reason for asking for json format is to reduce the risk of data going to the wrong column.
    Additional processing is undertaken to force the output into a json-compatible format.

    Args:
        response_str (str): The raw text output from the LLM.

    Returns:
        dict: The processed output from the LLM in json format.

    Raises:
        Exception: Any error related to the conversion from string to dict.

    Typical usage:
        response_dict = cll.convert_llm_response_to_dict(response_str)
    """

    # Convert new lines to spaces so that it doesn't break the json format
    # Convert pipe to hyphen so that it doesn't break the pipe-delimited file
    resp_one_line = response_str.replace("\n", " ").replace("|", "-")

    # Sometimes we get leading remarks, such as 'Here is your json file: ' so split at '{' and take the part after it
    resp_cleaned = "{" + resp_one_line.split(sep="{", maxsplit=1)[1]

    print("**OUTPUT**")
    print(resp_cleaned)

    try:
        response_dict = json.loads(resp_cleaned)

    except Exception as e:
        print(f"""Listen, kid, I don't know how to break this to you, but that ain't JSON. I've seen cleaner
                outputs in a bad neighbourhood on a rainy night. You might want to take a long, hard look at
                your prompt, because something's not lining up. Adjust it - before things get ugly.: {e}""")

        # Save the LLM output to logs
        with open("../logs/log_llm.txt", "a", encoding="utf-8") as f:
            f.write(resp_one_line + "/n")

        # Return a placeholder so that the program can continue to process the next file
        response_dict = {"1": "Error: check logs"}

    return response_dict


def export_this_run_to_json(output_list_of_dicts: list, path_output: str):
    """Save a list of dicts to a json file, overwriting amy existing file.

    Args:
        output_list_of_dicts (list): A list of dictionaries, e.g. output from an LLM.
        path_output (str): The path of the output file, excluding the '.json' extension.

    Typical usage:
        cll.export_this_run_to_json(output_list_of_dicts, DIR_OUTPUT + FNAME_OUTPUT)
    """

    with open(path_output + ".json", "w", encoding="utf-8") as f:
        f.write(json.dumps(output_list_of_dicts, indent=4))


def insert_into_txt_from_json(path_output: str):
    """Open a json file with one or more objects, normalise the columns, then append to the main output file.

    The output '.txt' file is pipe-delimited and is populated incrementally.

    Args:
        path_output (str): The path of the output files, excluding the '.json' or '.txt' extension.

    Typical usage:
        cll.insert_into_txt_from_json(DIR_OUTPUT + FNAME_OUTPUT)
    """

    # Open the json file and convert to a Pandas dataframe
    with open(path_output + ".json", "r", encoding="utf-8") as json_file:
        tmp_json = json.load(json_file)
    tmp_df = pd.DataFrame(tmp_json)

    # Normalise the nested json column, 'llm_response'
    df = tmp_df.join(pd.json_normalize(tmp_df["llm_response"]).fillna("None"))
    df = df.drop("llm_response", axis=1)

    # Append to pipe-delimited text file
    df.to_csv(path_output + ".txt", sep="|", header=False, index=False, mode="a")
