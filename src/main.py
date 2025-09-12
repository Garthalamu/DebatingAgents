import Agent
from Transcript import Transcript

if __name__ == "__main__":
    transcript = Transcript()
    
    topic = input("Enter debate topic: ")
    
    dave = Agent.Debater(
        name="Dave",
        persona="A quick on his feet lawyer who sets out a strong argument by listing facts and figures. He is clever and serious in his approach.",
        topic=topic,
        side='Pro'
    )
    tristan = Agent.Debater(
        name="Tristan",
        persona="A passionate and fiery debater who loves to argue his points with great enthusiasm. He is very charismatic and loves to use stories and anecdotes to make his points.",
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
    print(f"Pro: {dave.name}  |  Con: {tristan.name}\n")
    print(f"Here is what {dave.name} would like to say about the topic:\n{dave.ask('', 'Give the moderator a list of what you would like to talk about in the debate.', indent_paragraphs=False)}\n")
    print(f"Here is what {tristan.name} would like to say about the topic:\n{tristan.ask('', 'Give the moderator a list of what you would like to talk about in the debate.', indent_paragraphs=False)}\n")
    
    moderation = input(f"Give an introduction of the debates topic and members.\n>")
    transcript.add_message(moderator, moderation)
    
    while True:
        # TODO: Make moderator introduction more automated
        # run through debate rounds until user decides to end
        moderation = input(f"What would you like {dave.name} to respond to? (q to end debate)\n>")
        if moderation.lower() == 'q':
            break
        
        transcript.add_message(moderator, moderation)
        
        transcript.add_message(dave, dave.ask(transcript.print_transcript(topic, dave, tristan), "Make your opening argument to the moderator's prompt."))
        print(transcript.print_last_message())
        
        transcript.add_message(tristan, tristan.ask(transcript.print_transcript(topic, dave, tristan), "Make your opening argument to the moderator's prompt."))
        print(transcript.print_last_message())
        
        while True:
            moderation = input(f"Would you like a(nother) round of rebuttals? (y/n)\n>")
            if moderation.lower() == 'n':
                break
            
            transcript.add_message(dave, dave.ask(transcript.print_transcript(topic, dave, tristan), "Rebuttal."))
            print(transcript.print_last_message())
            
            transcript.add_message(tristan, tristan.ask(transcript.print_transcript(topic, dave, tristan), "Rebuttal."))
            print(transcript.print_last_message())
    
    transcript.add_message(moderator, "Thank you both for your participation in this debate. Now, please give your closing statements.")
    
    transcript.add_message(dave, dave.ask(transcript.print_transcript(topic, dave, tristan), "Closing statement."))
    print(transcript.print_last_message())
    
    transcript.add_message(tristan, tristan.ask(transcript.print_transcript(topic, dave, tristan), "Closing statement."))
    print(transcript.print_last_message())
    
    transcript.save_transcript("transcript.txt", dave, tristan, topic)
    print("\n\nFinal transcript has been saved")
    
    
    
    