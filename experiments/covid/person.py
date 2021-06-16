import numpy as np
import pygame
import random
import time, threading

from simulation.agent import Agent
from experiments.covid.config import config
from simulation.utils import *

class Person(Agent):
    """ """
    def __init__(
            self, pos, v, population, index: int, image : str ="experiments/covid/images/blue.png"
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
        self.width = config["agent"]["width"]
        self.height = config["agent"]["height"]
        self.population = population
        self.t_join = 0
        self.t_attempt_leave = 0
        self.t_leave_site = 0
        self.roach_timer = 0
        self.initialization_timer = 0
        self.stop = False
        self.state = "susceptible"
        self.on_site = False
        self.n_agents = config["base"]["n_agents"]




    def change_state(self) -> None:

        if self.state == "infectious":
            image = image_with_rect( #change image
                    "experiments/covid/images/corona.png", [self.width, self.height])[0]
        elif self.state == "susceptible":
            image = image_with_rect(  # change image
                "experiments/covid/images/blue.png", [self.width, self.height])[0]
        else:
            image = image_with_rect(  # change image
                "experiments/covid/images/green.png", [self.width, self.height])[0]
        return image


    def site_behavior(self, behaviour = "join") -> None:
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
            self.roach_timer += 1
            if random.random() < 0.005 and self.roach_timer < 50:
                self.state = "infectious"
                self.image = self.change_state()

            if self.state == "infectious" and random.random() < 0.2:
                num_neighbors = (self.population.find_neighbors(self, config["person"]["radius_view"]))
                for neighbor in num_neighbors:
                    neighbor.state= "infectious"
                    neighbor.image = self.change_state()

            for obstacle in self.population.objects.obstacles:
                collide = pygame.sprite.collide_mask(self, obstacle)
                if bool(collide):
                    #self.image = self.change_state()
                    self.avoid_obstacle()
                    self.image = self.change_state()


            #if self.min_speed != 0 and self.max_speed != 0 and self.timer2 == 0:

            for site in self.population.objects.sites:
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
