from openai import OpenAI
from dotenv import load_dotenv
from typing import Literal
import os

class Agent:
    def __init__(self, name: str, persona: str, model='gpt-5-mini'):
        self.name = name
        self.persona = persona
        self.model = model
        
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        self.person = f"Your name is {self.name}. You are {self.persona}."
        
        self.responses = []  # Store previous responses
        
    def set_side(self, side: Literal['Pro', 'Con', 'Moderator', 'Fact Checker']):
        self.side = side
        self.person += f" You are playing the role of {self.side} side of this debate."
        
    def respond(self, transcript_text: str, meta_prompt: str) -> str:
        openai = OpenAI(api_key=self.api_key)
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.person},
                {"role": "system", "content": "You are to respond in the style of your assigned role of this debate based on the transcript so far."},
                {"role": "system", "content": "Respond like as if you human in this debate.  Dont use headings and don't use lists.  Your response should feel natural."},
                {"role": "system", "content": "Try to keep your response close to 250 words or less."},
                
                {"role": "assistant", "content": transcript_text},
                {"role": "user", "content": meta_prompt}
            ]
        )
        
        self.responses.append(response)
        return response.choices[0].message.content
    
    def __repr__(self):
        return f"Agent(name={self.name}, persona={self.persona}, side={getattr(self, 'side', 'Unassigned')})"