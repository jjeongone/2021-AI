import os
import math
from utils import converged, plot_2d_soft, plot_centroids, read_data, \
    load_centroids, write_centroids_tofile
import matplotlib.pyplot as plt
import numpy as np
import copy

from kmeans import euclidean_distance

# problem for students
def get_responsibility(data_point, centroids, beta):
    """Calculate the responsibiliy of each cluster for a single data point.
    You should use the euclidean_distance function (that you previously implemented).
    You can use the math.exp() function to calculate the responsibility.

    Arguments:
        data_point: a list of floats representing a data point
        centroids: a dictionary representing the centroids where the keys are
                   strings (centroid names) and the values are lists of
                   centroid locations
        beta: hyper-parameter

    Returns: a dictionary whose keys are the the centroids' key names and
             value is a float as the responsibility of the cluster for the data point.
    """
    responsibility = {}
    sum_responsibility = 0.0
    for key, value in centroids.items():
        responsibility[key] = math.exp(-beta*euclidean_distance(data_point, value))
        sum_responsibility += math.exp(-beta*euclidean_distance(data_point, value))
    for key, value in responsibility.items():
        responsibility[key] = value / sum_responsibility
    return responsibility


# problem for students
def update_soft_assignment(data, centroids, beta):
    """Find the responsibility of each cluster for all data points.
    You should use the get_responsibility function (that you previously implemented).

    Arguments:
        data: a list of lists representing all data points
        centroids: a dictionary representing the centroids where the keys are
                   strings (centroid names) and the values are lists of
                   centroid locations

    Returns: a dictionary whose keys are the data points of type 'tuple'
             and values are the dictionary returned by get_responsibility function.
             (In python, 'list' cannot be the 'key' of 'dict')
             
    """
    new_assignment = {}
    for data_point in data:
        new_assignment[tuple(data_point)] = get_responsibility(data_point, centroids, beta)
    return new_assignment
    # pass
            

# problem for students
def update_centroids(soft_assignment_dict):
    """Update centroid locations with the responsibility of the cluster for each point
    as a weight. You can numpy methods for simple array computations. But the values of 
    the result dictionary must be of type 'list'.

    Arguments:
        assignment_dict: the dictionary returned by update_soft_assignment function

    Returns: A new dictionary representing the updated centroids
    """
    new_centroid = {}
    sum_centroid = {}
    # print(soft_assignment_dict)
    for key, centroid in soft_assignment_dict.items():
        for centroid_key, centroid_value in centroid.items():
            if not centroid_key in new_centroid:
                new_centroid[centroid_key] = np.array(list(key)) * centroid_value
                sum_centroid[centroid_key] = centroid_value
            else:
                new_centroid[centroid_key] += np.array(list(key)) * centroid_value
                sum_centroid[centroid_key] += centroid_value
    for key, value in new_centroid.items():
        new_centroid[key] = (value / sum_centroid[key]).tolist()
    return new_centroid

    # pass

def main(data, init_centroids):
    #######################################################
    # You do not need to change anything in this function #
    #######################################################
    beta = 3
    centroids = init_centroids
    old_centroids = None
    total_step = 7
    for step in range(total_step):
        # save old centroid
        old_centroids = centroids
        # new assignment
        soft_assignment_dict = update_soft_assignment(data, old_centroids, beta)
        # update centroids
        centroids = update_centroids(soft_assignment_dict)
        # plot centroid
        fig = plot_2d_soft(soft_assignment_dict, centroids)
        plt.title(f"step{step}")
        fig.savefig(os.path.join("results", "2D_soft", f"step{step}.png"))
        plt.clf()
    print(f"{total_step} iterations were completed.")
    return centroids


if __name__ == '__main__':
    data, label = read_data("data/data_2d.csv")
    init_c = load_centroids("data/2d_init_centroids.csv")
    final_c = main(data, init_c)
    write_centroids_tofile("2d_final_centroids_with_soft_kmeans.csv", final_c)
