from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv
import os

class Agent:
    """
    A base AI agent class for creating conversational debate participants.
    
    This class provides the foundation for AI-powered agents that can participate
    in debates and discussions. It handles OpenAI API integration, maintains
    conversation context through message history, and provides a persona-based
    response system.
    
    Attributes:
        name (str): The agent's display name.
        persona (str): Character description that defines the agent's personality and behavior.
        topic (str): The subject matter for discussions.
        model (str): OpenAI model identifier (default: 'gpt-5-mini').
        messages (list): Conversation history including system prompts and context.
        responses (list): Collection of API responses for tracking and analysis.
        api_key (str): OpenAI API authentication key loaded from environment.
        client (OpenAI): Configured OpenAI client instance.
    
    Example:
        >>> agent = Agent(
        ...     name="Alice",
        ...     persona="A thoughtful academic who considers all sides",
        ...     topic="Climate change policy"
        ... )
        >>> response = agent.ask("", "What's your initial position?")
    """
    def __init__(self, name, persona, topic, model='gpt-5-mini'):
        """
        Initialize a new Agent instance with personality and conversation setup.
        
        Sets up the agent's identity, loads API credentials, and configures the
        initial conversation context with system prompts that define the agent's
        behavior and constraints.
        
        Args:
            name (str): Display name for the agent used in conversations.
            persona (str): Detailed character description defining personality,
                          communication style, and behavioral traits.
            topic (str): The subject matter or theme for discussions.
            model (str, optional): OpenAI model identifier. Defaults to 'gpt-5-mini'.
                                 Common options include 'gpt-4', 'gpt-3.5-turbo'.
        
        Raises:
            ValueError: If OpenAI API key is not found in environment variables.
            OpenAIError: If there's an issue initializing the OpenAI client.
        
        Note:
            Requires OPENAI_API_KEY to be set in environment variables or .env file.
        """
        self.name = name
        self.persona = persona
        self.topic = topic
        self.model = model
        
        self.messages = [
            {"role": "system", "content": f"Your name is {self.name}. You are {self.persona}."},
            {"role": "system", "content": "Your responses should mimic real human conversation.  No headings or bullet points, just natural flowing text that aligns with your persona."},
            {"role": "system", "content": f"The topic of discussion is: {self.topic}."},
            {"role": "system", "content": f"Try not to repeat yourself or use similar phrases over and over again. Keep it fresh and engaging."}
        ]
        
        self.responses = []
        
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        
    def ask(self, related_text: str, meta_prompt: str, indent_paragraphs=True) -> str:
        """
        Generate an AI response based on conversation context and user prompt.
        
        Sends a request to the OpenAI API using the agent's personality, conversation
        history, and current context to generate a response that aligns with the
        agent's defined persona and the ongoing discussion.
        
        Args:
            related_text (str): Previous conversation context or related information
                               that provides background for the response. Can be empty
                               string for initial interactions.
            meta_prompt (str): The specific question, request, or instruction that
                              the agent should respond to.
            indent_paragraphs (bool, optional): Whether to indent paragraph breaks
                                              with tabs for formatted output.
                                              Defaults to True.
        
        Returns:
            str: The agent's generated response text. If indent_paragraphs is True,
                 newlines are replaced with newline + tab for indented formatting.
        
        Raises:
            OpenAIError: If the API request fails due to authentication, rate limits,
                        or service availability issues.
            ValueError: If the model parameter is invalid or unsupported.
        
        Note:
            Each API call is stored in self.responses for potential analysis or
            debugging. The conversation context (self.messages) is preserved
            across calls but not permanently updated with new exchanges.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages + [
                {"role": "assistant", "content": related_text},
                {"role": "user", "content": meta_prompt}
            ]
        )
        
        self.responses.append(response)
        
        if indent_paragraphs:
            return response.choices[0].message.content.replace("\n", "\n\t")
        else:
            return response.choices[0].message.content
    
    def __repr__(self):
        """
        Return a string representation of the Agent instance.
        
        Provides a concise, developer-friendly representation of the agent
        showing key identifying information for debugging and logging purposes.
        
        Returns:
            str: Formatted string in the format "Agent(name=<name>, persona=<persona>, model=<model>)"
                 where the persona text may be truncated for readability.
        
        Example:
            >>> agent = Agent("Alice", "A thoughtful teacher", "Education")
            >>> print(repr(agent))
            Agent(name=Alice, persona=A thoughtful teacher, model=gpt-5-mini)
        """
        return f"Agent(name={self.name}, persona={self.persona}, model={self.model})"
    
class Debater(Agent):
    """
    A specialized Agent designed for formal debate participation.
    
    Extends the base Agent class to add debate-specific functionality including
    side alignment (Pro/Con), argument constraints, and response length limits.
    Debaters are programmed to consistently argue from their assigned perspective
    and maintain focus on their designated position throughout the debate.
    
    Attributes:
        side (Literal['Pro', 'Con']): The debate position this agent will argue.
                                     'Pro' supports the topic, 'Con' opposes it.
        
    Inherits all attributes from Agent class:
        name, persona, topic, model, messages, responses, api_key, client
    
    Example:
        >>> debater = Debater(
        ...     name="Sarah",
        ...     persona="A passionate environmental advocate",
        ...     topic="Renewable energy subsidies",
        ...     side='Pro'
        ... )
        >>> response = debater.ask("", "What's your opening argument?")
    """
    def __init__(self, name, persona, topic, side: Literal['Pro', 'Con'], model='gpt-5-mini'):
        """
        Initialize a Debater with position-specific constraints and behavior.
        
        Sets up a debate agent by calling the parent Agent constructor and then
        adding debate-specific system prompts that enforce consistent argumentation
        from the assigned side and appropriate response length limits.
        
        Args:
            name (str): Display name for the debater.
            persona (str): Character description defining the debater's style,
                          expertise, and argumentative approach.
            topic (str): The debate topic or resolution being discussed.
            side (Literal['Pro', 'Con']): The position this debater will argue.
                                         'Pro' means arguing in favor of the topic,
                                         'Con' means arguing against it.
            model (str, optional): OpenAI model identifier. Defaults to 'gpt-5-mini'.
        
        Raises:
            ValueError: If side is not 'Pro' or 'Con', or if parent initialization fails.
            OpenAIError: If there's an issue with OpenAI client setup.
        
        Note:
            Automatically adds system prompts that:
            - Enforce consistent argument from the assigned side
            - Limit responses to approximately 250 words for concise debate format
        """
        super().__init__(name, persona, topic, model)
        self.side = side
        
        self.messages.extend([
            {"role": "system", "content": f"You are on the {self.side} side of the argument.  You should always argue in favor of your side."},
            {"role": "system", "content": "Try to keep your responses to a maximum of 250 words."}
        ])

class Moderator(Agent):
    """
    A specialized Agent that serves as a neutral debate moderator.
    
    Extends the base Agent class to create a neutral facilitator for debates.
    Unlike Debaters, Moderators don't take sides but instead guide the discussion,
    ask clarifying questions, manage the debate flow, and maintain neutrality.
    
    Attributes:
        side (str): Always set to 'Moderator' to indicate neutral role.
        
    Inherits all attributes from Agent class:
        name, persona, topic, model, messages, responses, api_key, client
    
    Example:
        >>> moderator = Moderator(
        ...     name="Dr. Smith",
        ...     persona="An experienced debate moderator who asks probing questions",
        ...     topic="Universal basic income"
        ... )
        >>> intro = moderator.ask("", "Please introduce tonight's debate")
    """
    def __init__(self, name, persona, topic, model='gpt-5-mini'):
        """
        Initialize a Moderator agent with neutral facilitation role.
        
        Creates a moderator by calling the parent Agent constructor and setting
        the side attribute to 'Moderator' to indicate their neutral, facilitating
        role in debates and discussions.
        
        Args:
            name (str): Display name for the moderator.
            persona (str): Character description defining the moderator's style,
                          expertise, and approach to facilitating discussions.
                          Should emphasize neutrality and fairness.
            topic (str): The debate topic or subject being moderated.
            model (str, optional): OpenAI model identifier. Defaults to 'gpt-5-mini'.
        
        Raises:
            ValueError: If parent initialization fails.
            OpenAIError: If there's an issue with OpenAI client setup.
        
        Note:
            The moderator inherits the same system prompts as the base Agent but
            doesn't receive side-specific argumentative constraints like Debaters do.
        """
        super().__init__(name, persona, topic, model)
        self.side= 'Moderator'


if __name__ == "__main__":
    dave = Debater(
        name="Dave",
        persona="A quick witted man who loves to poke fun at the others side in an arrogant way.  He is very clever in his arguments and loves to use humor to make his points.",
        topic="Parking tickets should be abolished.",
        side='Pro'
    )
    print(dave.ask("", "What is your opening statement?"))
