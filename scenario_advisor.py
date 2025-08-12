import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Google API Key not found in environment variables.")

# Initialize Gemini Model
llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=api_key)

def get_scenario_based_response(scenario_description):
    """
    Generate a Constitution of India based legal analysis for a given scenario.
    
    Args:
        scenario_description (str): The situation or hypothetical case.
    
    Returns:
        str: Legal analysis and guidance based on the Constitution of India.
    """

    prompt = f"""
    You are a Constitutional law expert specializing in the Constitution of India.
    Analyze the following scenario and provide a factual, unbiased explanation:

    Scenario:
    {scenario_description}

    Your response should include:
    1. Relevant Articles, Schedules, or Amendments (cite exact numbers and names).
    2. Explanation of how they apply to the scenario.
    3. Possible legal interpretations or outcomes.
    4. Any relevant Supreme Court or High Court precedents (if applicable).
    5. Limitations or areas of uncertainty in constitutional interpretation.

    Use clear, simple language so a non-lawyer can understand.
    Format the answer with clear headings and bullet points.
    """

    try:
        response = llm.invoke(prompt)
        # Handle both string and object responses
        if hasattr(response, 'content'):
            return response.content
        elif isinstance(response, str):
            return response
        else:
            return str(response)
    except Exception as e:
        return f"Error generating response: {str(e)}"

if __name__ == "__main__":
    scenario = """
    A state government passes a law restricting online speech criticizing its ministers,
    citing maintenance of public order. Is this constitutional?
    """
    print(get_scenario_based_response(scenario))