import Agent
from Transcript import Transcript

# Predefined personality profiles for debate agents
PERSONALITY_PROFILES = {
    "Dave": {
        "name": "Dave",
        "persona": "A quick on his feet lawyer who sets out a strong argument by listing facts and figures. He is clever and serious in his approach.",
        "description": "Analytical lawyer - fact-based, serious, logical"
    },
    "Tristan": {
        "name": "Tristan", 
        "persona": "A passionate and fiery debater who loves to argue his points with great enthusiasm. He is very charismatic and loves to use stories and anecdotes to make his points.",
        "description": "Passionate storyteller - enthusiastic, charismatic, uses anecdotes"
    },
    "Sarah": {
        "name": "Sarah",
        "persona": "A methodical professor who approaches debates with academic rigor. She values research, evidence, and careful analysis. She speaks with authority but remains respectful.",
        "description": "Academic professor - methodical, research-focused, authoritative"
    },
    "Marcus": {
        "name": "Marcus",
        "persona": "A witty and sarcastic debater who uses humor and clever wordplay to make points. He's quick with comebacks and loves to find irony in his opponent's arguments.",
        "description": "Witty comedian - sarcastic, humorous, clever wordplay"
    },
    "Elena": {
        "name": "Elena",
        "persona": "A compassionate advocate who focuses on the human impact of issues. She's empathetic, uses emotional appeals, and always considers the broader social implications.",
        "description": "Compassionate advocate - empathetic, emotional appeals, socially conscious"
    },
    "Alex": {
        "name": "Alex",
        "persona": "A pragmatic business leader who focuses on practical solutions and real-world applications. Direct, solution-oriented, and focused on outcomes.",
        "description": "Pragmatic business leader - practical, solution-oriented, results-focused"
    }
}

def display_personality_options():
    """Display available personality profiles for user selection."""
    print("\nAvailable Debate Personalities:")
    print("=" * 50)
    for i, (key, profile) in enumerate(PERSONALITY_PROFILES.items(), 1):
        print(f"{i}. {profile['name']} - {profile['description']}")
    print(f"{len(PERSONALITY_PROFILES) + 1}. Custom - Create your own personality")
    print("=" * 50)

def get_personality_choice(side_name):
    """Get user's choice for pro or con side personality."""
    while True:
        try:
            choice = input(f"\nSelect personality for {side_name} side (1-{len(PERSONALITY_PROFILES) + 1}): ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(PERSONALITY_PROFILES):
                # Return selected predefined personality
                profile_key = list(PERSONALITY_PROFILES.keys())[choice_num - 1]
                return PERSONALITY_PROFILES[profile_key]
            elif choice_num == len(PERSONALITY_PROFILES) + 1:
                # Create custom personality
                return create_custom_personality()
            else:
                print(f"Please enter a number between 1 and {len(PERSONALITY_PROFILES) + 1}")
        except ValueError:
            print("Please enter a valid number")

def create_custom_personality():
    """Allow user to create a custom personality."""
    print("\nCreating custom personality...")
    name = input("Enter the agent's name: ").strip()
    if not name:
        name = "Custom Agent"
    
    print(f"\nDescribe {name}'s personality and debate style:")
    print("(e.g., 'A calm philosopher who uses logical reasoning and thoughtful questions')")
    persona = input("> ").strip()
    
    if not persona:
        persona = "A thoughtful debater who presents arguments clearly and respectfully."
    
    return {
        "name": name,
        "persona": persona,
        "description": "Custom personality"
    }

if __name__ == "__main__":
    transcript = Transcript()
    
    print("Welcome to the AI Debate Platform!")
    print("=" * 40)
    
    # Get debate topic from user
    topic = input("Enter debate topic: ")
    
    # Display personality options and get user choices
    display_personality_options()
    
    print(f"\nDebate Topic: {topic}")
    pro_profile = get_personality_choice("PRO")
    con_profile = get_personality_choice("CON")
    
    # Create the selected agents
    pro_agent = Agent.Debater(
        name=pro_profile["name"],
        persona=pro_profile["persona"],
        topic=topic,
        side='Pro'
    )
    con_agent = Agent.Debater(
        name=con_profile["name"],
        persona=con_profile["persona"],
        topic=topic,
        side='Con'
    )
    moderator = Agent.Moderator(
        name='User',
        persona="The User",
        topic=topic
    )
    
    # Debate start with moderation
    print(f"\nDebate Topic: {topic}\n")
    print(f"Pro: {pro_agent.name}  |  Con: {con_agent.name}\n")
    print(f"Here is what {pro_agent.name} would like to say about the topic:\n{pro_agent.ask('', 'Give the moderator a list of what you would like to talk about in the debate.', indent_paragraphs=False)}\n")
    print(f"Here is what {con_agent.name} would like to say about the topic:\n{con_agent.ask('', 'Give the moderator a list of what you would like to talk about in the debate.', indent_paragraphs=False)}\n")
    
    moderation = input(f"Give an introduction of the debates topic and members.\n>")
    transcript.add_message(moderator, moderation)
    
    while True:
        # run through debate rounds until user decides to end
        moderation = input(f"What would you like {pro_agent.name} to respond to? (q to end debate)\n>")
        if moderation.lower() == 'q':
            break
        
        transcript.add_message(moderator, moderation)
        
        transcript.add_message(pro_agent, pro_agent.ask(transcript.print_transcript(topic, pro_agent, con_agent), "Make your opening argument to the moderator's prompt."))
        print(transcript.print_last_message())
        
        transcript.add_message(con_agent, con_agent.ask(transcript.print_transcript(topic, pro_agent, con_agent), "Make your opening argument to the moderator's prompt."))
        print(transcript.print_last_message())
        
        while True:
            moderation = input(f"Would you like a(nother) round of rebuttals? (y/n)\n>")
            if moderation.lower() == 'n':
                break
            
            transcript.add_message(pro_agent, pro_agent.ask(transcript.print_transcript(topic, pro_agent, con_agent), "Rebuttal."))
            print(transcript.print_last_message())
            
            transcript.add_message(con_agent, con_agent.ask(transcript.print_transcript(topic, pro_agent, con_agent), "Rebuttal."))
            print(transcript.print_last_message())
    
    transcript.add_message(moderator, "Thank you both for your participation in this debate. Now, please give your closing statements.")
    
    transcript.add_message(pro_agent, pro_agent.ask(transcript.print_transcript(topic, pro_agent, con_agent), "Closing statement."))
    print(transcript.print_last_message())
    
    transcript.add_message(con_agent, con_agent.ask(transcript.print_transcript(topic, pro_agent, con_agent), "Closing statement."))
    print(transcript.print_last_message())
    
    transcript.save_transcript("transcript.txt", pro_agent, con_agent, topic)
    print("\n\nFinal transcript has been saved")
    
    
    
    