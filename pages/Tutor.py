import streamlit as st
import os 
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

import sys 
sys.path.append('..')
from utils import bullet_format

from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains import LLMChain


st.set_page_config(page_title="Finance Tutor", page_icon="📖")

def main():
    # Loading the api keys
    load_dotenv()

    # Creating the prompt templates
    topic_template = PromptTemplate(
        input_variables=['topic'], 
        template="""
        You are an experienced finance tutor.
        
        Explain the topic: {topic} to a newbie.
        If the topic to explain is not related to finance then just say that "The topic is not related to finance" 
        and do not explain anything.
        """
    )
    
    # 根据解释和wikipedia搜索结果写笔记
    lecture_template = PromptTemplate(
        input_variables=["finance_topic", "wikipedia_research"], 
        template="Write me bullet pointed lecture notes based on the following: {finance_topic}, while leveraging this wikipedia reserch:{wikipedia_research}"
    )

    # Creating Memory objects 
    topic_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')

    # Creating LLM object
    llm = OpenAI(temperature=0.1) 
    
    # Creating chains
    topic_chain = LLMChain(
        llm=llm,
        prompt=topic_template,
        verbose=True,
        output_key="finance_topic",
        memory=topic_memory
    )
    
    lecture_chain = LLMChain(
        llm=llm,
        prompt=lecture_template,
        verbose=True,
        output_key="lecture_notes"
    )

    wiki = WikipediaAPIWrapper()

    # Setting the streamlit app
    st.title('Your Finance Tutor')
    topic_prompt = st.text_input("Which Finance topic would you like to learn:") 
    if topic_prompt: 
        finance_topic = topic_chain.run(topic_prompt)
        wiki_research = wiki.run(topic_prompt)
        lecture_notes = lecture_chain.run(finance_topic=finance_topic, wikipedia_research=wiki_research)

        lecture_notes = bullet_format(lecture_notes)

        st.write(f"Topic: :red[{topic_prompt.capitalize()}]")
        st.write(finance_topic)
        st.write("### :blue[_Wikipedia Notes_]:")
        st.write(wiki_research.replace("Page:", "Term:").replace("Summary:", "\nSummary:"))
        st.write("### :blue[_Useful Lecture Notes_]:")
        st.write(lecture_notes)

        with st.expander("Search History"): 
            st.info(topic_memory.buffer)
    
if __name__ == "__main__":
    main()