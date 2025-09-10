from Agent import Agent


dave = Agent(name="Dave", persona="a friendly and knowledgeable lawyer with a knack for making complex legal concepts easy to understand.")
alice = Agent(name="Alice", persona="a passionate and articulate social activist who fights for community rights and social justice.")
justin = Agent(name="Justin", persona="an impartial and fair-minded moderator who ensures that debates are conducted respectfully and stay on topic.")

dave.set_side('Pro')
r1 = dave.respond("Parking tickets should be abolished.", "Come up with a list of topics that support your idea to give to the moderator before the debate")

alice.set_side('Con')
r2 = alice.respond("Parking tickets should be abolished.", "Come up with a list of topics that support your idea to give to the moderator before the debate")

justin.set_side('Moderator')
r3 = justin.respond(f"Parking tickets should be abolished.\n\nDaves ideas of the argument:\n{r1}\n\nAlice's ideas of the argument:\n{r2}", "Introduce both sides and their positions.  Then ask the first question to start the debate.")

print("DAVE:", r1)
print("ALICE:", r2)
print("JUSTIN:", r3)
