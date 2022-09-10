
from typing import Dict, List

import numpy as np
from scipy.linalg import solve
import pandas as pd
import openturns as ot

from okami.src.domain.entities.room import Room
from okami.src.domain.entities.sensor import Sensor
from okami.src.domain.entities.source import Source
from okami.src.domain.entities.variogram import Variogram


class Operator:


    latest_variogram: Variogram = None


    def __init__(self) -> None:
        pass


    def _get_connection(self):
        return TimeseriesRepo()

        
    def read_values(self, sensors: List[Sensor]) -> List[Sensor]:
        connection = self._get_connection()

        for sensor in sensors:
            sensor.read_value(connection = connection)

        return sensors


    def get_variogram(self, sensors: List[Sensor]) -> Variogram:
        variances  = self.get_variances(sensors = sensors)
        parameters = self._fit_espherical_variogram(variances)

        if parameters["sill"] > parameters["nugget"]:
            variogram = Variogram(nugget = parameters["nugget"], sill = parameters["sill"],
                                  e_range = parameters["e_range"])
            self.latest_variogram = variogram
            return variogram
        
        else:
            return self.latest_variogram


    @staticmethod
    def get_variances(sensors: List[Sensor]) -> np.ndarray:
        rows      = int(np.math.factorial(len(sensors))/(np.math.factorial(2)*np.math.factorial(len(sensors) - 2)))
        variances = np.zeros(shape = (rows, 2))

        temp  = sensors.copy()
        index = 0

        for sensor in sensors:
            aux = temp.copy()
            aux.remove(sensor)

            for pair_sensor in aux:
                mean_variance = (pow(sensor.cache - pair_sensor.cache, 2)/2).mean()
                distance = pow(pow(sensor.x - pair_sensor.x, 2) + pow(sensor.y - pair_sensor.y, 2) + pow(sensor.z - pair_sensor.z, 2), 0.5)

                variances[index, 0] = distance
                variances[index, 1] = round(mean_variance)
                index += 1
                
            temp.remove(sensor)
        
        return variances


    @staticmethod
    def _fit_espherical_variogram(variances: np.ndarray) -> dict:
        x = variances[:, 0]
        y = variances[:, 1]

        z = np.polyfit(x, y, 2)
        estimator = np.poly1d(z)

        parameters = dict()
        parameters["nugget"]  = estimator(x[0])
        parameters["sill"]    = estimator(x[-1])
        parameters["e_range"] = x[-1]

        return parameters


    @staticmethod
    def _compute_sensor_vision(sensor: Sensor, room: Room) -> pd.DataFrame:
        xs = room.grid[0]
        ys = room.grid[1]

        df = pd.DataFrame(columns = np.unique(xs), index = np.unique(ys))
        
        for x, y in zip(xs, ys):
            dx = sensor.x - x
            dy = sensor.y - y
            
            distance = pow(dx*dx + dy*dy, 0.5)

            if distance > 1.2:
                value = np.nan

            else:
                value = sensor.value/pow(np.e, -pow(distance, 2)/0.5)

            # if distance > variogram.e_range:
            #     value = np.nan

            # else:
            #     variance = variogram.variance(distance = distance)
            #     value    = pow(2*variance, 0.5) + sensor.value

            df[x].loc[y] = value
        
        return df


    def locate_sources(self, sensors: List[Sensor], room: Room) -> List[Source]:
        visions = []
        sources = []

        for sensor in sensors:
            visions.append(self._compute_sensor_vision(sensor = sensor, room = room))

        temp = visions.copy()

        for vision in visions:
            aux = temp.copy()
            aux.remove(vision)

            for pair_vision in aux:
                mutual = (vision - pair_vision)
                mutual = mutual.applymap(lambda x: 1 if abs(x) < 100 else np.nan)
                mutual = mutual.dropna(how = "all")

                for column in mutual.columns:
                    for index in mutual.index:
                        if mutual[column].loc[index] == 1:
                            value = (vision[column].loc[index] + pair_vision[column].loc[index])/2
                            print(f"Source value {value} @ x = {column} y = {index}")
                            sources.append(Source(x = column, y = index, value = value))
            
            temp.remove(vision)
        
        return sources


    @staticmethod
    def _get_mutual_variance_matrix(positions: np.ndarray, variogram: Variogram) -> np.ndarray:
        # matrix = np.zeros(shape = (positions.shape[0] + 1, positions.shape[0] + 1))
        matrix = np.zeros(shape = (positions.shape[0], positions.shape[0]))

        for i in range(positions.shape[0]):
            for j in range(positions.shape[0]):
                if i == j:
                    matrix[i, j] = 0
                
                else:
                    dx = positions[i, 0] - positions[j, 0]
                    dy = positions[i, 1] - positions[j, 1]
                    dz = positions[i, 2] - positions[j, 2]
                    
                    distance     = pow(dx*dx + dy*dy + dz*dz, 0.5)
                    matrix[i, j] = variogram.variance(distance = distance) - variogram.sill
        
        # matrix[:, -1]  = np.array([1]*(positions.shape[0] + 1)) 
        # matrix[-1, :]  = np.array([1]*(positions.shape[0] + 1))
        # matrix[-1, -1] = 0

        return matrix


    @staticmethod
    def _get_variances_matrix(variogram: Variogram, positions: np.ndarray, x: float, y: float) -> np.ndarray:
        # result = np.zeros(shape = (positions.shape[0] + 1, 1))
        result = np.zeros(shape = (positions.shape[0], 1))

        for i, position in enumerate(positions):
            dx = position[0] - x
            dy = position[1] - y
            dz = position[2] - 0

            distance     = pow(dx*dx + dy*dy + dz*dz, 0.5)
            result[i, 0] = variogram.variance(distance = distance)

        # result[-1, 0] = 1
        return result


    # def krigit(self, sensors: List[Sensor], room: Room, variogram: Variogram, sources: List[Source] = []) -> pd.DataFrame:
    #     known_values  = [sensor.value for sensor in sensors]
    #     known_values += [source.value for source in sources]
    #     known_values  = np.array(known_values)
        
    #     positions  = [[sensor.x, sensor.y, sensor.z] for sensor in sensors]
    #     positions += [[source.x, source.y, source.z] for source in sources]
    #     positions  = np.array(positions)

    #     mutual_variances = self._get_mutual_variance_matrix(positions = positions, variogram = variogram)
    #     # print(mutual_variances)
    #     xs = room.grid[0]
    #     ys = room.grid[1]

    #     df = pd.DataFrame(columns = np.unique(xs), index = np.unique(ys))

    #     for x, y in zip(xs, ys):
    #         matrix_variances = self._get_variances_matrix(variogram = variogram, positions = positions, x = x, y = y)
    #         # print(matrix_variances)
    #         weights          = np.matmul(np.linalg.inv(mutual_variances), matrix_variances)#[:-1]

    #         value = [weight*value for weight, value in zip(weights, known_values)]

    #         df[x].loc[y] = sum(value)[0]

    #     return df


    def krigit(self, sensors: List[Sensor], room: Room, variogram: Variogram, sources: List[Source] = []) -> pd.DataFrame:
        known_values  = [sensor.value for sensor in sensors]
        known_values += [source.value for source in sources]
        known_values  = np.array(known_values)
        
        positions  = [[sensor.x, sensor.y, sensor.z] for sensor in sensors]
        positions += [[source.x, source.y, source.z] for source in sources]
        positions  = np.array(positions)
        
        input_train  = ot.Sample(positions[:, :2])
        output_train = ot.Sample(known_values.reshape(-1, 1))

        inputDimension = 2
        basis = ot.ConstantBasisFactory(inputDimension).build()
        covariance_kernel = ot.SquaredExponential([0.5]*inputDimension, [0.5])
        algo = ot.KrigingAlgorithm(input_train, output_train, covariance_kernel, basis)
        algo.run()
        result = algo.getResult()
        krigingMetamodel = result.getMetaModel()

        xs = room.grid[0]
        ys = room.grid[1]
        
        df = pd.DataFrame(columns = np.unique(xs), index = np.unique(ys))

        for x, y in zip(xs, ys):
            df[x].loc[y] = krigingMetamodel([x, y])[0]

        return df


    def simple_interpolation(self, sensors: List[Sensor], room: Room, sources: List[Source] = []) -> pd.DataFrame:
        xs = room.grid[0]
        ys = room.grid[1]

        df = pd.DataFrame(columns = np.unique(xs), index = np.unique(ys))

        know_points = sensors + sources

        for x, y in zip(xs, ys):
            distances = []
            values    = []

            for know_point in know_points:
                dx = know_point.x - x
                dy = know_point.y - y
                dz = know_point.z - 1.5

                distance = pow(dx*dx + dy*dy + dz*dz, 0.5)
                distances.append(pow(distance, 2))
                values.append(know_point.value)

            if 0 in distances:
                index = distances.index(0)

                df[x].loc[y] = values[index]

            else:
                distances = np.array(distances)
                temp      = 1/distances
                weights   = temp/temp.sum()

                df[x].loc[y] = sum(weights*np.array(values))

        return df