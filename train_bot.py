import os
from bot import *
from simple_number_guessing import *

n_bots = 500 # Number of bots in generation
n_generations = 500

bot_save_path = "bots"

for generation in range(n_generations):

    bot_scores = {}
    new_bot_generation = []
    sum_fitness = 0

    for i in range(n_bots):
        
        if generation == 0:
            #print(i)
            brain = BotBrain(nodes = (4, 8))
            bot = Bot(brain = brain)
        else:
            ## Generate next generation of bots
            #print(i)
            parent1 = pick_one(prob_list, old_bot_generation)
            parent2 = pick_one(prob_list, old_bot_generation)
            bot = parent1.combine(parent1)
            bot.brain = bot.brain.mutate(rate = 0.1, magnitude = 0.5)
    
        score = round_of_plays(player="bot", bot=bot)
        fitness = calculate_fitness(score)
        #print(generation, bot.id)
        bot_scores[bot.id] = (score, fitness)
        new_bot_generation.append(bot)
        sum_fitness += fitness
    
    old_bot_generation = new_bot_generation
    prob_list = [(id, bot_scores[id][1]/sum_fitness) for id in bot_scores.keys()]

    best_bots = sorted(bot_scores.items(), key = lambda kv: kv[1][1], reverse=True)[:3]
    best_bot_id = best_bots[0][0]
    best_bot_score = best_bots[0][1][0]
    best_bot = [bot for bot in new_bot_generation if bot.id == best_bot_id][0]
    print(generation, best_bot_score, best_bots)
    if best_bot_score > 100:
        torch.save(best_bot.brain.network.state_dict(), os.path.join(bot_save_path, "best_bot_weights.pth"))
        break

    generation += 1

#####
# draws = {key:0 for key in bot_scores.keys()}

# for _ in range(10000):
#     draw = pick_one(prob_list, new_bot_generation).id
#     draws[draw] += 1

# print(draws)

# sum_prob = 0
# max_prob = 0
# min_prob = 1

# for bot, score_tup in bot_scores.items():
#     score, fitness = score_tup
#     prob = fitness / sum_fitness
#     bot_scores[bot] = (score, fitness, prob)
#     sum_prob += prob

#     if prob < min_prob:
#         min_prob = prob

#     if prob > max_prob:
#         max_prob = prob

# sorted_bots = sorted(bot_scores.items(), key = lambda kv: kv[1][1], reverse=True)

# print(sorted_bots[:10], "\n")

# print(sum_prob, sum_fitness, min_prob, max_prob)

