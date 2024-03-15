from langchain.chains import LLMChain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.movie_lookup_agent import lookup as movie_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile
from dotenv import load_dotenv

load_dotenv()

input = "aneesh bose microsoft"
if __name__ == '__main__':
    print("Hello langchain")
    
    summary_template = """
    We have 2 kinds of data about a person. Firstly, We have this Linkedin data about the person - {linkedin_information}.
    Secondly, we have this movie data about the person - {movie_information}.
    Based on these 2 data sources, prepare 2 ice breaker points for the person.  The ice breaker should be interesting and engaging, you can include specific details about
    professional and movie choices.
    """

    
    movie_data = movie_lookup_agent(name = input)
    linkedin_profile_url = linkedin_lookup_agent(name = input)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    summary_prompt_template = PromptTemplate(input_variables=["linkedin_information", "movie_information"],template=summary_template)
    llm = AzureChatOpenAI(
        openai_api_version = "2024-02-15-preview",
        azure_deployment="gpt-35-turbo",
        temperature=0,
    )
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    res = chain.invoke(input={"linkedin_information": linkedin_data, "movie_information": movie_data})

    print(res['text'])

