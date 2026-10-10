# robot.py defines important variable associated with the robot all in one Robot class 
import numpy as np

class Robot:
    def __init__(self, arm_length=8.059, shoulder_ratio=8, elbow_ratio=-4,
                 steps_per_rev=200, microsteps=4, home=(-5.5, 14.0), starting_position=(-5.7, 0.5293)):
        self.arm_length = arm_length
        self.shoulder_ratio = shoulder_ratio
        self.elbow_ratio = elbow_ratio          # negative: motor is flipped
        self.steps_per_degree = steps_per_rev * microsteps / 360
        self.home = home
        self.starting_position = starting_position

    def angles(self, x, y):
        """XY position -> (shoulder, elbow) joint angles in degrees."""
        l = np.hypot(x, y)
        a1 = np.arccos(x / l)   
        a2 = np.arccos(l / (2 * self.arm_length))   
        return np.degrees(a1 + a2), np.degrees(np.pi - 2 * a2)  #(shoulder angle, elbow angle)

    def steps(self, x, y):
        """Path of XY points -> motor step positions relative to the first point."""
        shoulder, elbow = self.angles(np.asarray(x), np.asarray(y))
        steps_shoulder = (shoulder - shoulder[0]) * self.shoulder_ratio * self.steps_per_degree
        steps_elbow = (elbow - elbow[0]) * self.elbow_ratio * self.steps_per_degree
        #return np.round(ma).astype(int), np.round(mb).astype(int)
        return steps_shoulder, steps_elbow