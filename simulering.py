import matplotlib.pyplot as plt
import numpy as np

TREE_RADIUS_MEAN = 1
TREE_RADIUS_VARIATION = 0.5


class Tree:
    def __init__(self) -> None:
        self.position = self.random_position(100)
        self.radius = self.random_radius(mean=TREE_RADIUS_MEAN, variation=TREE_RADIUS_VARIATION)

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

    def __str__(self) -> str:
        return f"Träd | position: ({np.round(self.position[0], 2)}, {np.round(self.position[1], 2)}), radie: {np.round(self.radius, 2)}"


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
        """angle: vinkel i grader"""
        return np.array([tree.inside_angle(angle) for tree in self.trees])

    @property
    def total_area(self) -> float:
        return sum([tree.area for tree in self.trees])

    def __str__(self) -> str:
        return f"Skog | träd: {len(self.trees)}, total area: {np.round(self.total_area, 2)}"


def plot_forest(forest: Forest, angle: float):
    plt.scatter(forest.x_positions, forest.y_positions, s=forest.radii, c=forest.counted(angle))
    plt.title(f"vinkel={angle}")
    plt.show()


if __name__ == "__main__":
    angle = 5
    forest = Forest(number_of_trees=500)

    # testa olika vinklar
    for angle in range(1, 10):
        print(f"Vinkel: {angle}, ", end="")
        print(f"Räknade träd: {sum(forest.counted(angle))}, ", end="")
        print(f"Total area: {forest.total_area}, ", end="")
        print(f"area/träd: {forest.total_area/sum(forest.counted(angle))}")

    angle = 5

    # testa olika antal träd
    for trees in range(100, 2000, 100):
        forest = Forest(number_of_trees=trees)
        print(f"antal träd: {len(forest.trees)}, ", end="")
        print(f"area/träd: {forest.total_area/sum(forest.counted(angle))}")

    # plot_forest(forest, angle)
