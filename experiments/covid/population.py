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

            if index < 16:
             self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, state= "S"))
            else:
                self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, state="I"))

