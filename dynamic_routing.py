# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import datetime
import argparse
import time
import numpy as np
from random import randint

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='input_matrix', help='Name of the input file containing the adjacency matrix')
parser.add_argument('-o', dest='output_file', help='Name for the configuration file for GraphViz')
parser.add_argument('-t', dest='time_interval', type=int, help='Defines the time interval in seconds for route generation and update')
parser.add_argument('-n', dest='n_iterations', type=int, help='Defines the number of iterations with -t seconds between each')

args = parser.parse_args()

# Display help if any argument is missing
if len(sys.argv) != 9:
    parser.print_help()
    quit()

input_file = open(args.input_matrix, "r")

file_contents = input_file.readlines()
matrix_dimension = int(file_contents[0][0])
adjacency_matrix = np.zeros((matrix_dimension, matrix_dimension), dtype=np.int32)

# Remove whitespace between data in the input file
for line in range(1, len(file_contents)):
    file_contents[line] = file_contents[line].replace(" ", "")

# Load data from the file into the matrix
for line in range(1, matrix_dimension + 1):
    for column in range(matrix_dimension):
        adjacency_matrix[line - 1][column] = file_contents[line][column]

# Assign pseudo-random weights to valid graph edges
def initialize_weights(adj_matrix):
    for line in range(matrix_dimension):
        for column in range(matrix_dimension):
            if adj_matrix[line][column] != 0:
                adj_matrix[line][column] = randint(5, 20)

# Update edge values pseudo-randomly
def update_weights(adj_matrix):
    for line in range(matrix_dimension):
        for column in range(matrix_dimension):
            if adj_matrix[line][column] != 0:
                difference = randint(-10, 10)
                if (adj_matrix[line][column] + difference) < 0:
                    adj_matrix[line][column] -= difference
                else:
                    adj_matrix[line][column] += difference

# Generate routing tree images
def generate_image(dot_list, vertex, iteration):
    dot_file = open(args.output_file, 'w')
    dot_file.write("graph routing {")
    for item in dot_list:
        dot_file.write(item)
        dot_file.write('[label=" ' + str(adjacency_matrix[int(item[0])][int(item[5])]) + '"]; ')
    if vertex != 'global':
        dot_file.write('label="' + 'Router tree ' + str(vertex) + ' - Iteration ' + str(iteration) + '"; ')
        dot_file.write(' }')
        dot_file.close()
        os.system('dot -Tpng ' + args.output_file + ' -o tree_iter' + str(iteration) + '_router' + str(vertex) + '.png')
    else:
        dot_file.write('label="' + 'Global Tree - Iteration ' + str(iteration) + '"; ')
        dot_file.write(' }')
        dot_file.close()
        os.system('dot -Tpng ' + args.output_file + ' -o global_tree_iter' + str(iteration) + '.png')

# Create a list with edges in GraphViz accepted format
def create_dot(path_list):
    edges_list = []
    dot_list = []
    intermediate_list = []
    for item in range(len(path_list) - 1):
        if path_list[item] == '-':
            continue
        if path_list[item + 1] != '-':
            edges_list.append(path_list[item])
            edges_list.append(path_list[item + 1])
            edges_list.append('*')

    for item in range(len(edges_list) - 1):
        if (edges_list[item] == '*') or (edges_list[item + 1] == '*'):
            continue
        intermediate_list.append(str(edges_list[item]) + ' -- ' + str(edges_list[item + 1]))

    for item in intermediate_list:
        if item not in dot_list:
            dot_list.append(item)
    return dot_list

# Find the nearest vertex that is not yet in the spt_set
def min_distance(dist, spt_set):
    min_val = 2147483647

    for v in range(matrix_dimension):
        if (spt_set[v] == False and dist[v] <= min_val):
            min_val = dist[v]
            min_index = v
    return min_index

# Function to store the shortest path from source to v
def print_path(parent, v, path_list, src, history):
    if (parent[v] == -1):
        return

    print_path(parent, parent[v], path_list, src, history)
    path_list.append(v)
    history.write(' ' + str(v))

def generate_global(adj_matrix, iteration):
    global_edges = []
    for line in range(matrix_dimension):
        for column in range(matrix_dimension):
            if adj_matrix[line][column] != 0:
                global_edges.append(str(line) + ' -- ' + str(column))
    generate_image(global_edges, 'global', iteration)

# Function to start storing routing data in the history file
def print_solution(dist, parent, src, path_list, history):
    history.write('\n' + '-' * 50)
    history.write('\n' + str(datetime.datetime.now()))
    history.write("\n\nRouter --- Minimum Distance --- Path")
    for v in range(matrix_dimension):
        if (v != src):
            path_list.append(src)
        history.write(("\n%d -> %d\t\t%d\t\t%d" % (src, v, dist[v], src)))
        print_path(parent, v, path_list, src, history)
        if (v != src):
            path_list.append('-')

def dijkstra(adj_matrix, src, history):
    path_list = []
    dist = np.zeros((matrix_dimension), dtype=np.int32)
    spt_set = np.zeros((matrix_dimension), dtype=np.int32)
    parent = np.zeros((matrix_dimension), dtype=np.int32)

    # Initialize distances with a very high value and no vertex in the spt_set
    for index in range(matrix_dimension):
        parent[src] = -1
        dist[index] = 2147483647
        spt_set[index] = False

    # Distance from source to itself will always be 0
    dist[src] = 0

    # Find the shortest path to all vertices
    for _ in range(matrix_dimension):
        u = min_distance(dist, spt_set)

        # Place the calculated vertex in the spt_set
        spt_set[u] = True

        # Update the distances of vertices adjacent to the chosen vertex
        for v in range(matrix_dimension):
            if ((spt_set[v] == False) and (adj_matrix[u][v]) and (dist[u] != 2147483647) and (dist[u] + adj_matrix[u][v] < dist[v])):
                parent[v] = u
                dist[v] = dist[u] + adj_matrix[u][v]

    print_solution(dist, parent, src, path_list, history)
    return path_list


initialize_weights(adjacency_matrix)
history = open("history.txt", "w")

for iteration in range(args.n_iterations):
    generate_global(adjacency_matrix, iteration)
    for vertex in range(matrix_dimension):
        result = create_dot(dijkstra(adjacency_matrix, vertex, history))
        # Pass the list of edges to the function that generates the images
        generate_image(result, vertex, iteration)
    if iteration != args.n_iterations - 1:
        time.sleep(args.time_interval)
        update_weights(adjacency_matrix)
history.close()

