import unittest
from maze import Maze
from cell import Cell

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)  
        self.assertEqual(len(m1._cells), num_rows) 
        self.assertEqual(len(m1._cells[0]), num_cols)
        
    def test_cell_wall_defaults(self):
        cell = Cell(0, 0, 10, 10)
        self.assertTrue(cell.has_left_wall)
        self.assertTrue(cell.has_right_wall)
        self.assertTrue(cell.has_top_wall)
        self.assertTrue(cell.has_bottom_wall)

    def test_maze_different_dimensions(self):
        m1 = Maze(0, 0, 1, 1, 10, 10)
        self.assertEqual(len(m1._cells), 1)
        self.assertEqual(len(m1._cells[0]), 1)
        m2 = Maze(0, 0, 5, 1, 10, 10)
        self.assertEqual(len(m2._cells), 5)
        self.assertEqual(len(m2._cells[0]), 1)
        m3 = Maze(0, 0, 1, 5, 10, 10)
        self.assertEqual(len(m3._cells), 1)
        self.assertEqual(len(m3._cells[0]), 5)

    def test_maze_cell_wall_access(self):
        m = Maze(0, 0, 3, 3, 10, 10, break_entrance_exit=False, generate_maze=False)
        for row in m._cells:
            for cell in row:
                self.assertTrue(cell.has_left_wall)
                self.assertTrue(cell.has_right_wall)
                self.assertTrue(cell.has_top_wall)
                self.assertTrue(cell.has_bottom_wall)


    def test_cell_positioning(self):
        m = Maze(0, 0, 2, 2, 10, 10)
        self.assertEqual(m._cells[0][0]._x1, 0)
        self.assertEqual(m._cells[0][0]._y1, 0)
        self.assertEqual(m._cells[0][1]._x1, 10)
        self.assertEqual(m._cells[0][1]._y1, 0)
        self.assertEqual(m._cells[1][0]._x1, 0)
        self.assertEqual(m._cells[1][0]._y1, 10)
        self.assertEqual(m._cells[1][1]._x1, 10)
        self.assertEqual(m._cells[1][1]._y1, 10)

    def test_wall_removal(self):
        cell = Cell(0, 0, 10, 10)
        cell.has_left_wall = False
        self.assertFalse(cell.has_left_wall)
        cell.has_right_wall = False
        self.assertFalse(cell.has_right_wall)
        cell.has_top_wall = False
        self.assertFalse(cell.has_top_wall)
        cell.has_bottom_wall = False
        self.assertFalse(cell.has_bottom_wall)
        
    def test_maze_initialization_with_offset(self):
        m = Maze(50, 50, 2, 2, 10, 10)
        self.assertEqual(m._cells[0][0]._x1, 50)
        self.assertEqual(m._cells[0][0]._y1, 50)
        self.assertEqual(m._cells[0][1]._x1, 60)
        self.assertEqual(m._cells[0][1]._y1, 50)
        self.assertEqual(m._cells[1][0]._x1, 50)
        self.assertEqual(m._cells[1][0]._y1, 60)
        self.assertEqual(m._cells[1][1]._x1, 60)
        self.assertEqual(m._cells[1][1]._y1, 60)
        
    def test_maze_entrance_and_exit(self):
        num_rows = 5
        num_cols = 5
        m = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m._cells[0][0].has_top_wall)
        self.assertFalse(m._cells[num_rows - 1][num_cols - 1].has_bottom_wall)

    def test_reset_cells_visited(self):
        m = Maze(0, 0, 3, 3, 10, 10, break_entrance_exit=False)
        m._cells[0][0].visited = True
        m._cells[1][1].visited = True
        m._cells[2][2].visited = True
        m._reset_cells_visited()
        for row in m._cells:
            for cell in row:
                self.assertFalse(cell.visited)
        
if __name__ == "__main__":
    unittest.main()
