from experiments.covid.config import config
from experiments.covid.person import Person
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
                scale = [200, 200]
            else:
                scale = [800, 800]

            hospital = (
                "experiments/covid/images/hos.png"
            )

            self.objects.add_object(
                file=hospital, pos=object_loc, scale=scale, obj_type="site"
            )
            min_x, max_x = area(object_loc[0], scale[0])
            min_y, max_y = area(object_loc[1], scale[1])
        # To Do
        # code snipet (not complete) to avoid initializing agents on obstacles
        # given some coordinates and obstacles in the environment, this repositions the agent
        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)
            #print(coordinates)
            if config["population"]["obstacles"]:
                if config["population"]["outside"]:
                    while (
                            max_x >= coordinates[0] >= min_x
                            and max_y >= coordinates[1] >= min_y
                    ):
                        coordinates = generate_coordinates(self.screen)
                else:
                    while (
                            coordinates[0] >= max_x
                            or coordinates[0] <= min_x
                            or coordinates[1] >= max_y
                            or coordinates[1] <= min_y
                    ):
                        coordinates = generate_coordinates(self.screen)

            if index < 45:
             self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, state= "S"))
            elif index <90:
                self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, state="M"))
            else:
                self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, state="I"))

