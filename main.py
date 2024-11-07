from window import Window
from maze import Maze
import sys

def main():
    
    # window
    window = Window(1000, 800) 
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    # maze
    num_rows = 15
    num_cols = 15
    cell_size_x = 40
    cell_size_y = 40
    maze_width = num_cols * cell_size_x
    maze_height = num_rows * cell_size_y
    margin = 20
    maze_x = (window.width - maze_width) / 2 + margin
    maze_y = (window.height - maze_height) / 2 + margin
    maze = Maze(maze_x, maze_y, num_rows, num_cols, cell_size_x, cell_size_y, window, seed=seed, bg_color=window.bg_color)
    maze.solve()

    window.wait_for_close()

if __name__ == "__main__":
    main()