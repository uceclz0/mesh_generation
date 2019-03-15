#test
import os
import yaml
from ..grid import Grid
import numpy as np

def load_test_data(yml_file_path):
    """Given a file path of the yaml file, return the data in the file."""
    with open(yml_file_path, 'r') as f:
        s = f.read()
        test_data = yaml.load(s)
    return test_data

def test_vertices():
    #yml_files = ['grid1.yml']
    yml_file_path = os.path.join(os.path.dirname(__file__), 'fixture', 'grid_1.yml')
    test_data = load_test_data(yml_file_path)
    ans = test_data.pop('ans')
    ans_vertice = ans['vertice']
    
    grid = Grid.from_vtk_file('example.vtk')
    v = grid.vertices[1]
    (v == ans_vertice).all

def test_elements():
    yml_file_path = os.path.join(os.path.dirname(__file__), 'fixture', 'grid_1.yml')
    test_data = load_test_data(yml_file_path)
    ans = test_data.pop('ans')
    ans_element = ans['element']

    grid = Grid.from_vtk_file('example.vtk')
    e = grid.elements[1]
    (e == ans_element).all

def test_corners():
    yml_file_path = os.path.join(os.path.dirname(__file__), 'fixture', 'grid_1.yml')
    test_data = load_test_data(yml_file_path)
    ans = test_data.pop('ans')
    ans_corner = ans['corner']
    
    grid = Grid.from_vtk_file('example.vtk')
    c = grid.get_corners(1)
    (c == ans_corner).all


# if __name__ == '__main__':
#     test_vertices()
#     # test_wrong()
