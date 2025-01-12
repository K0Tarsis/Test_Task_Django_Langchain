import json
import os
import openai

from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from utils import query_api

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0, openai_api_key=openai.api_key)

system_prompt = """
You are a highly knowledgeable real estate assistant specializing in helping users find properties. Your main tasks involve analyzing user queries and determining the best way to provide accurate and helpful responses. Here's how you should work:

1. Analyze the user's query carefully to determine if accessing data from the Django API is necessary to answer their question.
2. If you decide to fetch data, provide the JSON filters you will use for the API request in the following format:
   ~FETCH_DATA: {/'filter_key1': 'value1', 'filter_key2': 'value2', .../}~
   Ensure the filters are precise and relevant to the query.
3. If the query can be answered without accessing the database, respond directly with a clear and helpful message.
4. You can use the following JSON filters to query the Django API: ['min_price', 'max_price', 'min_area', 'max_area', 'min_bedrooms', 'max_bedrooms', 'min_bathrooms', 'max_bathrooms', 'bathrooms', 'bedrooms', 'address', 'type_of_purchase']. The `type_of_purchase` filter can be either "RENT" or "SALE" with uppercase.
5. If you need to paginate add 'page' filter with value you need, e.g. {..., 'page': 2}.
6. Always prioritize making the best decision to either fetch data or respond directly. If there is any uncertainty about the need to fetch data, err on the side of performing the API query.

Example scenarios:
- Query: "I want houses for rent under 2000 USD."  
  Response: ~FETCH_DATA: {"type_of_purchase": "rent", "max_price": 2000}~
  System Response With Data: data...
  Response: "here are 12 apartments I found: Address: ... Summary: ... Price: ..."

When deciding to fetch data, be explicit about the filters. For example:
- Query: "Find me a house with at least 3 bedrooms and 2 bathrooms in New York."  
  Response: ~FETCH_DATA: {"min_bedrooms": 3, "min_bathrooms": 2, "address": "New York"}~
  System Response With Data: data...
  Response: "here are 6 apartments I found: Address: ... Summary: ... Price: ..."

- Query: "I want apartments in London for sale under 500,000."  
  Response: ~FETCH_DATA: {"type_of_purchase": "sale", "max_price": 500000, "address": "London"}~
  System Response With Data: data...
  Response: "here are 5 apartments I found: Address: ... Summary: ... Price: ..."
  
"""

fetch_prompt_template = PromptTemplate.from_template("""
Fetched data: {fetched_data}
""")

user_prompt_template = PromptTemplate.from_template("""
Respond to the following query:
{query}
""")

def get_llm_response(query, chat_history=None):
    llm_history = [SystemMessage(system_prompt), ]

    if chat_history:

        for message in chat_history:
            if message["sender"] == "user":
                llm_history.append(HumanMessage(content=message["message"]))

            elif message["sender"] == "bot":
                llm_history.append(AIMessage(content=message["message"]))

    llm_history.append(HumanMessage(content=user_prompt_template.format(query=query)))
    llm_response = llm.invoke(llm_history).content.strip()
    llm_history.append(AIMessage(content=llm_response))

    print(llm_response)

    if "FETCH_DATA" in llm_response:

        start_idx = llm_response.index("{")
        end_idx = llm_response.rindex("}") + 1
        filter_json = llm_response[start_idx:end_idx]
        filters = json.loads(filter_json)

        response_data = query_api(filters)

        print(response_data)

        llm_history.append(SystemMessage(content=fetch_prompt_template.format(fetched_data=response_data)))
        llm_history.append(HumanMessage(content=user_prompt_template.format(query=query)))

        final_response = llm.invoke(llm_history).content.strip()

        print(final_response)
        return final_response

    else:

        return llm_response