from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import re

class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper, self).__init__()

    @staticmethod
    def _process_response(res: dict):
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif (
            "answer_box" in res.keys()
            and "snippet_highlighted_words" in res["answer_box"].keys()
        ):
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif (
            "sports_results" in res.keys()
            and "game_spotlight" in res["sports_results"].keys()
        ):
            toret = res["sports_results"]["game_spotlight"]
        elif (
            "knowledge_graph" in res.keys()
            and "description" in res["knowledge_graph"].keys()
        ):
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0]["link"]

        else:
            toret = "No good search result found"
        return toret


def get_profile_url(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    search = CustomSerpAPIWrapper()
    res = search.run(f"{name}")
    return res


def get_txt(name: str):
    """loads the name.txt file which contains the person's watching history."""
    try:
        with open(f"{name}.txt", "r") as file:
            return str(file.read())
    except FileNotFoundError:
        return None
    

def get_movie_suggestions(likes: str):
    """Searches for movie recommendations based on the past likes of the person. It can be based on actor/genre/director."""
    search = SerpAPIWrapper()
    res = search.run(f"movies similar to {likes}")
    return res

def get_past_history(name: str):
    """Searches for a person's likes/genres/actors/directors based on person's name."""

    name = re.sub(r'\W+', '', name.split()[0]).lower()
    print(name)
    try:
        with open(f"tools\{name}.txt", "r") as file:
            content = str(file.read()).lower()

        summary_template = """
        Given this watch history information about a person - [ {information} ], find the favourite genre and director of the person. The Output should be short and concise.
        """
        summary_prompt_template = PromptTemplate(input_variables=["information"],template=summary_template)
        llm = AzureChatOpenAI(
            openai_api_version = "2023-09-15-preview",
            azure_deployment="gpt-35-turbo",
            temperature=0,
        )
        chain = LLMChain(llm=llm, prompt=summary_prompt_template)
        res = chain.invoke(input={"information": content})

        return res

    except FileNotFoundError:
        return None
    

if __name__ == "__main__":
    print(get_past_history("shivam shrivastava"))