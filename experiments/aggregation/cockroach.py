import numpy as np
import pygame
import random
import time, threading
from threading import Timer

from typing import Tuple
from experiments.aggregation.config import config

from simulation.agent import Agent
from experiments.aggregation.config import config
from simulation.utils import *


class Cockroach(Agent):
    """ """
    def __init__(
            self, pos, v, aggregate, index: int, image: str = "experiments/aggregation/images/ant.png"
    ) -> None:

        super(Cockroach, self).__init__(
            pos,
            v,
            image,
            max_speed=config["agent"]["max_speed"],
            min_speed=config["agent"]["min_speed"],
            mass=config["agent"]["mass"],
            width=config["agent"]["width"],
            height=config["agent"]["height"],
            dT=config["agent"]["dt"],
            index=index
        )

        self.aggregation = aggregate
        self.timer = 0
        self.state = "wander"




    def change_state(self, state) -> None:
        state = self.state
        for obstacle in self.flock.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.sensing = "site"

        if state == "wander":
            force = self.wander(wander_dist, wander_radius, wander_angle)
        elif state == "still":
            self.max_speed, self.min_speed = 0, 0
        #elif state == "leave":






    def site_behavior(self, behaviour = "join") -> None:
        if behaviour == "join":
            num_neighbors = len(self.aggregation.find_neighbors(self, config["cockroach"]["radius_view"]))
            if num_neighbors <= 5:
                p = 0.33
            elif num_neighbors >= 5 <= 10:
                p = 0.66
            else:
                p = 1
            if random.random() < p:
                self.min_speed = 0
                self.max_speed = 0



            #leave



    def update_actions(self) -> None:
        # calculate how many seconds
              # if more than 10 seconds close the game
            #print(seconds)  # print how many seconds
            for obstacle in self.aggregation.objects.obstacles:
                collide = pygame.sprite.collide_mask(self, obstacle)
                if bool(collide):
                    self.avoid_obstacle()


            for site in self.aggregation.objects.sites:
                col = pygame.sprite.collide_mask(self, site)
                if bool(col):
                    self.timer += 1
                    print(self.timer)
                    if self.timer % 5 == 0:
                        self.site_behavior()



        #if self.max_speed == 0 and self.min_speed == 0:

           # if self.max_speed == 0:

                #threading.Timer(1.0)
                #num_neighbors = len(self.flock.find_neighbors(self, config["cockroach"]["radius_view"]))
               # p_leave = min(1, num_neighbors / 100 + leave_constant)
                #self.change_state(state="leave")
