from Agent import Agent
from datetime import datetime

class Transcript:
    class Comment:
        def __init__(self, content):
            self.timestamp = datetime.now()
            self.content = content
            
        def __repr__(self):
            return f"{self.__class__.__name__}(timestamp={self.timestamp}, content={self.content})"
    
    class Dialogue:
        def __init__(self, speaker: str, message: str):
            self.speaker = speaker
            self.timestamp = datetime.now()
            self.message = message
            
        def __repr__(self):
            return f"{self.__class__.__name__}(speaker={self.speaker}, timestamp={self.timestamp}, message={self.message})"
    
    def __init__(self, topic: str, pro_agent: Agent, con_agent: Agent, moderator_agent: Agent):
        self.topic = topic
        self.pro_agent = pro_agent
        assert self.pro_agent.side == 'Pro', "pro_agent must be assigned the 'Pro' side"
        self.con_agent = con_agent
        assert self.con_agent.side == 'Con', "con_agent must be assigned the 'Con' side"
        self.moderator_agent = moderator_agent
        assert self.moderator_agent.side == 'Moderator', "moderator_agent must be assigned the 'Moderator' side"
        
        self.transcript = []  # List to hold the transcript exchanges
        
    def add_comment(self, comment: str):
        self.transcript.append(self.Comment(comment))
        
    def add_dialogue(self, speaker: str, message: str):
        self.transcript.append(self.Dialogue(speaker, message))
        
    def get_transcript(self) -> str:
        result = "="*42
        result += f"\nTopic: {self.topic}"
        result += f"\nPro: {self.pro_agent.name}  |  Con: {self.con_agent.name}\n"
        result += "="*42 + "\n\n"