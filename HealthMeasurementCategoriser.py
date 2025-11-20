from typing import List, Dict, Any, Union
from dataclasses import dataclass
from new_dataclasses import *

class HealthMeasurementCategoriser:
    @staticmethod
    def process_measurements(measurements: List[HealthMeasurement]) -> List[HealthMeasurementValuePair]:
        replacements = []

        for measurement in measurements:
            if isinstance(measurement, HeartRateMeasurement):
                HealthMeasurementCategoriser._process_heartrate(measurement, replacements)
            elif isinstance(measurement, InflammatoryMeasurement):
                HealthMeasurementCategoriser._process_inflammatories(measurement, replacements)
            elif isinstance(measurement, BreathingRateMeasurement):
                HealthMeasurementCategoriser._process_breathing_rate(measurement, replacements)
            elif isinstance(measurement, MuscleTensionMeasurement):
                HealthMeasurementCategoriser._process_muscle_tension(measurement, replacements)
            elif isinstance(measurement, ChokingMeasurement):
                HealthMeasurementCategoriser._process_choking(measurement, replacements)
            elif isinstance(measurement, AsthmaAttackMeasurement):
                HealthMeasurementCategoriser._process_asthma_attack(measurement, replacements)
            elif isinstance(measurement, GroundHardnessMeasurement):
                HealthMeasurementCategoriser._process_ground_hardness(measurement, replacements)
            elif isinstance(measurement, EKGReadingMeasurement):
                HealthMeasurementCategoriser._process_ekg_reading(measurement, replacements)
            elif isinstance(measurement, AirflowMeasurement):
                HealthMeasurementCategoriser._process_airflow(measurement, replacements)
            elif isinstance(measurement, HyperventilationMeasurement):
                HealthMeasurementCategoriser._process_hyperventilation(measurement, replacements)

        return replacements

    @staticmethod
    def _process_heartrate(measurement: HealthMeasurement, replacements: List[HealthMeasurementValuePair]) -> None:
        if measurement.value < 40:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_LOW))
        elif 40 <= measurement.value <= 60:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.LOW))
        elif 61 <= measurement.value <= 100:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.MEDIUM))
        elif 101 <= measurement.value <= 140:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.HIGH))
        elif measurement.value > 140:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_inflammatories(measurement: HealthMeasurement, replacements: List[HealthMeasurementValuePair]) -> None:
        if measurement.value < 1:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_LOW))
        elif 1 <= measurement.value <= 3:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.LOW))
        elif 4 <= measurement.value <= 10:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.MEDIUM))
        elif 11 <= measurement.value <= 20:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.HIGH))
        elif measurement.value > 20:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_breathing_rate(measurement: HealthMeasurement, replacements: List[HealthMeasurementValuePair]) -> None:
        if measurement.value < 8:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_LOW))
        elif 8 <= measurement.value <= 12:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.LOW))
        elif 13 <= measurement.value <= 20:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.MEDIUM))
        elif 21 <= measurement.value <= 30:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.HIGH))
        elif measurement.value > 30:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_muscle_tension(measurement: HealthMeasurement, replacements: List[HealthMeasurementValuePair]) -> None:
        if 1 <= measurement.value <= 2:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_LOW))
        elif 3 <= measurement.value <= 4:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.LOW))
        elif 5 <= measurement.value <= 6:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.MEDIUM))
        elif 7 <= measurement.value <= 8:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.HIGH))
        elif 9 <= measurement.value <= 10:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_choking(measurement: HealthMeasurement, replacements: List[HealthMeasurementValuePair]) -> None:
        if 1 <= measurement.value <= 2:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_LOW))
        elif 3 <= measurement.value <= 4:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.LOW))
        elif 5 <= measurement.value <= 6:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.MEDIUM))
        elif 7 <= measurement.value <= 8:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.HIGH))
        elif 9 <= measurement.value <= 10:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_asthma_attack(measurement: HealthMeasurement, replacements: List[HealthMeasurementValuePair]) -> None:
        if 1 <= measurement.value <= 2:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_LOW))
        elif 3 <= measurement.value <= 4:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.LOW))
        elif 5 <= measurement.value <= 6:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.MEDIUM))
        elif 7 <= measurement.value <= 8:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.HIGH))
        elif 9 <= measurement.value <= 10:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_ground_hardness(measurement: HealthMeasurement, replacements: List[HealthMeasurementValuePair]) -> None:
        if 1 <= measurement.value <= 2:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_LOW))
        elif 3 <= measurement.value <= 4:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.LOW))
        elif 5 <= measurement.value <= 6:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.MEDIUM))
        elif 7 <= measurement.value <= 8:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.HIGH))
        elif 9 <= measurement.value <= 10:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_ekg_reading(measurement: HealthMeasurement, replacements: List[HealthMeasurementValuePair]) -> None:
        if measurement.value == 0:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_LOW))
        elif measurement.value == 1:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.LOW))
        elif measurement.value == 2:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.MEDIUM))
        elif measurement.value == 3:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.HIGH))
        elif measurement.value == 4:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_airflow(measurement: HealthMeasurement, replacements: List[HealthMeasurementValuePair]) -> None:
        if measurement.value < 100:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_LOW))
        elif 100 <= measurement.value <= 200:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.LOW))
        elif 201 <= measurement.value <= 300:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.MEDIUM))
        elif 301 <= measurement.value <= 400:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.HIGH))
        elif measurement.value > 400:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_HIGH))

    @staticmethod
    def _process_hyperventilation(measurement: HealthMeasurement, replacements: List[HealthMeasurementValuePair]) -> None:
        if 1 <= measurement.value <= 2:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_LOW))
        elif 3 <= measurement.value <= 4:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.LOW))
        elif 5 <= measurement.value <= 6:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.MEDIUM))
        elif 7 <= measurement.value <= 8:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.HIGH))
        elif 9 <= measurement.value <= 10:
            replacements.append(HealthMeasurementValuePair(measurement_type=measurement.measurement_type, category=MeasurementCategory.VERY_HIGH))