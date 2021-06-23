import numpy as np
import pygame
import random
import time, threading
import sys
import time
from simulation.agent import Agent
from experiments.covid.config import config
from simulation.utils import *
from simulation.utils import normalize, truncate


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
        elif state == "M":
            self.image = image_with_rect( #change image
                    "experiments/covid/images/mask.png", [self.width, self.height])[0]




    def change_state(self) -> None:

        if self.state == "I":
            image = image_with_rect( #change image
                    "experiments/covid/images/corona.png", [self.width, self.height])[0]
        elif self.state == "S":
            image = image_with_rect(  # change image
                "experiments/covid/images/blue.png", [self.width, self.height])[0]
        elif self.state == "M":
            image = image_with_rect(  # change image
                "experiments/covid/images/mask.png", [self.width, self.height])[0]
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
            if self.init_timer==1500:
                print("QUUUUUUUUUUUUUUUUUUUUUUUIT")
                #pygame.quit()
                #sys.exit()

            #self.population.add_point(self.listo)

            if self.state == "I":
                self.rec_timer += 1

            # infection timer to recover
            if self.rec_timer == 1000:
                self.state = "R"
                self.image = self.change_state()
                self.rec_timer = 0

            # infect susceptible neighbors
            if self.state == "I":
                num_neighbors = (self.population.find_neighbors(self, config["person"]["radius_view"]))
                for neighbor in num_neighbors:
                    if neighbor.state == "S" and random.random() < 0.1:
                        neighbor.state = "I"
                        neighbor.image = self.change_state()
                    elif neighbor.state == "M" and random.random() < 0.005:
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

            # code for socia distance below

            align_force, cohesion_force, separate_force = self.neighbor_forces()

            # combine the vectors in one
            steering_force = (
                    align_force * config["person"]["alignment_weight"]
                    + cohesion_force * config["person"]["cohesion_weight"]
                    + separate_force * config["person"]["separation_weight"]
            )

            # adjust the direction of the boid
            self.steering += truncate(
                steering_force / self.mass, config["person"]["max_force"]
            )

            # code for social distance aboves

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


# added code for social distance:
    def neighbor_forces(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
            """
            Find the neighbors of the agent and compute the total align force (force required to align agent with its neighbors'
            total force), cohesion force (force required to move the agent towards the center of mass of its neighbors)
            and separate force considering the total amount of neighbors close to the agent
            """
            # find all the neighbors of a boid based on its radius view
            neighbors = self.population.find_neighbors(self, config["person"]["radius_view"])

            #
            # if there are neighbors, estimate the influence of their forces

            if neighbors:
                pre_align_force, pre_cohesion_force, separate_force = self.population.find_neighbor_velocity_center_separation(self,
                                                                                                                        neighbors)
                align_force = self.align(pre_align_force)
                cohesion_force = self.cohesion(pre_cohesion_force)
            #
            else:
                align_force, cohesion_force, separate_force = (
                    np.zeros(2),
                    np.zeros(2),
                    np.zeros(2)
                )
            return align_force, cohesion_force, separate_force

    def align(self, neighbor_force: np.ndarray):
        """
        Function to align the agent in accordance to neighbor velocity

        Args:
            neighbor_force (np.ndarray):

        """
        return normalize(neighbor_force - self.v)

    def cohesion(self, neighbor_center):
        """
        Function to move the agent towards the center of mass of its neighbors

        Args:
        ----
            neighbor_center:

        """
        force = neighbor_center - self.pos
        return normalize(force - self.v)