import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_community.tools import tool
import sympy as sp


# Define the calculation tool
@tool("calculate")
def calculate(equation):
    """Useful for solving math equations safely."""
    try:
        result = sp.sympify(equation).evalf()
        return result
    except Exception as e:
        return f"Error evaluating equation: {e}"

