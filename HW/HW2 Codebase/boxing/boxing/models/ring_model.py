import logging
import math
from typing import List

from boxing.models.boxers_model import Boxer, update_boxer_stats
from boxing.utils.logger import configure_logger
from boxing.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class RingModel:
    def __init__(self):
        self.ring: List[Boxer] = []

    def fight(self) -> str:
        """Simulates a fight between two boxers and returns the boxer's name that won the fight.

        Returns:
            str: A string representing the name of the boxer that won the fight.

        Raises:
            ValueError: if there is less than two boxers in the ring.
        
        """
        logger.info("Received request to simulate fight")
        if len(self.ring) < 2:
            logger.warning("unable to fight, less than two boxers are in the ring")
            raise ValueError("There must be two boxers to start a fight.")
        boxer_1, boxer_2 = self.get_boxers()

        skill_1 = self.get_fighting_skill(boxer_1)
        skill_2 = self.get_fighting_skill(boxer_2)

        # Compute the absolute skill difference
        # And normalize using a logistic function for better probability scaling
        delta = abs(skill_1 - skill_2)
        normalized_delta = 1 / (1 + math.e ** (-delta))

        random_number = get_random()

        if random_number < normalized_delta:
            winner = boxer_1
            loser = boxer_2
        else:
            winner = boxer_2
            loser = boxer_1

        update_boxer_stats(winner.id, 'win')
        update_boxer_stats(loser.id, 'loss')

        self.clear_ring()
        logger.info("fight successfully executed")
        return winner.name

    def clear_ring(self):
        """Deletes all boxers in ring.

        """
        logger.info("Received request to clear ring")
        if not self.ring:
            logger.info("Ring is already cleared")
            return
        logger.info("Ring is successfully cleared")
        self.ring.clear()
        

    def enter_ring(self, boxer: Boxer):
        """Adds a boxer into the ring.

        Args:
            boxer (Boxer): The an instance of the Boxer class to be added into the ring.

        Raises:
            TypeError: If boxer is not Type Boxer.
            ValueError: If the ring has two or more boxers.
       
        """
        logger.info("Attempting to add a boxer into the ring")
        if not isinstance(boxer, Boxer):
            logger.warning("Invalid boxer type provided.")
            raise TypeError(f"Invalid type: Expected 'Boxer', got '{type(boxer).__name__}'")

        if len(self.ring) >= 2:
            logger.warning("Attempted to add more than Two boxers into the ring.")
            raise ValueError("Ring is full, cannot add more boxers.")

        logger.info(f"boxer {boxer} is successfully added to the ring")
        self.ring.append(boxer)

    def get_boxers(self) -> List[Boxer]:
        """Retrieves the list of Boxers in the ring.
        
        Returns: 
            List[Boxer]: A list of Boxer instances in the ring.
       
       """
        logger.info("Attempting to obtain the list of all boxers")
        if not self.ring:
            pass
        else:
            pass

        return self.ring

    def get_fighting_skill(self, boxer: Boxer) -> float:
        """Retrieves the skill of a boxer
        
        Args:
            boxer (Boxer): the Boxer instance whose skill will be calculated.
        
        Returns: 
            float: A float representing the Boxer instance's skill.
        
        Raises:
            logging needs to be implemented"""
        # Arbitrary calculations
        logger.info(f"Attempting to calculate boxer {boxer}'s skill")
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier

        logger.info("skill successfully calculated")
        return skill
