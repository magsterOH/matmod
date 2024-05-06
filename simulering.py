import matplotlib.pyplot as plt
import numpy as np


class Tree:
    def __init__(self, tree_radius_mean, tree_radius_variation) -> None:
        self.position = self.random_position(300)
        self.radius = self.random_radius(mean=tree_radius_mean, variation=tree_radius_variation)

    def random_position(self, size: int) -> np.ndarray:
        return np.random.uniform(-size / 2, size / 2, 2)

    def random_radius(self, mean: float, variation: float) -> float:
        return max(np.random.normal(mean, variation), 0)

    @property
    def distance(self) -> float:
        return np.sqrt(self.position[0] ** 2 + self.position[1] ** 2)

    def inside_angle(self, angle: float) -> bool:
        """angle: vinkel i grader"""
        return self.radius > self.distance * np.tan(np.deg2rad(angle) / 2)

    @property
    def inside_hectare(self) -> bool:
        return -50 < self.position[0] < 50 and -50 < self.position[1] < 50

    @property
    def area(self) -> float:
        return np.pi * self.radius**2


class Forest:
    def __init__(self, number_of_trees=1000, tree_radius_mean=1, tree_radius_variation=0.5) -> None:
        self.trees = [Tree(tree_radius_mean, tree_radius_variation) for _ in range(number_of_trees)]

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
    def area_in_hectare(self) -> float:
        """returnerar totala arean inom 100x100 område runt (0,0)"""
        return sum([tree.area for tree in self.trees if tree.inside_hectare])


def plot_forest(forest: Forest, angle: float, title: str):
    plt.plot([50, -50, -50, 50, 50], [50, 50, -50, -50, 50], color="grey", linewidth=1)
    plt.scatter(forest.x_positions, forest.y_positions, s=forest.radii, c=forest.counted(angle))
    plt.axis("equal")
    plt.title(title)
    plt.show()


if __name__ == "__main__":

    # undersöker skillnaden från väntevärde för några olika vinklar och trädradier

    radii = np.arange(0.1, 0.51, 0.05)
    angles = np.arange(0.8, 2.1, 0.2)

    differences_by_angle = {}

    for angle in angles:
        differences = np.array([])
        for tree_radius_mean in radii:
            forest = Forest(number_of_trees=1000, tree_radius_mean=tree_radius_mean, tree_radius_variation=0)

            expected_value = forest.area_in_hectare
            counted_trees = sum(forest.counted(angle))
            difference = np.abs(expected_value - counted_trees)

            differences = np.append(differences, difference)

            print(f"radie: {round(tree_radius_mean, 2)}, vinkel: {round(angle, 1)}")
            print(f"expected value: {round(expected_value, 2)} m^2")
            print(f"räknade träd: {counted_trees}")
            print(f"skillnad: {round(difference, 2)}", end="\n" * 2)

        differences_by_angle[angle] = differences
        plt.plot(radii, differences, label=f"{round(angle, 1)}°")

    plt.ylabel("Skillnad från väntevärde")
    plt.xlabel("Trädradier [m]")
    plt.title("Skillnad från väntevärde för olika vinklar över trädradier")
    plt.legend()
    plt.show()

    # plotta vinkeln 1.2 grader

    plt.plot(radii, differences_by_angle[1.2])
    plt.ylim(0, max(differences_by_angle[1.2]))
    plt.ylabel("Skillnad från väntevärde")
    plt.xlabel("Trädradier [m]")
    plt.title("Skillnad från väntevärde över trädradier för vinkel 1.2°")
    plt.show()

    # exempelskog

    forest = Forest(number_of_trees=1000, tree_radius_mean=1, tree_radius_variation=0)
    plot_forest(forest, angle=1.2, title="1000 träd med radie 1m, relaskopets vinkel 1.2°")
