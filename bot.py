# Imports
from cmath import inf
from random import random
import math
import torch
from torch import nn
from copy import deepcopy
from pipe import WIDTH, HEIGHT
torch.set_grad_enabled(False)

class Bot:

    next_id = 1

    @classmethod
    def _generate_id(cls):
        result = cls.next_id
        cls.next_id += 1
        return result

    def __init__(self, *, brain):
        self.id = self._generate_id()
        self._brain = brain

    @property
    def brain(self):
        return self._brain

    @brain.setter
    def brain(self, value):
        self._brain = value

    def think(self, state_vars):
        tensor_state_vars = list_to_tensor(state_vars)
        outputs = self.brain.network(tensor_state_vars)
        return outputs.tolist()

    @classmethod
    def copy(cls, brain):
        return cls(brain = brain)

    def combine(self, other):
        child = self.copy(brain=self._brain)

        self_params = dict(self.brain.network.named_parameters())
        other_params = dict(other.brain.network.named_parameters())
        child_params = dict(child.brain.network.named_parameters())

        for name, param in child_params.items():
            randmat = torch.rand_like(param)
            mask = (randmat <= 0.5).long()
            new_param = mask * self_params[name].data + (1-mask) * other_params[name].data
            child_params[name].data.copy_(new_param)
        
        child.brain.network.load_state_dict(child_params)
        return child

    # Override repr
    def __repr__(self):
        return f"{typename(self)} with id={self.id}"

class BotBrain(nn.Module):

    def __init__(self, nodes):
        super().__init__()
        self._nodes = nodes
        n_input, n_hidden = self._nodes
        n_output = 3                                
        self.network = nn.Sequential(
            nn.Linear(n_input, n_hidden),
            nn.Sigmoid(),
            nn.Linear(n_hidden, n_output),
            nn.Sigmoid()
        )

    @property
    def nodes(self):
        return self._nodes

    def mutate(self, rate, magnitude):
        mutated = deepcopy(self)
        dict_params = dict(mutated.network.named_parameters())
        for name, param in dict_params.items():
            randmat_mask = torch.rand_like(param) # random uniform like param to generate mask
            mask = (randmat_mask <= rate).long() # choose which parameters to mutate
            randmat = torch.randn_like(param) #- 0.5 # random normal like param centered at zero for mutations
            mutmat = magnitude * randmat * mask # mutation effect at selected masking positions
            dict_params[name].data.copy_(param.data + mutmat) # add selective mutation to original parameters
        
        mutated.network.load_state_dict(dict_params) 
        return mutated


    # Override repr
    def __repr__(self):
        return f"{typename(self)}(nodes = {self.nodes})"
 

class Bird(Bot):
    def __init__(self, brain):
        super().__init__(brain=brain)
        self.x = 64
        self.y = 200
        self.r = 12
        self.gravity = 0.8
        self.lift = -12
        self.velocity = 0
        self.score = 0
        self.fitness = 0

    def find_closest_pipe(self, pipes):
        closest = None
        record = inf

        for pipe in pipes:
            diff = pipe.x - self.x
            if diff > 0 and diff < record:
                record = diff
                closest = pipe

        return closest

    def think(self, closest_pipe):
        
        if closest_pipe is not None:
            inputs = [None] * 5
            inputs[0] = map(closest_pipe.x, self.x, WIDTH)
            inputs[1] = map(closest_pipe.top, 0, HEIGHT)
            inputs[2] = map(closest_pipe.bottom, 0, HEIGHT)
            inputs[3] = map(self.y, 0, HEIGHT)
            inputs[4] = map(self.velocity, -10, 10)

            tensor_state_vars = list_to_tensor(inputs)
            outputs = self.brain.network(tensor_state_vars)
            #print(inputs)

            if outputs[1] > outputs[0]:
                self.up()

    def up(self):
        self.velocity += self.lift

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        self.score += 1

    def hit_top_bottom(self):
        return self.y > HEIGHT or self.y < 0 


class BirdBrain(BotBrain):
    def __init__(self, nodes):
        super().__init__(nodes=nodes)
        n_input, n_hidden = self._nodes
        n_output = 2                                
        self.network = nn.Sequential(
            nn.Linear(n_input, n_hidden),
            nn.Sigmoid(),
            nn.Linear(n_hidden, n_output),
            nn.Softmax(dim=0)
        )


def typename(obj):
    return type(obj).__name__

def list_to_tensor(list):
    return torch.Tensor(list)

def pick_one(prob_list, bot_generation):
    index = 0
    r = random()

    while r > 0:
        _, prob = prob_list[index]
        r = r - prob
        index += 1

    index = index - 1
    one_bot_id = prob_list[index][0]
    one_bot = [bot for bot in bot_generation if bot.id == one_bot_id][0]
    return one_bot

def calculate_fitness(score):
    return math.pow(score, 2) #math.exp(score)

def map(value, current_min, current_max, new_min = 0, new_max = 1):
    scaled = (value - current_min) / (current_max - current_min)
    return scaled * (new_max - new_min) + new_min
