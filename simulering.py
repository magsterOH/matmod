import matplotlib.pyplot as plt
import numpy as np


class Tree:
    def __init__(self, tree_radius_mean, tree_radius_variation) -> None:
        self.position = self.random_position(100)
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
    def area(self) -> float:
        return np.pi * self.radius**2

    def __str__(self) -> str:
        return f"Träd | position: ({np.round(self.position[0], 2)}, {np.round(self.position[1], 2)}), radie: {np.round(self.radius, 2)}"


class Forest:
    def __init__(self, number_of_trees=300, tree_radius_mean=1, tree_radius_variation=0.5) -> None:
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
    def total_area(self) -> float:
        return sum([tree.area for tree in self.trees])

    def __str__(self) -> str:
        return f"Skog | träd: {len(self.trees)}, total area: {np.round(self.total_area, 2)}"


def plot_forest(forest: Forest, angle: float):
    plt.scatter(forest.x_positions, forest.y_positions, s=forest.radii, c=forest.counted(angle))
    plt.title(f"vinkel={angle}")
    plt.show()


if __name__ == "__main__":
    # hitta optimala vinkeln som funkar för olika trädradier

    variances = np.array([])
    angles = np.arange(0.5, 5, 0.2)

    for angle in angles:
        ratios = np.array([])

        radii = np.arange(0.1, 1, 0.1)
        for tree_radius in radii:

            print(f"Vinkel: {np.round(angle, 1)}, radie: {np.round(tree_radius, 1)}, ", end=" ")

            forest = Forest(number_of_trees=10000, tree_radius_mean=tree_radius, tree_radius_variation=0)
            ratio = forest.total_area / sum(forest.counted(angle))
            # ratio /= 100 * 100

            if ratio != np.inf:
                ratios = np.append(ratios, ratio)

            print(f"densitet: {ratio}")

        print(f"relative variance: {np.var(ratios) / np.mean(ratios)}", end="\n" * 2)
        variances = np.append(variances, np.var(ratios) / np.mean(ratios))
        plt.plot(radii, ratios)
    # vinkeln vars "relative variance" är lägst, så att densiteten är så konstant som möjligt för trädradier mellan 0.1 och 0.9
    best_angle = angles[np.argmin(variances)]
    print(f"bästa vinkeln är: {np.round(best_angle, 2)}")

    # plt.plot(np.arange(0.5, 5, 0.2), variances)
    # plt.xlabel("vinkel")
    # plt.ylabel("relative variance")
    plt.show()
