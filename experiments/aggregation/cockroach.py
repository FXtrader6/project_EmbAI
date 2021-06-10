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
        self.timer2 = 0
        self.timer3 = 0
        self.stop = False
        self.state = "wander"
        self.on_site = False




    def change_state(self) -> None:

        if self.state == "wander":
            self.v = self.set_velocity()
        elif self.state == "still":
            self.v *= 0


    def site_behavior(self, behaviour = "join") -> None:
        if behaviour == "join":
            num_neighbors = len(self.aggregation.find_neighbors(self, config["cockroach"]["radius_view"]))
            if num_neighbors <= 5:
               p = 0.33
            elif num_neighbors >= 5 <= 10:
               p = 0.66
            else:
                p = 0.8
            if random.random() < p:
               self.state = "still"
               self.change_state()
        elif behaviour == "leave":
            num_neighbors = len(self.aggregation.find_neighbors(self, config["cockroach"]["radius_view"]))
            if num_neighbors <= 5:
                p_leave = min(1, (0.4 * num_neighbors + 1) / config["base"]["n_agents"])

            elif (0.25 * config["base"]["n_agents"]) >= num_neighbors <= (0.5 * config["base"]["n_agents"]):
                p_leave = min(1, (0.6 * num_neighbors + 1) / config["base"]["n_agents"])

            # 1 ----> (0.25 * config["base"]["n_agents"]) >= num_neighbors <= (0.5 * config["base"]["n_agents"]):
            # 2 ----> (0.4 * config["base"]["n_agents"]) >= num_neighbors <= (0.65 * config["base"]["n_agents"]):
            # 3 ----> (0.35 * config["base"]["n_agents"]) >= num_neighbors <= (0.6 * config["base"]["n_agents"]):
            # 4 ----> (0.35 * config["base"]["n_agents"]) >= num_neighbors <= (0.6 * config["base"]["n_agents"]):
            else:
                p_leave = min(1, (0.01 * num_neighbors + 1) / config["base"]["n_agents"])
            if random.random() < p_leave:
                self.state = "wander"
                self.timer3 += 1

                self.on_site = True
                #self.timer = 0
                self.change_state()

                #self.change_state(state="wander")




            #leave



    def update_actions(self) -> None:

            for obstacle in self.aggregation.objects.obstacles:
                collide = pygame.sprite.collide_mask(self, obstacle)
                if bool(collide):
                    self.avoid_obstacle()

            #if self.min_speed != 0 and self.max_speed != 0 and self.timer2 == 0:

            for site in self.aggregation.objects.sites:
                col = pygame.sprite.collide_mask(self, site)
                if bool(col):

                    self.timer += 1

                    if self.timer % 35 == 0:
                        if self.on_site == False:
                            self.site_behavior()
                            self.timer = 0

            if self.timer3 >= 1:
                self.timer3 +=1
                #print(self.timer3)
            if self.timer3 > 250:
                self.on_site = False
                self.timer3 = 0

            if self.state == "still":
                self.timer2 += 1
                #print(self.timer2)
                if self.timer2 % 500 == 0:
                    self.site_behavior(behaviour="leave")
                    self.timer2 = 0











        #if self.max_speed == 0 and self.min_speed == 0:

           # if self.max_speed == 0:

                #threading.Timer(1.0)
                #num_neighbors = len(self.flock.find_neighbors(self, config["cockroach"]["radius_view"]))
               # p_leave = min(1, num_neighbors / 100 + leave_constant)
                #self.change_state(state="leave")
