#!/usr/bin/env python
"""
from idk import NODE_COORDINATES

TASK_GENERATION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST.txt"
TASK_CONVERSION_FILE_PATH = "/home/chloe/Downloads/LKH-3.0.9/MTSP_TEST_CONVERSION.txt

def read_tsp_solution(TASK_GENERATION_FILE_PATH):
    with open(file_path, 'r') as file:
        tsp_solution = [int(line.strip()) for line in file]
    return tsp_solution

def convert_labels(tsp_solution, NODE_COORDINATES):
    original_solution = [NODE_COORDINATES[label] for label in tsp_solution]
    return original_solution

def write_original_solution(original_solution, output_file_path):
    with open(output_file_path, 'w') as file:
        for label in original_solution:
            file.write(str(label) + '\n')

"""