import vtk
class Grid(object):
    """This class implements access to triangular grids."""

    def __init__(self, vertices, elements):
        """
        Initialize a grid.

        This routine takes an Nx2 Numpy array of N vertices
        and a Mx3 Numpy array with corresponding M elements.
        """
        import numpy as np

        if not (isinstance(vertices, np.ndarray) and
                isinstance(elements, np.ndarray)):
            raise ValueError("The input data must be of type numpy.ndarray.")
        self.__vertices = vertices
        self.__elements = elements

        # Some protection against modifying the grid data externally
        self.__vertices.setflags(write=False)
        self.__elements.setflags(write=False)


    @classmethod
    def from_vtk_file(cls, filename):
        """Create a grid from a given vtk file."""

        # Insert code that reads a grid from a vtk file.
        # For this you should look up the VtkUnstructuredGridReader class.
        # Make sure that you only import triangular elements (check the vtk cell type).
        # VTK only knows vertices in 3 dimensions. Simply ignore the z-coordinate.
        
        # Below is a possible stub
        
        # import os.path
        # import vtk
        # import numpy as np

        # if not os.path.isfile(filename):
          #   raise ValueError("File does not exist.")

        # return cls(points, elements)
        import os.path
        import vtk
        import numpy as np
        if not os.path.isfile(filename):
            raise ValueError("File does not exist.")
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(filename)
        reader.Update()
        m = reader.GetOutput()
        lenpt = m.GetNumberOfPoints()
        points = np.array([(m.GetPoint(i)[0], m.GetPoint(i)[1], m.GetPoint(i)[2])
                           for i in range(lenpt)])
        lencell = m.GetNumberOfCells()
        elements = np.array([[m.GetCell(i).GetPointId(j) for j in range(3)]
                             for i in range(lencell)
                              if m.GetCell(i).__vtkname__ == 'vtkTriangle'])
        
        
        return cls(points, elements)

    @property
    def number_of_vertices(self):
        """Return the number of vertices."""
        return self.__vertices.shape[0]

    @property
    def number_of_elements(self):
        """Return the number of elements."""
        return self.__elements.shape[0]

    @property
    def vertices(self):
        """Return the vertices."""
        return self.__vertices

    @property
    def elements(self):
        """Return the elements."""
        return self.__elements

    def get_corners(self, element_id):
        """Return the 3x3 matrix of corners associated with an element."""

        # Implement this
        import numpy as np
        v = self.vertices 
        e = self.elements
        el = e[element_id]
        return np.array([v[el[i]] for i in range(3)]).transpose()

    def get_jacobian(self, element_id):
        """Return the jacobian associated with a given element id."""
        import numpy as np
        [[x1, x2, x3], [y1, y2, y3], [z1, z2, z3]] = self.get_corners(element_id)
        n1 = np.array([x1, y1, z1])
        n2 = np.array([x2, y2, z2])
        n3 = np.array([x3, y3, z3])
        return np.array([n2 - n1, n3 - n1, n3 - n2]).T
        # Implement this
        
        
 
    def export_to_vtk(self, fname, point_data=None):
        """Export grid to a vtk file. Optionally also export point data."""
        from vtk import vtkUnstructuredGrid, vtkPointData, vtkDoubleArray, \
            vtkPoints, vtkUnstructuredGridWriter, VTK_TRIANGLE

        grid = vtkUnstructuredGrid()

        if point_data is not None:

            data = grid.GetPointData()
            scalar_data = vtkDoubleArray()
            scalar_data.SetNumberOfValues(len(point_data))
            for index, value in enumerate(point_data):
                scalar_data.SetValue(index, value)
            data.SetScalars(scalar_data)

        points = vtkPoints()
        points.SetNumberOfPoints(self.number_of_vertices)
        for index in range(self.number_of_vertices):
            points.InsertPoint(
                index,
                (self.vertices[0, index], self.vertices[1, index], self.vertices[2, index]))

        grid.SetPoints(points)

        for index in range(self.number_of_elements):
            grid.InsertNextCell(
                VTK_TRIANGLE, 3,
                [self.elements[0, index], self.elements[1, index],
                 self.elements[2, index]]
            )

        writer = vtkUnstructuredGridWriter()
        writer.SetFileName(fname)
        writer.SetInputData(grid)
        writer.Write()

        return grid

# grid = Grid.from_vtk_file('example.vtk')

# (grid.vertices[1])
# print(grprintid.elements[1])
# print(grid.get_corners(1))
# print(grid.get_jacobian(1))
