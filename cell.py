from geometry import Point, Line

class Cell:
    def __init__(self, x1, y1, x2, y2, window= None,  bg_color="white"):
        
        # boundary coordinates
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = window
        self.visited = False
        self.bg_color = bg_color
        
        # Wall states
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

    def draw(self):
        
        if self._win is None:
            return
        
        wall_color = "black"  
        erase_color = self.bg_color
        
        # Draw left wall
        left_wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        self._win.draw_line(left_wall, wall_color if self.has_left_wall else erase_color)

        # Draw right wall
        right_wall = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        self._win.draw_line(right_wall, wall_color if self.has_right_wall else erase_color)

        # Draw top wall
        top_wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        self._win.draw_line(top_wall, wall_color if self.has_top_wall else erase_color)

        # Draw bottom wall
        bottom_wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        self._win.draw_line(bottom_wall, wall_color if self.has_bottom_wall else erase_color)

    def draw_move(self, to_cell, undo=False):
        
        # center points of the two cells
        from_center_x = (self._x1 + self._x2) / 2
        from_center_y = (self._y1 + self._y2) / 2
        to_center_x = (to_cell._x1 + to_cell._x2) / 2
        to_center_y = (to_cell._y1 + to_cell._y2) / 2
        color = "gray" if undo else "red"

        # Draw the move line
        move_line = Line(Point(from_center_x, from_center_y), Point(to_center_x, to_center_y))
        self._win.draw_line(move_line, color)