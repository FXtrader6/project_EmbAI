import numpy as np
import pygame
import time, threading

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
        elif state == "leave":






    def site_behavior(self) -> None:
        for site in self.aggregations.objects.sites:
            collide = pygame.sprite.collide_mask(self, site)
            if bool(collide):
                sensing = "site"
        join_constant = 0.3
        num_neighbors =  len(self.flock.find_neighbors(self, config["cockroach"]["radius_view"]))
        p_join = min(1, num_neighbors / 100 + join_constant)

        #join state
        if sensing == "site" and p_join > np.random.rand() :
            r = np.random.uniform(0, 0.5) #random noise
            time.sleep(0.3 + r) #time function for join -> still
            self.change_state(state="still")
        else:
            self.change_state(state="wander")

            #join behavior



            #leave



    def update_actions(self) -> None:
        for obstacle in self.flock.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

            if self.max_speed == 0:

                threading.Timer(1.0)
                num_neighbors = len(self.flock.find_neighbors(self, config["cockroach"]["radius_view"]))
                p_leave = min(1, num_neighbors / 100 + leave_constant)
                self.change_state(state="leave")

