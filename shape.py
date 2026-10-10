# shape.py
import numpy as np

class Shape:
    def __init__(self, x, y, num_points):
        self.x = x
        self.y = y
        self.num_points = num_points

    def points(self):
        raise NotImplementedError("each shape defines its own points()\n" \
        "points function should be in the shape class")

    def path(self, start_x, start_y):
        """Shape points with the pen's start/end position added on each end."""
        xs, ys = self.points()
        return (xs, ys)
        #return (np.concatenate(([start_x], xs, [start_x])),
                #np.concatenate(([start_y], ys, [start_y])))


class Circle(Shape):
    def __init__(self, x, y, radius, num_points):
        super().__init__(x, y, num_points)   # let Shape store x, y, num_points
        self.radius = radius

    def points(self):
        theta = np.linspace(0, 2*np.pi, self.num_points)
        return (self.x + self.radius * np.cos(theta),
                self.y + self.radius * np.sin(theta))


class Rectangle(Shape):
    def __init__(self, x, y, width, height, num_points):
        super().__init__(x, y, num_points)
        self.width = width
        self.height = height

    def points(self):
        hw, hh = self.width / 2, self.height / 2
        cx = self.x + np.array([-hw,  hw, hw, -hw, -hw])   # corners, back to start
        cy = self.y + np.array([-hh, -hh, hh,  hh, -hh])
        n = self.num_points // 4                            # points per side
        xs = np.concatenate([np.linspace(cx[i], cx[i+1], n, endpoint=False) for i in range(4)])
        ys = np.concatenate([np.linspace(cy[i], cy[i+1], n, endpoint=False) for i in range(4)])
        return np.append(xs, cx[0]), np.append(ys, cy[0])