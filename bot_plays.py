from bot import *
from simple_number_guessing import *

smart_brain = BotBrain(nodes = (4,8))
simple_brain = BotBrain(nodes = (4,8))

smart_bot = Bot(brain = smart_brain)
simple_bot = Bot(brain = simple_brain)

smart_bot.brain.network.load_state_dict(torch.load("bots/best_bot_weights.pth"))

#play(player="bot", bot=bot, verbose=True)

n_games = 1

scores_smart_bot = []
scores_simple_bot = []
scores_halfing = []

for _ in range(n_games):

    game_score_smart_bot = play(player="bot", bot = smart_bot, verbose=True)
    scores_smart_bot.append(game_score_smart_bot)

    game_score_simple_bot = play(player="bot", bot = simple_bot, verbose=True)
    scores_simple_bot.append(game_score_simple_bot)

    game_score_halfing = play(player="halfing", bot = None, verbose=True)
    scores_halfing.append(game_score_halfing)

avg_smart_bot = sum(scores_smart_bot)/n_games
avg_simple_bot = sum(scores_simple_bot)/n_games
avg_halfing = sum(scores_halfing)/n_games

# print("The smart bot average is ", round(avg_smart_bot,2))
# print("The simple bot average is ", round(avg_simple_bot,2))
# print("The halfing average is ", round(avg_halfing,2))