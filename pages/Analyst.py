import streamlit as st
import os 
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains import LLMChain
from langchain.agents import load_tools, AgentExecutor, initialize_agent, AgentType, ZeroShotAgent

st.set_page_config(page_title="Stock Analyst", page_icon="📈")

def main():

    # Loading the api keys
    load_dotenv()
    
    # Creating LLM object
    llm = OpenAI(temperature=0.1) 
    tools = load_tools(['serpapi', 'llm-math'], llm=llm)

    news_template = PromptTemplate(
        input_variables=['company', 'when'],
        template="""
        Search for five news of {company} on {when} and list them with bullet.
        """
    )

    rise_or_fall_template = ZeroShotAgent.create_prompt(
        tools=tools, 
        input_variables=['company', 'when'],
        suffix="""
        Did {company}'s stock price rise or fall on {when}? Answer with necessary price values and the result of rise or fall. If the stock market was closed, answer with closed.
        """
    )

    analysis_template = PromptTemplate(
        input_variables=['company', 'news', 'when', 'rise_or_fall'],
        template="""
        Your are an experienced finance analyst.

        Use following news of {company} to analysis the reason of the {rise_or_fall} of its stock price on {when}: {news}
        Explain in details step by step. Must answer with no more than 100 words.
        """
    )

    # Creating Memory objects 
    search_memory = ConversationBufferMemory(input_key='company', memory_key='chat_history')

    analysis_chain = LLMChain(
        llm=llm,
        prompt=analysis_template,
        verbose=True,
        output_key="analysis_result"
    )

    #tools = load_tools(['serpapi', 'news-api'], llm=llm, news_api_key=NEWS_API_KEY)
    news_agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    llm_chain = LLMChain(llm=llm, prompt=rise_or_fall_template)
    rise_or_fall_agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    #rise_or_fall_agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    rise_or_fall_agent_chain = AgentExecutor.from_agent_and_tools(agent=rise_or_fall_agent, tools=tools, verbose=True, memory=search_memory)
        
    st.title('Your Stock Analyst')
    analysis_prompt = st.text_input("Which company's stock would you like to analysis:")
    when_prompt = st.text_input("When:")    
    
    if analysis_prompt and when_prompt:
        rise_or_fall = rise_or_fall_agent_chain.run(company=analysis_prompt, when=when_prompt)
        st.write(f"### :blue[_Rise or Fall_]:")
        st.write(rise_or_fall)

        news = news_agent.run(news_template.format(company=analysis_prompt, when=when_prompt))

        ns = news
        notes = ns.split("-")
        tmp = ""
        for n in notes[1:]:
            tmp = tmp + "\n•  " + n + "\n"
        news = tmp
        #del(tmp)

        st.write(f"### :blue[_News_]:")
        st.write(news)

        analysis = analysis_chain.run(company=analysis_prompt, news=news, when=when_prompt, rise_or_fall=rise_or_fall)
        st.write(f"### :blue[_Analysis_]:")
        st.write(analysis)

        with st.expander("Search History"): 
            st.info(search_memory.buffer)


if __name__ == "__main__":
    main()
