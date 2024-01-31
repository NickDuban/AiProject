from chatterBot import chatbot
from chatterbot.trainers import ListTrainer

trainer = ListTrainer(chatbot)

trainer.train([
    "Hi there!",
    "Hello",
])
trainer.train([
    "Greetings!",
    "Hello",
    "Hey",
])
dubot = open("../AIProject/dubotAI.txt", "r",encoding='UTF8').readlines()
trainer.train(dubot)
insults = open("../AIProject/insults.txt", "r",encoding='UTF8').readlines()
trainer.train(insults)
complements = open("../AIProject/complements.txt", "r",encoding='UTF8').readlines()
trainer.train(complements)

uinput = "Hello"
while(input != "exit"):
    response = chatbot.get_response(uinput)
    print(response)
    uinput = input()
