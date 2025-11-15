from typing import List, Dict, Any, Union
from dataclasses import dataclass
from new_dataclasses import *

class HealthMeasurementCategoriser:
    @staticmethod
    def process_measurements(measurements: List[HealthMeasurement]) -> List[HealthMeasurementValuePair]:
        replacements = []

        for measurement in measurements:
            measurement_name = measurement.name
            measurement_value = measurement.value

            if measurement_name == Heartrate(value=0).name:
                HealthMeasurementCategoriser._process_heartrate(measurement_value, replacements)
            elif measurement_name == Inflammatories(value=0).name:
                HealthMeasurementCategoriser._process_inflammatories(measurement_value, replacements)
            elif measurement_name == BreathingRate(value=0).name:
                HealthMeasurementCategoriser._process_breathing_rate(measurement_value, replacements)
            elif measurement_name == MuscleTension(value=0).name:
                HealthMeasurementCategoriser._process_muscle_tension(measurement_value, replacements)
            elif measurement_name == Choking(value=0).name:
                HealthMeasurementCategoriser._process_choking(measurement_value, replacements)
            elif measurement_name == AsthmaAttack(value=0).name:
                HealthMeasurementCategoriser._process_asthma_attack(measurement_value, replacements)
            elif measurement_name == GroundHardness(value=0).name:
                HealthMeasurementCategoriser._process_ground_hardness(measurement_value, replacements)
            elif measurement_name == EKGReading(value=0).name:
                HealthMeasurementCategoriser._process_ekg_reading(measurement_value, replacements)
            elif measurement_name == Airflow(value=0).name:
                HealthMeasurementCategoriser._process_airflow(measurement_value, replacements)
            elif measurement_name == Hyperventilation(value=0).name:
                HealthMeasurementCategoriser._process_hyperventilation(measurement_value, replacements)

        return replacements

    @staticmethod
    def _process_heartrate(value: Union[int, float], replacements: List[HealthMeasurementValuePair]) -> None:
        if value < 40:
            replacements.append(HealthMeasurementValuePair(IllnessType.CARDIAC, MeasurementCategory.VERY_LOW))
        elif 40 <= value <= 60:
            replacements.append(HealthMeasurementValuePair(IllnessType.CARDIAC, MeasurementCategory.LOW))
        elif 61 <= value <= 100:
            replacements.append(HealthMeasurementValuePair(IllnessType.CARDIAC, MeasurementCategory.MEDIUM))
        elif 101 <= value <= 140:
            replacements.append(HealthMeasurementValuePair(IllnessType.CARDIAC, MeasurementCategory.HIGH))
        elif value > 140:
            replacements.append(HealthMeasurementValuePair(IllnessType.CARDIAC, MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_inflammatories(value: Union[int, float], replacements: List[HealthMeasurementValuePair]) -> None:
        if value < 1:
            replacements.append(HealthMeasurementValuePair(IllnessType.INFLAMMATORY, MeasurementCategory.VERY_LOW))
        elif 1 <= value <= 3:
            replacements.append(HealthMeasurementValuePair(IllnessType.INFLAMMATORY, MeasurementCategory.LOW))
        elif 4 <= value <= 10:
            replacements.append(HealthMeasurementValuePair(IllnessType.INFLAMMATORY, MeasurementCategory.MEDIUM))
        elif 11 <= value <= 20:
            replacements.append(HealthMeasurementValuePair(IllnessType.INFLAMMATORY, MeasurementCategory.HIGH))
        elif value > 20:
            replacements.append(HealthMeasurementValuePair(IllnessType.INFLAMMATORY, MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_breathing_rate(value: Union[int, float], replacements: List[HealthMeasurementValuePair]) -> None:
        if value < 8:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.VERY_LOW))
        elif 8 <= value <= 12:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.LOW))
        elif 13 <= value <= 20:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.MEDIUM))
        elif 21 <= value <= 30:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.HIGH))
        elif value > 30:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_muscle_tension(value: Union[int, float], replacements: List[HealthMeasurementValuePair]) -> None:
        if 1 <= value <= 2:
            replacements.append(HealthMeasurementValuePair(IllnessType.MUSCULAR, MeasurementCategory.VERY_LOW))
        elif 3 <= value <= 4:
            replacements.append(HealthMeasurementValuePair(IllnessType.MUSCULAR, MeasurementCategory.LOW))
        elif 5 <= value <= 6:
            replacements.append(HealthMeasurementValuePair(IllnessType.MUSCULAR, MeasurementCategory.MEDIUM))
        elif 7 <= value <= 8:
            replacements.append(HealthMeasurementValuePair(IllnessType.MUSCULAR, MeasurementCategory.HIGH))
        elif 9 <= value <= 10:
            replacements.append(HealthMeasurementValuePair(IllnessType.MUSCULAR, MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_choking(value: Union[int, float], replacements: List[HealthMeasurementValuePair]) -> None:
        if 1 <= value <= 2:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.VERY_LOW))
        elif 3 <= value <= 4:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.LOW))
        elif 5 <= value <= 6:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.MEDIUM))
        elif 7 <= value <= 8:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.HIGH))
        elif 9 <= value <= 10:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_asthma_attack(value: Union[int, float], replacements: List[HealthMeasurementValuePair]) -> None:
        if 1 <= value <= 2:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.VERY_LOW))
        elif 3 <= value <= 4:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.LOW))
        elif 5 <= value <= 6:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.MEDIUM))
        elif 7 <= value <= 8:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.HIGH))
        elif 9 <= value <= 10:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_ground_hardness(value: Union[int, float], replacements: List[HealthMeasurementValuePair]) -> None:
        if 1 <= value <= 2:
            replacements.append(HealthMeasurementValuePair(IllnessType.MUSCULAR, MeasurementCategory.VERY_LOW))
        elif 3 <= value <= 4:
            replacements.append(HealthMeasurementValuePair(IllnessType.MUSCULAR, MeasurementCategory.LOW))
        elif 5 <= value <= 6:
            replacements.append(HealthMeasurementValuePair(IllnessType.MUSCULAR, MeasurementCategory.MEDIUM))
        elif 7 <= value <= 8:
            replacements.append(HealthMeasurementValuePair(IllnessType.MUSCULAR, MeasurementCategory.HIGH))
        elif 9 <= value <= 10:
            replacements.append(HealthMeasurementValuePair(IllnessType.MUSCULAR, MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_ekg_reading(value: Union[int, float], replacements: List[HealthMeasurementValuePair]) -> None:
        if value == 0:
            replacements.append(HealthMeasurementValuePair(IllnessType.CARDIAC, MeasurementCategory.VERY_LOW))
        elif value == 1:
            replacements.append(HealthMeasurementValuePair(IllnessType.CARDIAC, MeasurementCategory.LOW))
        elif value == 2:
            replacements.append(HealthMeasurementValuePair(IllnessType.CARDIAC, MeasurementCategory.MEDIUM))
        elif value == 3:
            replacements.append(HealthMeasurementValuePair(IllnessType.CARDIAC, MeasurementCategory.HIGH))
        elif value == 4:
            replacements.append(HealthMeasurementValuePair(IllnessType.CARDIAC, MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_airflow(value: Union[int, float], replacements: List[HealthMeasurementValuePair]) -> None:
        if value < 100:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.VERY_LOW))
        elif 100 <= value <= 200:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.LOW))
        elif 201 <= value <= 300:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.MEDIUM))
        elif 301 <= value <= 400:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.HIGH))
        elif value > 400:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_hyperventilation(value: Union[int, float], replacements: List[HealthMeasurementValuePair]) -> None:
        if 1 <= value <= 2:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.VERY_LOW))
        elif 3 <= value <= 4:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.LOW))
        elif 5 <= value <= 6:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.MEDIUM))
        elif 7 <= value <= 8:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.HIGH))
        elif 9 <= value <= 10:
            replacements.append(HealthMeasurementValuePair(IllnessType.RESPIRATORY, MeasurementCategory.VERY_HIGH))