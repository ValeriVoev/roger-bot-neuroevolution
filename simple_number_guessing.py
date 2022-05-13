from bot import *
from random import randrange, random
import math

def pick_number(N = 100):
    return randrange(N+1)

def response(guess,target):
    if guess-target <= -25:
        return -2
    elif guess-target >= 25:
        return 2
    elif guess-target < 0:
        return -1
    elif guess-target > 0:
        return 1
    else:
        return 0 

response_dict = (
    {-2: "Your guess is too low by at least 25", 
    -1: "Your guess is too low by less than 25", 
    0: "Your guess is correct!", 
    1: "Your guess is too high by less than 25", 
    2: "Your guess is too high by at least 25"}
)

def play(player, bot = None, n_turns = 3, verbose = False):

    target = pick_number()
    guesses = []
    turn = 1

    while turn <= n_turns:
        if turn == 1:
            guess = 50
            guesses.append(guess)
            known_minimum = 0
            known_maximum = 100
            feedback = response(guess, target)
            
        else:
            if player == "halfing":
                guess, known_minimum, known_maximum = halfing_strategy(last_guess=guess, feedback=feedback, known_minimum=known_minimum, known_maximum=known_maximum)
            elif player == "bot":
                guess, known_minimum, known_maximum = bot_strategy(bot = bot, last_guess=guess, feedback=feedback, known_minimum=known_minimum, known_maximum=known_maximum)
            elif player == "random":
                guess = random_strategy()
            else:
                raise ValueError("Player needs to be 'halfing', 'bot' or 'random'")    
            guesses.append(guess)
            feedback = response(guess, target)

        if response(guess, target) == 0:
            # print("You got it! Your score is 100!")
            score = 100 - abs(guess-target)
            if verbose:
                print(f"Your score is: {score}. Target was {target}. Your final guess was {guess} at turn {turn}.")
            break
        
        if turn == n_turns:
            score = 100 - abs(guess-target)
            if verbose:
                print(f"Your score is: {score}. Target was {target}. Your final guess was {guess} at turn {turn}.")

        turn += 1
        print(bot, feedback, guess, target)
        input("Paused...")
        

    return score

def round_of_plays(player, bot = None, n_rounds = 10):
    scores = []
    for _ in range(n_rounds):
        score = play(player = player, bot = bot)
        scores.append(score)
    round_avg_score = sum(scores) / n_rounds
    sq_devs = [(score - round_avg_score)**2 for score in scores]
    stdev = math.sqrt((1/n_rounds)*sum(sq_devs))

    return round_avg_score/stdev

def halfing_strategy(last_guess, feedback, known_minimum, known_maximum):
    
    random_bias = 0.1 * (random() - 0.5) # 
    
    if feedback == -2:
        known_minimum = min(100,last_guess + 25)
        potential_range = known_maximum - known_minimum
        guess = known_minimum + round(potential_range/2 + random_bias)
    elif feedback == -1:
        known_maximum = min(100,last_guess + 25, known_maximum)
        known_minimum = last_guess
        potential_range = known_maximum - known_minimum
        guess = known_minimum + round(potential_range/2 + random_bias)
        while guess == last_guess:
            guess = known_minimum + round(potential_range/2 + random_bias)
        
    elif feedback == 1:
        known_maximum = last_guess
        known_minimum = max(0,last_guess - 25, known_minimum)
        potential_range = known_maximum - known_minimum
        guess = known_minimum + round(potential_range/2 + random_bias)
        while guess == last_guess:
            guess = known_minimum + round(potential_range/2 + random_bias)

    elif feedback == 2:
        known_maximum = max(0,last_guess - 25)
        potential_range = known_maximum - known_minimum
        guess = known_minimum + round(potential_range/2 + random_bias)
    else:
        guess = last_guess
    
    if guess > 100 or guess < 0:
        raise ValueError("Guess is outside [0,100]")

    return guess, known_minimum, known_maximum


def bot_strategy(bot, last_guess, feedback, known_minimum, known_maximum):
    outputs = bot.think([last_guess/100, feedback/2, known_minimum/100, known_maximum/100])
    #print(round(outputs[0], 2), round(outputs[1], 2), round(outputs[2], 2))
    guess = int(round(outputs[0]*100))
    known_minimum = int(round(outputs[1]*100))
    known_maximum = int(round(outputs[2]*100))

    return guess, known_minimum, known_maximum

def random_strategy():
    guess = pick_number()

    return guess