import os
from crewai import Agent, Task, Crew, Process
from calculator_tool import calculate

# Directly assign environment variables
os.environ["OPENAI_API_KEY"] = "sk-apikey"  # Replace with your actual API key
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"



print("## Welcome to the Math Whiz")

# Function to validate math input
def get_math_input():
    while True:
        math_input = input("What is your math equation: ")
        try:
            # Attempt to evaluate the expression to check its validity
            eval(math_input)
            return math_input
        except Exception as e:
            print(f"Invalid equation. Please enter a valid math expression. Error: {e}")

math_input = get_math_input()

# Set up the math agent
math_agent = Agent(
    role="Math Magician",
    goal="You are able to evaluate any math expression",
    backstory="YOU ARE A MATH WHIZ.",
    verbose=True,
    tools=[calculate]
)

# Set up the writer agent
writer = Agent(
    role="Writer",
    goal="Craft compelling explanations based on results of math equations.",
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.  
    You transform complex concepts into compelling narratives.""",
    verbose=True
)

# Define the first task
task1 = Task(
    description=math_input,
    expected_output="Give full details in bullet points.",
    agent=math_agent
)

# Define the second task
task2 = Task(
    description="""Using the insights provided, explain in great detail how the equation and result 
    were formed.""",
    expected_output="""Explain in great detail and save in markdown. Do not add the triple tick marks at the 
                    beginning or end of the file. Also don't say what type it is in the first line.""",
    output_file="markdown/math.md",
    agent=writer
)

# Create the crew with the defined agents and tasks
crew = Crew(
    agents=[math_agent, writer],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True
)

# Kick off the crew's tasks and capture the result
try:
    result = crew.kickoff()
    print(result)
except Exception as e:
    print(f"An error occurred during processing: {e}")
