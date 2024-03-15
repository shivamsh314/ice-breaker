from dotenv import load_dotenv

from tools.tools import get_movie_suggestions, get_past_history

load_dotenv()

from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain_core.tools import Tool
from langchain_openai import AzureChatOpenAI
from langchain import hub
from langchain_core.prompts import PromptTemplate



def lookup(name: str):
    llm = AzureChatOpenAI(
        openai_api_version = "2024-02-15-preview",
        azure_deployment="gpt-35-turbo",
        temperature=0.2,
    )
    template = """given the name of the person - {name_of_person}, I want you to find what movie should they watch next? Look up their previous local watch 
    history and suggest a movie according to their likes/genres/directors"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google for movies suggestions",
            func=get_movie_suggestions,
            description="useful for when you need to search for movie recommendations based on the past likes of the person. It can be based on actor/genre/director.",
        ),
        Tool(
            name="Find a person's personal likes/genres/actors/directors",
            func=get_past_history,
            description="useful for when you need to find a person's local likes/genres/actors/directors based on the person's name.",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    
    return result

if __name__ == "__main__":
    print(lookup("Shivam"))