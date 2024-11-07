import random
import time
from cell import Cell

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, break_entrance_exit=True, seed = None, bg_color="#d9d9d9", generate_maze=True):
        
        # Initialization
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self.bg_color = bg_color
        
        
        if seed is not None:
            random.seed(seed)
        
        # Initialize the grid of cells
        self._create_cells()
        
        if break_entrance_exit:
            self._break_entrance_and_exit()
        
        if generate_maze:
            self._break_walls_r(0, 0)
            self._reset_cells_visited()

    def _create_cells(self):
        
        # Populate the grid with Cell objects arranged in a 2D list
        for row in range(self.num_rows):
            cell_row = []
            for col in range(self.num_cols):
                # Calculate cell's x/y boundaries based on grid position
                cell_x1 = self.x1 + col * self.cell_size_x
                cell_y1 = self.y1 + row * self.cell_size_y
                cell_x2 = cell_x1 + self.cell_size_x
                cell_y2 = cell_y1 + self.cell_size_y

                # Create and store each cell
                cell = Cell(cell_x1, cell_y1, cell_x2, cell_y2, self.win)
                cell_row.append(cell)

            # Add the completed row to the grid
            self._cells.append(cell_row)

        # Draw each cell after the grid is populated
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self._draw_cell(row, col)
                
                
                
    def _break_entrance_and_exit(self):
        
        # Remove the top left entrance wall 
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False 
        self._draw_cell(0, 0)

        # Remove the bottom right exit wall
        exit_cell = self._cells[self.num_rows - 1][self.num_cols - 1]
        exit_cell.has_bottom_wall = False  
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)
        

    def _draw_cell(self, i, j):
        
        # cell at position (i, j)
        cell = self._cells[i][j]
        cell.draw()  # cell's walls
        self._animate() 
        
        
    def _animate(self):
        if self.win:
            self.win.redraw()
            time.sleep(0.05)
            
    def _break_walls_r(self, i, j):
        # Get the current cell and mark it as visited
        current_cell = self._cells[i][j]
        current_cell.visited = True

        # Infinite loop to traverse randomly
        while True:
            directions = []  
            
            # Check neighbors and add unvisited ones to directions list
            if i > 0 and not self._cells[i - 1][j].visited:  # Up
                directions.append((i - 1, j, 'top', 'bottom'))
            if i < self.num_rows - 1 and not self._cells[i + 1][j].visited:  # Down
                directions.append((i + 1, j, 'bottom', 'top'))
            if j > 0 and not self._cells[i][j - 1].visited:  # Left
                directions.append((i, j - 1, 'left', 'right'))
            if j < self.num_cols - 1 and not self._cells[i][j + 1].visited:  # Right
                directions.append((i, j + 1, 'right', 'left'))

            # If no unvisited neighbors, draw the cell and exit loop
            if not directions:
                self._draw_cell(i, j)
                return

            # Pick a random direction
            next_i, next_j, current_wall, next_wall = random.choice(directions)

            # Break the walls between current cell and chosen cell
            setattr(current_cell, f'has_{current_wall}_wall', False)
            setattr(self._cells[next_i][next_j], f'has_{next_wall}_wall', False)

            # Recursively move to the chosen cell
            self._break_walls_r(next_i, next_j)
            
            
    def _reset_cells_visited(self):
        # Iterate through each cell and reset the visited attribute to False
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        # recursive process from the top-left cell (0, 0)
        return self._solve_r(0, 0)
    
    
    def _solve_r(self, i, j):
        # Get the current cell and mark it as visited
        current_cell = self._cells[i][j]
        current_cell.visited = True
        self._animate()  # Call animate to visualize the solution process

        # Check if we've reached the end cell (bottom-right cell)
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        # Define the possible directions: (next_i, next_j, wall_to_check, opposite_wall)
        directions = [
            (i - 1, j, 'top', 'bottom'),    # Up
            (i + 1, j, 'bottom', 'top'),    # Down
            (i, j - 1, 'left', 'right'),    # Left
            (i, j + 1, 'right', 'left')     # Right
        ]

        # Try moving in each direction
        for next_i, next_j, wall, opposite_wall in directions:
            
            # Check if the move is within bounds, no wall blocks the way and the cell is unvisited
            if 0 <= next_i < self.num_rows and 0 <= next_j < self.num_cols:
                next_cell = self._cells[next_i][next_j]
                if not getattr(current_cell, f'has_{wall}_wall') and not next_cell.visited:
                    
                    # Draw the move to the next cell
                    current_cell.draw_move(next_cell, undo=False)

                    # Recursively attempt to solve from the next cell
                    if self._solve_r(next_i, next_j):
                        return True  # Path to the end found

                    # Backtrack: draw an "undo" move
                    current_cell.draw_move(next_cell, undo=True)

        # No valid moves found, return False to backtrack
        return False