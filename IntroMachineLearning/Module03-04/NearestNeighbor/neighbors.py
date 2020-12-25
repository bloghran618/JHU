from collections import Counter
import math

from write_to_output import write_output


# class to track nearest neighbors
class Neighbors:
    def __init__(self, k, columns, outputfile):
        self.k = k
        self.nearest = []
        self.dimensions = columns
        self.outputfile = outputfile

    def output_neighbors(self, outputfile):
        """
        output the state of the neighbors class

        :param outputfile: the file to write to
        """
        write_output(outputfile, f'The nearest {self.k} neighbors are: ')
        for near in self.nearest:
            write_output(outputfile, near)

    def get_nearest(self, training_set, test_point):
        """
        get the nearest k points to the test point in the training set

        :param training_set: the training set
        :param test_point: the point to find the nearest points to
        """

        best_distances = {}

        for row in training_set.itertuples():
            # add point to nearest if nearest has less than k points
            if not self.nearest:
                self.nearest.append(row)
                best_distances[row[0]] = self.distance(test_point, row)
            elif len(self.nearest) < self.k:
                self.nearest.append(row)
                best_distances[row[0]] = self.distance(test_point, row)
            # else check if the new point is in nearest
            else:
                distance = self.distance(test_point, row)
                # get the index of the maximum distance of the k neighbors
                max_best_index = max(best_distances, key=best_distances.get)
                # if the point is one of the nearest
                if distance < best_distances[max_best_index]:
                    # remove the furthest best distance from the best_distance dict
                    del best_distances[max_best_index]
                    # add the new best distance to the best_distance dict
                    best_distances[row[0]] = distance
                    # remove the furthest best distance from nearest
                    for near in self.nearest:
                        if near[0] == max_best_index:
                            self.nearest.remove(near)
                    # add the new best distance to nearest
                    self.nearest.append(row)

        write_output(self.outputfile, f'nearest rows: {best_distances}')
        # print(self.nearest)

        # reorder nearest by closest
        ordered_nearest = []
        for i in range(len(self.nearest)):
            # get the nearest remaining index
            min_best_index = min(best_distances, key=best_distances.get)
            # append the nearest to ordered_nearest
            for near in self.nearest:
                if near[0] == min_best_index:
                    ordered_nearest.append(near)
                # pop the old nearest from the best distances dictionary
                best_distances.pop(min_best_index, None)
        self.nearest = ordered_nearest

    def distance(self, point_a, point_b):
        """
        Calculate the distance between two points

        :param point_a: the first point
        :param point_b: the second point

        :return: the distance between the two points
        """
        distance = 0

        for index, dim in enumerate(self.dimensions[:-1]):
            distance += (point_a[index+1] - point_b[index+1]) ** 2
        distance = distance ** (1/2)
        # write_output(self.outputfile, f'the distance between {point_a} and {point_b} is {distance}')
        return distance

    def purality_vote(self):
        """
        return the classification in the event of a plurality vote

        :return: the classification
        """
        result_col = len(self.dimensions)

        classifications = []
        for near in self.nearest:
            classifications.append(near[result_col])
        write_output(self.outputfile, f'the {self.k} nearest are: {classifications}')
        class_tally = Counter(classifications)
        classification = max(class_tally, key=class_tally.get)
        return classification

    def gaussian_kernel(self, point, sigma):
        """
        Return the guess for the regression

        :param point: the point to consider
        :param sigma: the sigma value for the gaussian function

        :return: the guess for the regression
        """

        # initialize weights and values to 0 and result column to last column
        total_weight = 0
        weighted_value = 0
        result_col = len(self.dimensions)

        for near in self.nearest:
            distance = self.distance(point, near)
            # compute the kernel function
            weight = math.exp(-1 * (distance ** 2) / (2 * (sigma ** 2)))

            # sum the weights
            weighted_value += weight * near[result_col]
            total_weight += weight

        try:
            regression_guess = weighted_value / total_weight
        # if the total weight is zero just use average
        except ZeroDivisionError:
            classification_sum = 0
            for near in self.nearest:
                classification_sum += near[result_col]
            regression_guess = classification_sum / len(self.nearest)

        return regression_guess
