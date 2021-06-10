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
        self.t_join = 0
        self.t_attempt_leave = 0
        self.t_leave_site = 0
        self.roach_timer = 0
        self.stop = False
        self.state = "wander"
        self.on_site = False
        self.n_agents = config["base"]["n_agents"]




    def change_state(self) -> None:

        if self.state == "wander":
            self.v = self.set_velocity()
        elif self.state == "still":
            self.v *= 0


    def site_behavior(self, behaviour = "join") -> None:
        if behaviour == "join":
            num_neighbors = len(self.aggregation.find_neighbors(self, config["cockroach"]["radius_view"]))
            if num_neighbors <= 5:
                p_join = 0.5
            elif 5 <= num_neighbors <= 10:
                p_join = 0.8
            else:
                p_join = 0.99
            if random.random() < p_join:
               self.state = "still"
               self.change_state()
        elif behaviour == "leave":
            num_neighbors = len(self.aggregation.find_neighbors(self, config["cockroach"]["radius_view"]))
            if num_neighbors <= 5:
                p_leave = 0.4

            elif 5 <= num_neighbors <= 10:
                p_leave = 0.2

            # 1 ----> (0.25 * config["base"]["n_agents"]) >= num_neighbors <= (0.5 * config["base"]["n_agents"]):
            # 2 ----> (0.4 * config["base"]["n_agents"]) >= num_neighbors <= (0.65 * config["base"]["n_agents"]):
            # 3 ----> (0.35 * config["base"]["n_agents"]) >= num_neighbors <= (0.6 * config["base"]["n_agents"]):
            # 4 ----> (0.35 * config["base"]["n_agents"]) >= num_neighbors <= (0.6 * config["base"]["n_agents"]):
            else:
                p_leave = 0.1
            if random.random() < p_leave:
                self.state = "wander"
                self.t_leave_site += 1

                self.on_site = True
                #self.timer = 0
                self.change_state()

                #self.change_state(state="wander")




            #leave



    def update_actions(self) -> None:
            self.roach_timer += 1
            if self.roach_timer % 9000 ==0:
                time.sleep(45)


            for obstacle in self.aggregation.objects.obstacles:
                collide = pygame.sprite.collide_mask(self, obstacle)
                if bool(collide):
                    self.avoid_obstacle()

            #if self.min_speed != 0 and self.max_speed != 0 and self.timer2 == 0:

            for site in self.aggregation.objects.sites:
                col = pygame.sprite.collide_mask(self, site)
                if bool(col):

                    self.t_join += 1

                    if self.t_join % 35 == 0:
                        if self.on_site == False:
                            self.site_behavior()
                            self.t_join = 0

            if self.t_leave_site >= 1:
                self.t_leave_site +=1
                #print(self.timer3)
            if self.t_leave_site > 250:
                self.on_site = False
                self.t_leave_site = 0

            if self.state == "still":
                self.t_attempt_leave += 1
                #print(self.timer2)
                if self.t_attempt_leave % 500 == 0:
                    self.site_behavior(behaviour="leave")
                    self.t_attempt_leave = 0











        #if self.max_speed == 0 and self.min_speed == 0:

           # if self.max_speed == 0:

                #threading.Timer(1.0)
                #num_neighbors = len(self.flock.find_neighbors(self, config["cockroach"]["radius_view"]))
               # p_leave = min(1, num_neighbors / 100 + leave_constant)
                #self.change_state(state="leave")
