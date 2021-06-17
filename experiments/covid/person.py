import numpy as np
import pygame
import random
import time, threading
import sys

from simulation.agent import Agent
from experiments.covid.config import config
from simulation.utils import *

class Person(Agent):
    """ """
    def __init__(
            self, pos, v, population, state, index: int, image:str = "experiments/covid/images/blue.png"
    ) -> None:
        super(Person, self).__init__(
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
        self.prev_pos = None
        self.prev_v = None
        self.width = config["agent"]["width"]
        self.height = config["agent"]["height"]
        self.population = population
        self.t_join = 0
        self.t_attempt_leave = 0
        self.t_leave_site = 0
        self.rec_timer = 0
        self.init_timer = 0
        self.stop = False
        self.avoided_obstacles: bool = False
        self.state = state
        self.on_site = False
        self.n_agents = config["base"]["n_agents"]


        if state == "S":
            self.image = image_with_rect( #change image
                    "experiments/covid/images/blue.png", [self.width, self.height])[0]
        elif state == "I":
            self.image = image_with_rect( #change image
                    "experiments/covid/images/corona.png", [self.width, self.height])[0]




    def change_state(self) -> None:

        if self.state == "I":
            image = image_with_rect( #change image
                    "experiments/covid/images/corona.png", [self.width, self.height])[0]
        elif self.state == "S":
            image = image_with_rect(  # change image
                "experiments/covid/images/blue.png", [self.width, self.height])[0]
        else:
            image = image_with_rect(  # change image
                "experiments/covid/images/green.png", [self.width, self.height])[0]
        return image


    def site_behavior(self, behaviour = "join") -> None:
        #print(self.type)
        if behaviour == "join":
            num_neighbors = len(self.population.find_neighbors(self, config["cockroach"]["radius_view"]))
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
            num_neighbors = len(self.population.find_neighbors(self, config["cockroach"]["radius_view"]))
            if num_neighbors <= 5:
                p_leave = 0.1

            elif 5 <= num_neighbors <= 10:
                p_leave = 0.05
            else:
                p_leave = 0.01
            if random.random() < p_leave:
                self.state = "wander"
                self.t_leave_site += 1

                self.on_site = True
                #self.timer = 0
                self.change_state()

                #self.change_state(state="wander")




            #leave


    def update_actions(self) -> None:
            #print(self.type)
            #infection timer to recover
            self.init_timer+=1
            if self.init_timer==500:
                pygame.quit()
                sys.exit()

            #self.population.add_point(self.listo)

            if self.state == "I":
                self.rec_timer += 1

            # infection timer to recover
            if self.rec_timer == 2000:
                self.state = "R"
                self.image = self.change_state()
                self.rec_timer = 0

            # infect susceptible neighbors
            if self.state == "I" and random.random() < 0.1:
                num_neighbors = (self.population.find_neighbors(self, config["person"]["radius_view"]))
                for neighbor in num_neighbors:
                    if neighbor.state == "S":
                        neighbor.state = "I"
                        neighbor.image = self.change_state()

            #avoid obstacles
            for obstacle in self.population.objects.obstacles:
                collide = pygame.sprite.collide_mask(self, obstacle)
                if bool(collide):
                    # If boid gets stuck because when avoiding the obstacle ended up inside of the object,
                    # resets the position to the previous one and do a 180 degree turn back
                    if not self.avoided_obstacles:
                        self.prev_pos = self.pos.copy()
                        self.prev_v = self.v.copy()

                    else:
                        self.pos = self.prev_pos.copy()
                        self.v = self.prev_v.copy()

                    self.avoided_obstacles = True
                    self.avoid_obstacle()
                    self.image = self.change_state()
                    return
            self.prev_v = None
            self.prev_pos = None

            self.avoided_obstacles = False

            #

            #if self.min_speed != 0 and self.max_speed != 0 and self.timer2 == 0:

'''            for site in self.population.objects.sites:
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
                                                '''