from experiments.covid.config import config
from experiments.covid.person import Person
from simulation.agent import Agent

from simulation.swarm import Swarm
from simulation.utils import *
import numpy as np


class Population(Swarm):
    """Class that represents the Population for the Covid experiment. TODO"""

    def __init__(self, screen_size) -> None:
        super(Population, self).__init__(screen_size)
        self.object_loc = config["population"]["outside"]

    def initialize(self, num_agents: int) -> None:
        """
        Args:
            num_agents (int):

        """
        if config["population"]["obstacles"]:
            object_loc = config["base"]["object_location"]

            if config["population"]["outside"]:
                scale = [300, 300]
            else:
                scale = [800, 800]

            filename = (
                "experiments/covid/images/env.png"
            )

            self.objects.add_object(
                file=filename, pos=object_loc, scale=scale, obj_type="obstacle"
            )
            min_x, max_x = area(object_loc[0], scale[0])
            min_y, max_y = area(object_loc[1], scale[1])
        # To Do
        # code snipet (not complete) to avoid initializing agents on obstacles
        # given some coordinates and obstacles in the environment, this repositions the agent
        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)
            #print(coordinates)
            if config["population"]["obstacles"]:  # you need to define this variable
                for obj in self.objects.obstacles:
                    rel_coordinate = relative(
                        coordinates, (obj.rect[0], obj.rect[1])
                    )
                    # print(rel_coordinate)
                    try:
                        while obj.mask.get_at(rel_coordinate):
                            coordinates = generate_coordinates(self.screen)
                            print(coordinates)
                            rel_coordinate = relative(
                                coordinates, (obj.rect[0], obj.rect[1])
                            )

                    except IndexError:
                        pass

            if index < 45:
             self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, state= "S"))
            elif index <90:
                self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, state="M"))
            else:
                self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, state="I"))

    


            # code added for social distancing

    def find_neighbor_velocity_center_separation(self, person: Agent, neighbors: list) -> Tuple[float, float, float]:
            """
                Compute the total averaged sum of the neighbors' velocity, position and distance with regards to the considered
                agent
                :param boid: Agent
                :param neighbors: list

            """
            neighbor_sum_v, neighbor_sum_pos, separate = (
                np.zeros(2),
                np.zeros(2),
                np.zeros(2),
            )

            for neigh in neighbors:
                neighbor_sum_v += neigh.v
                neighbor_sum_pos += neigh.pos
                difference = (
                        person.pos - neigh.pos
                )  # compute the distance vector (v_x, v_y)
                difference /= norm(
                    difference
                )  # normalize to unit vector with respect to its maginiture
                separate += difference  # add the influences of all neighbors up

            return neighbor_sum_v / len(neighbors), neighbor_sum_pos / len(neighbors), separate / len(neighbors)

