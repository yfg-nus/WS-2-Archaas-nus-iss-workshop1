import os
from dotenv import load_dotenv

from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

llm_name = "gpt-4"

client = OpenAI(api_key=openai_key)

# Create a agent
class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        response = client.chat.completions.create(
            model=llm_name,
            temperature=0.0,
            messages=self.messages,
        )
        return response.choices[0].message.content


prompt = """
You run in a loop of Thought, Action, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 5 * 7 / 2
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

fruit_cost:
e.g. fruit_cost: Apple
returns the cost of a fruit


""".strip()


# Implement the functions actions
def calculate(what):
    return eval(what)


def fruit_cost(name):
    masses = {
        "Apple": 3.5,
        "Pear": 4.8,
        "Orange": 5.7,
        "Grape": 4.1,
        "Peach": 5.5
    }
    return f"{name} costs {masses[name]}"


known_actions = {"calculate": calculate, "fruit_cost": fruit_cost}


# Create the agent
agent = Agent(system=prompt)

# ----- simple query ------
# response = agent("How much does Apple cost?")
# print(response)
# #
# #
# response = fruit_cost("Apple")
# next_message = f"Observation: {response}"
# print(next_message)
# #
# response = agent(next_message)
# print(response)

# # # all messages
# print(f" Messages--> {agent.messages}")
# ----- END simple query ------


# ----- Complex query ------
# question = "What is the combined cost of Orange and Grape?"
# response = agent(question)
# #
# print(response)
# #
# next_prompt = "Observation: {}".format(fruit_cost("Orange"))
# print(next_prompt)
#
# # call the agent again with the next prompt
# res = agent(next_prompt)
# print(res)
#
#
# next_prompt = "Observation: {}".format(fruit_cost("Grape"))
# print(next_prompt)
#
# # call the agent again with the next prompt
# res = agent(next_prompt)
# print(res)
#
# # calculate the combined cost
# next_prompt = "Observation: {}".format(eval("5.7+4.1"))
# print(next_prompt)
#
# # call the agent again with the next prompt
# res = agent(next_prompt)
# print(
#     f"Final answer is {res}"
# )
# ----- END Complex query  ------

# ----- Final solution - Automate our AI Agent ------
# Create a loop to automate the agent until the agent returns an answer

import re

action_re = re.compile(r"^Action: (\w+): (.*)$")


# Create a query function
def query(question, max_turns=10):
    i = 0
    bot = Agent(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split("\n") if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return


question = "What is the combined cost of Orange and Grape and Peach?"
query(question)


# Function to handle the interactive query
# def query_interactive():
#     bot = Agent(prompt)
#     max_turns = int(input("Enter the maximum number of turns: "))
#     i = 0
#
#     while i < max_turns:
#         i += 1
#         question = input("You: ")
#         result = bot(question)
#         print("Bot:", result)
#
#         actions = [action_re.match(a) for a in result.split("\n") if action_re.match(a)]
#         if actions:
#             action, action_input = actions[0].groups()
#             if action not in known_actions:
#                 print(f"Unknown action: {action}: {action_input}")
#                 continue
#             print(f" -- running {action} {action_input}")
#             observation = known_actions[action](action_input)
#             print("Observation:", observation)
#             next_prompt = f"Observation: {observation}"
#             result = bot(next_prompt)
#             print("Bot:", result)
#         else:
#             print("No actions to run.")
#             break
#
#
# if __name__ == "__main__":
#     query_interactive()


