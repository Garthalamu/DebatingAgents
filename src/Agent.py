from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv
import os

class Agent:
    def __init__(self, name, persona, topic, model='gpt-5-mini'):
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
        return f"Agent(name={self.name}, persona={self.persona}, model={self.model})"
    
class Debater(Agent):
    def __init__(self, name, persona, topic, side: Literal['Pro', 'Con'], model='gpt-5-mini'):
        super().__init__(name, persona, topic, model)
        self.side = side
        
        self.messages.extend([
            {"role": "system", "content": f"You are on the {self.side} side of the argument.  You should always argue in favor of your side."},
            {"role": "system", "content": "Try to keep your responses to a maximum of 250 words."}
        ])

class Moderator(Agent):
    def __init__(self, name, persona, topic, model='gpt-5-mini'):
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
