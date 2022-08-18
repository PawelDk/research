import random

class MobileRobot:
    MAP_BORDERS = {"x_min": 0,
                   "x_max": 100,
                   "y_min": 0,
                   "y_max": 100}
    DISTANCE_LIMIT = 10

    def __init__(self, position_x,  position_y, sensor_noise_threshold):
        self.position = {"pos_x": position_x, "pos_y": position_y}
        self.sensor_noise_threshold = sensor_noise_threshold
        self.movements_record = []

    def move(self, vector_x, vector_y):
        if abs(vector_x) > self.DISTANCE_LIMIT or abs(vector_y) > self.DISTANCE_LIMIT:
            raise ValueError
        else:
            new_x = self.position["pos_x"] + vector_x
            new_y = self.position["pos_y"] + vector_y
            if new_x < self.MAP_BORDERS["x_min"] or new_x > self.MAP_BORDERS["x_max"] or \
               new_y < self.MAP_BORDERS["y_min"] or new_y > self.MAP_BORDERS["y_max"]:
                raise ValueError
            else:
                self.position["pos_x"] = new_x
                self.position["pos_y"] = new_y
                self.movements_record.append((vector_x, vector_y))

    def read_SLAM_record(self):
        return self.movements_record

    def SLAM_calculate_position_change(self):
        change = {"x": 0, "y": 0}
        for movement in self.movements_record:
            change["x"] = change["x"] + movement[0]
            change["y"] = change["y"] + movement[1]
        return change

    def read_position_sensor(self):
        return (self.position["pos_x"] + self.simulate_sensor_noise(self.sensor_noise_threshold),
                self.position["pos_y"] + self.simulate_sensor_noise(self.sensor_noise_threshold))

    @staticmethod
    def simulate_sensor_noise(sensor_noise_threshold):
        return random.uniform(-sensor_noise_threshold, sensor_noise_threshold)
