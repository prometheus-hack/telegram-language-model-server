#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, AgentOutputParser
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
from langchain.tools.base import StructuredTool
import requests
import telebot
import os

OPENAI_API = "sk-"

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__f7252ae2e7e4433d965ad37d94d63d6d"
project_name = "Prometheus"
os.environ["LANGCHAIN_PROJECT"] = project_name

BOT_KEY = '6415742729:AAHVyDkHHF57ZsVd9gJjVtXjKE2M9CydzPk'

WELCOME_MSG = f"Привет! ✨ Добро пожаловать в {project_name}, мы поможем Вам отлично провести время! \n Спроси что-нибудь у нашего бота"

AGW_URL = f"https://gw.cg.k-lab.su/"

bot = telebot.TeleBot(BOT_KEY)

def fetch_get_interests(params={}):
    try:
        response = requests.post(AGW_URL + 'api/v1/', json=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print('Error fetching data:', e)
        return None

def get_interests_insight() -> str:
  """Этот инструмент используется для получения данных о достопримечательностях"""
  data = fetch_get_interests()
  return data

sensors_insights_tool = StructuredTool.from_function(get_interests_insight)

chat = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.2, openai_api_key=OPENAI_API)

tools = [sensors_insights_tool]

class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            final_answer = llm_output.split("Final Answer:")[-1].strip()
            print("final is - " + final_answer)
            return AgentFinish(
                return_values={"output": final_answer},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(
            tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output
        )

output_parser = CustomOutputParser()

agent_chain = initialize_agent(
  tools,
  chat,
  max_iterations=4,
  agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
  verbose=True,
  output_parser=output_parser,
  project_name=project_name
)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, WELCOME_MSG)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
  print(message.text)
  bot.reply_to(message, "AI думает... 🤔")
  request = "Ты Ассистент платформы Prometheus, который помогает пользователю с планированием путешествия на автомобиле. Клиент написал: " + message.text
  result = agent_chain(request)
  if (result):
    final_answer = result['output']
    bot.reply_to(message, str(final_answer))


bot.infinity_polling()
