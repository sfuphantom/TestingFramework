#Author : Kevin Litvin
#Date : November 2023
#Description : Model analog waves using mathematical equations for hardware testing

from typing import Union
from abc import ABC, abstractmethod
from enum import Enum
import math
import random

from vcu_communication import (
	APPS1_MIN,
	APPS1_MAX,
	APPS2_MIN,
	APPS2_MAX,
	BSE_MIN,
	BSE_MAX
)

class VCU_Pedals(Enum):
    APPS1 = 1,
    APPS2 = 2,
    BSE = 3

class VCU_Pedal:
    """
    Encapsulates the traits of a VCU pedal : APPS1, APPS2, BSE
    """

    max_voltages: dict[VCU_Pedals, int] = {
        VCU_Pedals.APPS1: APPS1_MAX,
        VCU_Pedals.APPS2: APPS2_MAX,
        VCU_Pedals.BSE: BSE_MAX,
    }

    min_voltages : dict[VCU_Pedals, int] = {
        VCU_Pedals.APPS1: APPS1_MIN,
        VCU_Pedals.APPS2: APPS2_MIN,
        VCU_Pedals.BSE: BSE_MIN,
    }

    def __init__(self, pedal_type: VCU_Pedals):
        """
        Generate the identifier alongside the min and max values
        """
        self._pedal_type: VCU_Pedals = pedal_type
        self._min: int = self.min_voltages[pedal_type]
        self._max: int  = self.max_voltages[pedal_type]

class AnalogWave(ABC):
    """
    Abstract class to lay foundation for waveforms
    """
    _registered_waves: dict[str, object] = {}

    @classmethod
    def register(cls, identifier=None):
        """
        Decorator method for registering a subclass with a unique identifier.

        Parameters:
        - identifier (str, optional): A unique identifier for the registered subclass. If not
          provided, the subclass's name is used as the identifier.

        Returns:
        - decorator (function): The actual decorator function that registers the subclass.

        Raises:
        - KeyError: Raised if the provided identifier is already registered with another subclass
          of FormSimulator.

        Usage:
        To use this decorator, decorate a subclass of FormSimulator with the `@FormSimulatorRegistrar.register()`
        decorator, optionally providing a unique identifier. The decorated subclass will be registered,
        and the identifier can be used to invoke it from the command line.

        Example:
        ```
        @FormSimulatorRegistrar.register("custom_identifier")
        class CustomFormSimulator(FormSimulator):
            # Define Standard Mapping
            # Define Inverse  Mapping
        ```

        This will register AnalogWave with the identifier "custom_identifier", allowing it to
        be invoked from the command line when generating simulations
        ```
        1 30 SH T
        ```
        """
        def decorator(subclass):
            nonlocal identifier
            if identifier is None:
                identifier = subclass.__name__
            if identifier in cls._registered_waves:
                raise KeyError(f"Identifier {identifier} already registered with {subclass}")
            cls._registered_waves[identifier] = subclass
            return subclass
        return decorator
    
    @classmethod
    @abstractmethod
    def standard_mapping(cls, percent_pressed: float) -> float:
        pass
    
    @classmethod
    @abstractmethod
    def inverse_mapping(cls, percent_pressed: float) -> float:
        pass
    
    @classmethod
    def map_percentage_to_voltage(cls, pedal_spec: VCU_Pedal, percentage: float) -> float:
        """
        Map the percentage to the correct voltage interval given the specific pedal spec.

        :param pedal_spec: An instance of the VCU_Pedal class, which specifies the voltage interval.
        :type pedal_spec: VCU_Pedal

        :param percentage: The percentage value to be mapped to a voltage within the specified interval.
        :type percentage: int

        :return: The voltage value calculated based on the provided percentage and pedal specification.
        :rtype: float
        """
        return percentage * (pedal_spec._max - pedal_spec._min) + pedal_spec._min
    
    @classmethod
    def set_values(cls, pedal_spec: VCU_Pedal, percent_pressed: int, vcu_values: dict[VCU_Pedals, int]):
        """
        Sets the vcu values holder with the pedal spec as the key and the mapped percent pressed as the value
        
        :param pedal_spec: class identifying the specfic vcu pedal
        :param percent_pressed: the percentage pressed which is to be scaled and mapped:
        :param vcu_values: container to be populated with the specific vcu_pedal
        """
        
        scaled_percentage = cls.map_percentage_to_voltage(pedal_spec, percent_pressed)
        vcu_values[pedal_spec._pedal_type] = scaled_percentage
    

        
@AnalogWave.register("SH")
class HalfSinusodialWave(AnalogWave):
    """
    Half Sinusodial Wave used to simulate a car when turning a tight corner
    """

    @classmethod
    def standard_mapping(cls, percent_pressed: float) -> float:
        return math.sin(percent_pressed * math.pi)


    @classmethod
    def inverse_mapping(cls, percent_pressed: float) -> float:
        return -math.sin(percent_pressed * math.pi) + 1

@AnalogWave.register("SF")
class FullSinusodialWave(AnalogWave):
    """
    Full Sinusodiaul Wave, which can simulate cars going through a chicane
    """

    @classmethod
    def standard_mapping(cls, percent_pressed: float) -> float:
        return (-(math.cos(percent_pressed * 2 * math.pi)) + 1)/2


    @classmethod
    def inverse_mapping(cls, percent_pressed: float) -> float:
        return (math.cos(percent_pressed * 2 * math.pi) + 1)/2


@AnalogWave.register("T")    
class TriangularWave(AnalogWave):
    """
    Triangular Wave: linear increasing mapping
    """

    @classmethod
    def standard_mapping(cls, percent_pressed: float) -> float:
        return percent_pressed
    
    @classmethod
    def inverse_mapping(cls ,percent_pressed: float) -> float:
        return 1-percent_pressed
    
@AnalogWave.register("R")    
class DiscontinousWave(AnalogWave):
    """
    Random wave which takes a uniform number between the current percent pressed and 0
    """

    @classmethod
    def standard_mapping(cls, percent_pressed: float) -> float:
        return random.uniform(0, percent_pressed)
    
    @classmethod
    def inverse_mapping(cls, percent_pressed: float) -> float:
        return random.uniform(0, 1- percent_pressed)
    
@AnalogWave.register("M")    
class MaxWave(AnalogWave):
    """
    Maps to the maximum of pedals voltage, used for stress testing
    """

    @classmethod
    def standard_mapping(cls, percent_pressed: float) -> float:
        return 1
    
    @classmethod
    def inverse_mapping(cls, percent_pressed: float) -> float:
        return 0
    
@AnalogWave.register("O")    
class MinWave(AnalogWave):
    """
    Maps to the minimum of a pedal's voltage, used for excluding a pedal's role in the simulation
    """

    @classmethod
    def standard_mapping(cls, percent_pressed: float) -> float:
        return 0
    
    @classmethod
    def inverse_mapping(cls, percent_pressed: float) -> float:
        return 1

@AnalogWave.register("P") 
class SpikeWave(AnalogWave):
    """
    Spike wave, used to measure circuit fauls for spikes in pedal voltage readings
    """

    @classmethod
    def standard_mapping(cls, percent_pressed: float) -> float:
        return 1 if percent_pressed == 0 else 0
    
    @classmethod
    def inverse_mapping(cls, percent_pressed: float) -> float:
        return 1 if percent_pressed != 0 else 0

 #reserved to avoid accidentally overriding the inverse functionality   
@AnalogWave.register("I") 
class InverseWave(AnalogWave):
    """
    Inverse mapping of the opposite pedal pressed, reflect over the line y = (median of pedal range)
    """

    @classmethod
    def standard_mapping(cls, percent_pressed: float) -> float:
        return super().standard_mapping(percent_pressed)
    
    @classmethod
    def inverse_mapping(cls, percent_pressed: float) -> float:
        return super().inverse_mapping(percent_pressed)