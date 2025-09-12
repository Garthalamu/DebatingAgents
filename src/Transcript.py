from Agent import Agent
from datetime import datetime
import json

class Transcript:
    """
    A class for managing and formatting debate transcripts.
    
    This class handles the collection, storage, and formatting of messages
    from debate participants. It maintains a chronological record of all
    exchanges and can generate formatted transcripts for display or saving.
    """
    def __init__(self):
        """
        Initialize an empty transcript.
        
        Creates a new transcript instance with an empty message list
        ready to collect debate exchanges.
        """
        self.messages = []
        
    def add_message(self, agent: Agent, message: str):
        """
        Add a new message to the transcript with timestamp.
        
        Args:
            agent (Agent): The agent (debater, moderator, etc.) who spoke
            message (str): The content of the message
        """
        self.messages.append({"timestamp": datetime.now(), "agent": agent, "message": message})
        
    def print_transcript(self, topic, pro: Agent, con: Agent, final=False):
        """
        Generate a formatted transcript of the entire debate.
        
        Args:
            topic (str): The debate topic
            pro (Agent): The agent arguing for the pro side
            con (Agent): The agent arguing for the con side
            final (bool): Whether this is the final transcript (adds ending marker)
            
        Returns:
            str: Formatted transcript with headers, timestamps, and messages
        """
        r_string = ""
        r_string += "[TRANSCRIPT OF DEBATE]\n\n"
        r_string += "="*40 + "\n"
        r_string += f"Topic: {topic}\n"
        r_string += f"Pro: {pro.name}  |  Con: {con.name}\n"
        r_string += "="*40 + "\n\n"
        
        # Add each message with timestamp and speaker information
        for entry in self.messages:
            time_str = entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            r_string += f"[{time_str}] {entry['agent'].name} ({entry['agent'].side}):\n\t{entry['message']}\n"
            r_string += "-"*40 + "\n\n"
        
        # Add final marker if this is the complete transcript
        if final:
            r_string += "="*40 + "\n\n"
            r_string += "[END OF DEBATE]"
            
        return r_string
    
    def print_last_message(self):
        """
        Format and return just the most recent message from the transcript.
        
        Returns:
            str: Formatted representation of the last message, or empty string if no messages
        """
        if not self.messages:
            return ""
        
        # Get the most recent message
        entry = self.messages[-1]
        time_str = entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        return f"[{time_str}] {entry['agent'].name} ({entry['agent'].side}):\n\t{entry['message']}\n\n"
    
    def save_transcript(self, filename: str, pro: Agent, con: Agent, topic: str):
        """
        Save the complete transcript to a file.
        
        Args:
            filename (str): Path where the transcript file should be saved
            pro (Agent): The agent arguing for the pro side
            con (Agent): The agent arguing for the con side
            topic (str): The debate topic
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.print_transcript(topic, pro, con, final=True))