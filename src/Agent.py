from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv
import os

class Agent:
    """
    Base class for creating AI-powered conversation agents using OpenAI's API.
    
    This class provides the foundation for creating agents with distinct personalities
    that can engage in conversations about specific topics. Each agent maintains
    its own conversation history and can respond contextually based on its persona.
    """
    def __init__(self, name, persona, topic, model='gpt-5-mini'):
        """
        Initialize an Agent with a name, personality, topic, and AI model.
        
        Args:
            name (str): The name of the agent
            persona (str): Detailed description of the agent's personality and speaking style
            topic (str): The topic the agent will be discussing
            model (str): OpenAI model to use for responses (default: 'gpt-5-mini')
        """
        self.name = name
        self.persona = persona
        self.topic = topic
        self.model = model
        
        # Initialize the system messages that define the agent's behavior
        self.messages = [
            {"role": "system", "content": f"Your name is {self.name}. You are {self.persona}."},
            {"role": "system", "content": "Your responses should mimic real human conversation.  No headings or bullet points, just natural flowing text that aligns with your persona."},
            {"role": "system", "content": f"The topic of discussion is: {self.topic}."},
            {"role": "system", "content": f"Try not to repeat yourself or use similar phrases over and over again. Keep it fresh and engaging."}
        ]
        
        # Store all API responses for potential future analysis
        self.responses = []
        
        # Load OpenAI API key from environment variables
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        
    def ask(self, related_text: str, meta_prompt: str, indent_paragraphs=True) -> str:
        """
        Generate a response from the agent based on context and a specific prompt.
        
        Args:
            related_text (str): Previous conversation context or related information
            meta_prompt (str): Specific instruction or question for the agent to respond to
            indent_paragraphs (bool): Whether to indent paragraphs in the response (default: True)
            
        Returns:
            str: The agent's response, optionally with indented paragraphs
        """
        # Send the conversation context and prompt to OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages + [
                {"role": "assistant", "content": related_text},
                {"role": "user", "content": meta_prompt}
            ]
        )
        
        # Store the response for potential analysis
        self.responses.append(response)
        
        # Format the response with optional paragraph indentation
        if indent_paragraphs:
            return response.choices[0].message.content.replace("\n", "\n\t")
        else:
            return response.choices[0].message.content
    
    def __repr__(self):
        """
        Return a string representation of the Agent for debugging purposes.
        
        Returns:
            str: String representation showing agent's key attributes
        """
        return f"Agent(name={self.name}, persona={self.persona}, model={self.model})"
    
class Debater(Agent):
    """
    Specialized Agent class for debate participants.
    
    Extends the base Agent class to include debate-specific functionality,
    including taking a stance (Pro or Con) on a topic and limiting response length
    for structured debate formats.
    """
    def __init__(self, name, persona, topic, side: Literal['Pro', 'Con'], model='gpt-5-mini'):
        """
        Initialize a Debater agent with a specific stance on the debate topic.
        
        Args:
            name (str): The name of the debater
            persona (str): Detailed description of the debater's personality and style
            topic (str): The debate topic
            side (Literal['Pro', 'Con']): Which side of the argument the debater supports
            model (str): OpenAI model to use (default: 'gpt-5-mini')
        """
        # Initialize the base Agent class
        super().__init__(name, persona, topic, model)
        self.side = side
        
        # Add debate-specific system messages
        self.messages.extend([
            {"role": "system", "content": f"You are on the {self.side} side of the argument.  You should always argue in favor of your side."},
            {"role": "system", "content": "Try to keep your responses to a maximum of 250 words."}
        ])

class Moderator(Agent):
    """
    Specialized Agent class for debate moderation.
    
    Extends the base Agent class for moderating debates. The moderator
    typically manages the flow of conversation and provides neutral guidance.
    """
    def __init__(self, name, persona, topic, model='gpt-5-mini'):
        """
        Initialize a Moderator agent for managing debate flow.
        
        Args:
            name (str): The name of the moderator
            persona (str): Description of the moderator's style and approach
            topic (str): The debate topic being moderated
            model (str): OpenAI model to use (default: 'gpt-5-mini')
        """
        # Initialize the base Agent class
        super().__init__(name, persona, topic, model)
        # Set the moderator's role identifier
        self.side = 'Moderator'


if __name__ == "__main__":
    """
    Example usage of the Debater class.
    
    Creates a sample debater and demonstrates how to get an opening statement.
    This is primarily for testing and development purposes.
    """
    dave = Debater(
        name="Dave",
        persona="A quick witted man who loves to poke fun at the others side in an arrogant way.  He is very clever in his arguments and loves to use humor to make his points.",
        topic="Parking tickets should be abolished.",
        side='Pro'
    )
    print(dave.ask("", "What is your opening statement?"))
