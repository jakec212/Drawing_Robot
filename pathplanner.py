# pathplanner.py
import numpy as np

class Trajectory:
    def __init__(self, t, ma, mb):
        self.t, self.ma, self.mb = t, ma, mb

    @property
    def duration(self):
        return self.t[-1]

    def at(self, time):
        """Motor step positions at any time in seconds (scalar or array)."""
        return (np.interp(time, self.t, self.ma),
                np.interp(time, self.t, self.mb))

    def sampled(self, dt=0.02):
        """Positions on a fixed time grid, handy for streaming to the robot."""
        ts = np.arange(0, self.duration + dt, dt)
        return (ts, *self.at(ts))


def velocity_plan(ma, mb, t):
    """Motor velocities in steps per second for each segment of the path."""                  # seconds per segment
    dt = np.gradient(t)
    va = np.gradient(ma) / dt            # shoulder steps per second
    vb = np.gradient(mb) / dt            # elbow steps per second
    #return np.round(va).astype(int), np.round(vb).astype(int)
    return va, vb

def acceleration_plan(va, vb, t):
    """Motor accelerations in steps per second squared for each segment of the path."""
    dt = np.gradient(t)
    a_a = np.gradient(va) / dt
    a_b = np.gradient(vb) / dt
    return np.round(a_a).astype(int), np.round(a_b).astype(int)