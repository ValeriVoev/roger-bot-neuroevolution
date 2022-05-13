from pipe import *
from bot import *
import math

n_birds = 500

# def reset_game(best_bird):

#     counter = 0
#     if best_bird is not None:
#         print(best_bird, best_bird.score)
#         best_bird.score = 0
#         print(best_bird.score)
#     pipes = []

#     return best_bird, counter, pipes

# def next_generation():
#     reset_game()
#     normalize_fitness(all_birds)
#     active_birds = generate(all_birds)
#     all_birds = deepcopy(active_birds)

#     return all_birds, active_birds

# def generate(old_birds):
#     new_birds = []
#     for bird in old_birds:
#         pass
        

n_generations = 100

def normalize_fitness(birds):
    sum_score = 0
    for bird in birds:
        exp_score = math.pow(bird.score, 2)
        sum_score += exp_score

    for bird in birds:
        bird.fitness = math.pow(bird.score, 2) / sum_score

    return birds


def play_game(prev_generation, prob_list, old_birds):

    # Initialize game
    active_birds = []
    all_birds = []
    pipes = []
    high_score = 0
    n_pipes = 0

    # Set frame counter
    counter = 0

    # Generate birds
    for _ in range(n_birds):
        
        if prev_generation == 0:
            brain = BirdBrain(nodes = (5, 8))
            bird = Bird(brain)

        else:
            ## Generate next generation of bots
            parent1 = pick_one(prob_list, old_birds)
            parent2 = pick_one(prob_list, old_birds)
            bird = parent1.combine(parent1)
            bird.brain = bird.brain.mutate(rate = 0.1, magnitude = 0.5)
        
        all_birds.append(bird)
        active_birds.append(bird)
    
    while True:

        for pipe in pipes:
            pipe.update()
            if pipe.passed():
                pipes.remove(pipe)
    
        for bird in reversed(active_birds):
            closest_pipe = bird.find_closest_pipe(pipes)
            bird.think(closest_pipe)
            bird.update()
            #print(bird.id, bird.score)
            #input("Press Enter to continue...")
        
            for pipe in pipes:
                if pipe.hits(bird):
                    active_birds.remove(bird)
                    break

            if bird.hit_top_bottom():
                if bird in active_birds:
                    active_birds.remove(bird)


        if counter % 75 == 0:
            # Add pipe
            pipe = Pipe()
            pipes.append(pipe)
            n_pipes += 1

        temp_high_score = 0
        temp_best_bird = None

        for bird in active_birds:
            s = bird.score
            if s > temp_high_score:
                temp_high_score = s
                temp_best_bird = bird

        if temp_high_score > high_score:
            high_score = temp_high_score
            best_bird = temp_best_bird

        if len(active_birds) == 0:
            print("Game Over")
            print(f"Best bird in generation {generation} has score {high_score} passing {n_pipes} pipes.") 
            all_birds = normalize_fitness(all_birds)
            prob_list = [(bird.id, bird.fitness) for bird in all_birds]
            old_birds = all_birds
            
            # fitsum = 0
            # for bird in all_birds:
            #     fitsum += bird.fitness
            #     print(bird, bird.score, bird.fitness)
            # print(fitsum)
            break

        counter += 1
    
    return prob_list, old_birds

for generation in range(n_generations):

    if generation == 0:
        prob_list, old_birds = play_game(generation, None, None)
    else:
        prob_list, old_birds = play_game(generation, prob_list, old_birds)



