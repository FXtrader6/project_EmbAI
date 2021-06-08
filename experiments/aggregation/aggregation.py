from experiments.aggregation.cockroach import Cockroach
from experiments.aggregation.boid import Boid
from simulation.agent import Agent


from experiments.aggregation.config import config
from simulation.utils import *
from simulation.swarm import Swarm
from simulation.utils import area, generate_coordinates, norm



class Aggregations(Swarm):
    """
    Specific flock properties, and flocking environment definition. This class inherits from the base class Swarm.
    It collects every element (agents, sites, and obstacles) of the simulation, and is in charge of commanding each
    agent to update its state, and display the new states frame by frame

    Attributes:
        object_loc

    """
    def __init__(self, screen_size) -> None:
        """
        This function is the initializer of the class Flock.
        :param screen_size:
        """
        super(Aggregations, self).__init__(screen_size)
        self.object_loc = config["aggregation"]["outside"]

    def initialize(self, num_agents: int) -> None:
        """
        Initialize the whole swarm, creating and adding the obstacle objects, and the agent, placing them inside of the
        screen and avoiding the obstacles.
        :param num_agents: int:

        """

        # add obstacle/-s to the environment if present
        if config["aggregation"]["obstacles"]:
            object_loc = config["base"]["object_location"]

            if config["aggregation"]["outside"]:
                scale = [300, 300]
            else:
                scale = [800, 800]

            # shelter locations and sizes
            scale_for_shelter1 = [100, 100]
            shelter1loc = config["base"]["shelter1_loc"]
            scale_for_shelter2 = [150, 150]
            shelter2loc = config["base"]["shelter2_loc"]

            filename = (
                "experiments/aggregation/images/convex.png"
                # if config["aggregation"]["convex"]
                # else "experiments/flocking/images/redd.png"
            )

            shelter1 = (
                "experiments/aggregation/images/greyc1.png"
                # if config["aggregation"]["convex"]
                # else "experiments/flocking/images/redd.png"
            )

            shelter2 = (
                "experiments/aggregation/images/greyc2.png"
                # if config["aggregation"]["convex"]
                # else "experiments/flocking/images/redd.png"
            )

            self.objects.add_object(
                file=filename, pos=object_loc, scale=scale, obj_type="obstacle"
            )

            self.objects.add_object(
                file=shelter1, pos=shelter1loc, scale=scale_for_shelter1, obj_type="site"
            )

            self.objects.add_object(
                file=shelter2, pos=shelter2loc, scale=scale_for_shelter2, obj_type="site"
            )

            min_x, max_x = area(object_loc[0], scale[0])
            min_y, max_y = area(object_loc[1], scale[1])

        # add agents to the environment
        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)

            # if obstacles present re-estimate the corrdinates
            if config["aggregation"]["obstacles"]:
                if config["aggregation"]["outside"]:
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




# THE CODE BELOW WOKRS USING BOID FROM THE FLOCKING ASSIGNMNET
#  NEEDS TO BE SWITCHED OVER TO THE COCKROACH CLASS WHEN FINISHED


            self.add_agent(Boid(pos=np.array(coordinates), v=None, flock=self, index=index))

    def find_neighbor_velocity_center_separation(self, boid: Agent, neighbors: list) -> Tuple[float, float, float]:
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
                    boid.pos - neigh.pos
            )  # compute the distance vector (v_x, v_y)
            difference /= norm(
                difference
            )  # normalize to unit vector with respect to its maginiture
            separate += difference  # add the influences of all neighbors up

        return neighbor_sum_v / len(neighbors), neighbor_sum_pos / len(neighbors), separate / len(neighbors)
