from bot import *
from simple_number_guessing import *


l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# for el in l:
#     l.remove(el)
#     print(f"Removing element: {el}")    
#     print(l)

# for el in reversed(l):
#     l.remove(el)
#     print(f"Removing element: {el}")
#     print(l)


n_games = 200

scores = []

for _ in range(n_games):
    #brain = BotBrain(nodes = (4,8))
    #bot = Bot(brain = brain)
    game_score = play(player="halfing", bot=None)
    scores.append(game_score)

avg = sum(scores)/n_games
print("The average is ", round(avg,2))

# prob_list = [0.1, 0.05, 0.6, 0.25]

# #print(prob_list, len(prob_list))

# draws = {0:0, 1:0, 2:0, 3:0} 

# for _ in range(10000):
#     draw = pick_one(prob_list)
#     draws[draw] += 1




# print(draws)

# brain1 = BotBrain(nodes=(2,3))
# parent1 = NegotiationBot(brain=brain1)
# print(dict(parent1.brain.network.named_parameters()), "\n")
# brain2 = BotBrain(nodes=(2,3))
# parent2 = NegotiationBot(brain=brain2)
# print(dict(parent2.brain.network.named_parameters()), "\n")
# bot = parent1.combine(parent2)
# print(dict(bot.brain.network.named_parameters()), "\n")