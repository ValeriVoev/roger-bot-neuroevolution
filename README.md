# Evolving a negotiation bot using neuroevolution

## Intro

The purpose is to train a negotiation bot to maximize negotiation value as the difference between the agreed payoff and the reservation price (or BATNA?). The negotiation is a multistage game where the bot and a human player negotiate to buy/sell an asset.

## Neuroevolution

The idea of neuroevolution is to evolve an AI agent to make better decisions based on the principle of "survival of the fittest". The AI agent makes decisions based on an algorithm (typically a neural network) and receives at each stage of the game as inputs the "state" of the game at that point. That state depends on the nature of the game - in many computer games, the state can be all the pixel values of the screen, or some engineered features.

The idea is that a first generation of bots is created using randomized parameters in the AI algorithm, e.g., random initialization of the weights and biases in a neural network. These parameters are considered the "genetic code" or "digital DNA" of the agent and it is these parameters that evolve over time using processes akin to biological evolution such as cross-over and mutation to generate better/fitter generations of agents.

The first generation of agents play against each other and at the end of each game each agent gets assigned a fitness score via a fitness function (e.g., a game score, win/lose, survival time, etc.). The fitness function can be non-linear in order to accentuate differences in fitness scores.

Once we have the fitness scores of all agents, a second generation is created by picking agents with the highest fitness as "parents", combining their digital DNA ("cross-over") and introducing some degree of mutation. Then the second generation of agents play again, fitness scores are assigned and the process continues until some desired level of performance (fitness) is achieved. 

## Specific application to the negotiation bot

1. **Initialization**
    * Choose N - the population size (even)
    * Initialize the bots' "brains" (neural networks) with some reasonably random weights
    * Choose a scoring and fitness function

2. **Play round**
    * Assign N bots to N/2 games
    * At each stage make a decision (accept or not, and if not what the offer should be - see discussion point below)
    * (Optionally), remove bots/end games early - see discussion point below
    * At the end of the game evaluate and normalize bots' fitness

3. **Evolution step**
    * Draw a set of parents with probability according to fitness
    * (Optional) Cross over parents' digital DNA (network weights) to create children
    * Mutate children's digital DNA randomly (with a small probability)

4. **Iterate**
    * Repeat steps 2. and 3. until some convergence/level of fitness is achieved


## Decision/discussion points

* Python/Javascript?
* State variables that describe the state of the game at each stage
* Multi-output network for multistage decision making:
    - first stage: accept vs continue &mdash; binary decision
    - second stage: if continue, value of offer &mdash; continuous output (constrained)
* Fitness function &mdash; final score/value, possibly normalized/non-linear
* In-game elimination of poor bots
