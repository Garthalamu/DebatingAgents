from Agent import Agent
from datetime import datetime
import json

class Transcript:
    def __init__(self):
        self.messages = []
        
    def add_message(self, agent: Agent, message: str):
        self.messages.append({"timestamp": datetime.now(), "agent": agent, "message": message})
        
    def print_transcript(self, topic, pro: Agent, con: Agent, final=False):
        r_string = ""
        r_string += "[TRANSCRIPT OF DEBATE]\n\n"
        r_string += "="*40 + "\n"
        r_string += f"Topic: {topic}\n"
        r_string += f"Pro: {pro.name}  |  Con: {con.name}\n"
        r_string += "="*40 + "\n\n"
        
        for entry in self.messages:
            time_str = entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            r_string += f"[{time_str}] {entry['agent'].name} ({entry['agent'].side}):\n\t{entry['message']}\n"
            r_string += "-"*40 + "\n\n"
        
        if final:
            r_string += "="*40 + "\n\n"
            r_string += "[END OF DEBATE]"
            
        return r_string
    
    def print_last_message(self):
        if not self.messages:
            return ""
        
        entry = self.messages[-1]
        time_str = entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        return f"[{time_str}] {entry['agent'].name} ({entry['agent'].side}):\n\t{entry['message']}\n\n"
    
    def save_transcript(self, filename: str, pro: Agent, con: Agent, topic: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.print_transcript(topic, pro, con, final=True))