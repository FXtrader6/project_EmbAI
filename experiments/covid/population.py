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
        self.wow = True

    def initialize(self, num_agents: int) -> None:
        """
        Args:
            num_agents (int):

        """
        if config["population"]["obstacles"]:
            object_loc = config["base"]["object_location"]

            if config["population"]["outside"]:
                scale = [150, 150]
            else:
                scale = [800, 800]

            # shelter locations and sizes
            scale_for_building1 = [300, 600]
            building1loc = config["base"]["shelter1_loc"]
            scale_for_building2 = [300, 600]
            building2loc = config["base"]["shelter2_loc"]

            hospital = (
                "experiments/covid/images/hos.png"
                # if config["aggregation"]["convex"]
                # else "experiments/flocking/images/redd.png"
            )
            building1 = (
                "experiments/covid/images/new1.png"
                # if config["aggregation"]["convex"]
                # else "experiments/flocking/images/redd.png"
            )

            building2 = (
                "experiments/covid/images/new2.png"
                # if config["aggregation"]["convex"]
                # else "experiments/flocking/images/redd.png"
            )
            self.objects.add_object(
                file=hospital, pos=object_loc, scale=scale, obj_type="site"
            )
            self.objects.add_object(
                file=building2, pos=building1loc, scale=scale_for_building1, obj_type="obstacle"
            )
            self.objects.add_object(
                file=building1, pos=building2loc, scale=scale_for_building2, obj_type="obstacle"
            )
            min_x1, max_x1 = area(building1loc[0], scale_for_building1[0])
            min_y1, max_y1 = area(building1loc[1], scale_for_building1[1])
            min_x2, max_x2 = area(building2loc[0], scale_for_building2[0])
            min_y2, max_y2 = area(building2loc[1], scale_for_building2[1])
        # To Do
        # code snipet (not complete) to avoid initializing agents on obstacles
        # given some coordinates and obstacles in the environment, this repositions the agent
        for index, agent in enumerate(range(num_agents)):
            coordinates1 = generate_coordinates(self.screen)
            coordinates2 = generate_coordinates(self.screen)
            # if obstacles present re-estimate the corrdinates
            while (
                    coordinates1[0] >= max_x1
                    or coordinates1[0] <= min_x1
                    or coordinates1[1] >= max_y1
                    or coordinates1[1] <= min_y1
                    or coordinates2[0] >= max_x2 -20
                    or coordinates2[0] <= min_x2 +20
                    or coordinates2[1] >= max_y2
                    or coordinates2[1] <= min_y2
            ):
                coordinates1 = generate_coordinates(self.screen)
                coordinates2 = generate_coordinates(self.screen)

            if index < 12:
                self.add_agent(Person(pos=np.array(coordinates1), v=None, population=self, index=index, state="V"))
            elif index < 25:
                self.add_agent(Person(pos=np.array(coordinates2), v=None, population=self, index=index, state="V"))
            elif index < 58:
                self.add_agent(Person(pos=np.array(coordinates1), v=None, population=self, index=index, state="S"))
            elif index < 90:
                self.add_agent(Person(pos=np.array(coordinates2), v=None, population=self, index=index, state="M"))
            elif index < 95:
                self.add_agent(Person(pos=np.array(coordinates1), v=None, population=self, index=index, state="I"))
            else:
                self.add_agent(Person(pos=np.array(coordinates2), v=None, population=self, index=index, state="I"))

            # 12,25, 58 ,90, 95
            # 25,50, 70, 90 ,95
            # 38, 75, 83, 90, 95

            '''if config["population"]["obstacles"]:  # you need to define this variable
                for obj in self.objects.obstacles:
                    rel_coordinate = relative(
                        coordinates, (obj.rect[0], obj.rect[1])
                    )
                    # print(rel_coordinate)
                    try:
                        while obj.mask.get_at(rel_coordinate):
                            coordinates = generate_coordinates(self.screen)
                            rel_coordinate = relative(
                                coordinates, (obj.rect[0], obj.rect[1])
                            )

                    except IndexError:
                        pass'''
