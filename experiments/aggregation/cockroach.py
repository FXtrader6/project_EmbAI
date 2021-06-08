import numpy as np
import pygame

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




        def change_state(self, state="wander") -> None:
            for obstacle in self.flock.objects.obstacles:
                collide = pygame.sprite.collide_mask(self, obstacle)
                if bool(collide):
                    self.sensing = "site"

            if state == "wander":
                force = self.wander(wander_dist, wander_radius, wander_angle)
            elif state == "still":
                self.v = np.zeros(2)



        def site_behavior(self) -> None:
            for site in self.aggregations.objects.sites:
                collide = pygame.sprite.collide_mask(self, site)
                if bool(collide):
                    sensing = "site"
            join_constant = 0.3
            num_neighbors =  len(self.flock.find_neighbors(self, config["cockroach"]["radius_view"]))
            p_join = min(1, num_neighbors / 100 + join_constant)
            #join
            if sensing == "site" and p_join > np.random.rand() :
                pass
            else:
                pass
                #join behavior


            #leave

            pass

        def update_actions(self) -> None:
            pass





