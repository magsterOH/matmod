import matplotlib.pyplot as plt
import numpy as np


class Tree:
    def __init__(self) -> None:
        self.position = self.random_position(100)
        self.radius = self.random_radius(mean=1, variation=0.5)

    def random_position(self, size: int) -> np.ndarray:
        return np.random.uniform(-size / 2, size / 2, 2)

    def random_radius(self, mean: float, variation: float) -> float:
        return max(np.random.normal(mean, variation), 0)

    @property
    def distance(self) -> float:
        return np.sqrt(self.position[0] ** 2 + self.position[1] ** 2)

    def inside_angle(self, angle: float) -> bool:
        return self.radius > self.distance * np.tan(np.deg2rad(angle) / 2)

    @property
    def area(self) -> float:
        return np.pi * self.radius**2


class Forest:
    def __init__(self, number_of_trees=300) -> None:
        self.trees = [Tree() for _ in range(number_of_trees)]

    @property
    def x_positions(self) -> np.ndarray:
        return np.array([tree.position[0] for tree in self.trees])

    @property
    def y_positions(self) -> np.ndarray:
        return np.array([tree.position[1] for tree in self.trees])

    @property
    def radii(self) -> np.ndarray:
        return np.array([tree.radius for tree in self.trees]) * 10

    def counted(self, angle) -> np.ndarray:
        return np.array([tree.inside_angle(angle) for tree in self.trees])

    @property
    def total_area(self) -> float:
        return sum([tree.area for tree in self.trees])


def plot_forest(forest: Forest):
    plt.scatter(forest.x_positions, forest.y_positions, s=forest.radii, c=forest.counted(angle))
    plt.show()


angle = 5
forest = Forest(number_of_trees=500)

for angle in range(1, 10):
    print(f"Vinkel: {angle}, ", end="")
    print(f"Räknade träd: {sum(forest.counted(angle))}, ", end="")
    print(f"Total area: {forest.total_area}, ", end="")
    print(f"area/träd: {forest.total_area/sum(forest.counted(angle))}")


plot_forest(forest)
