import tkinter as tk
import random
import time

GRID_SIZE = 12
CELL_SIZE = 30
NUM_COLORS = 6
COLORS = ["red", "green", "blue", "yellow", "purple", "orange"]

class FloodFillGame:
    def __init__(self, master): 
        self.master = master
        self.grid = [[random.randint(0, NUM_COLORS - 1) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.canvas = tk.Canvas(master, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
        self.canvas.pack()
        self.draw_grid()
        
        # Frame to hold buttons side by side
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        bfs_btn = tk.Button(button_frame, text="Solve with BFS", command=self.auto_solve_bfs)
        bfs_btn.pack(side="left", padx=5)

        dfs_btn = tk.Button(button_frame, text="Solve with DFS", command=self.auto_solve_dfs)
        dfs_btn.pack(side="left", padx=5)

        reset_btn = tk.Button(button_frame, text="Reset Grid", command=self.reset_grid)
        reset_btn.pack(side="left", padx=5)

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = COLORS[self.grid[i][j]]
                x0, y0 = j * CELL_SIZE, i * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    def flood_fill_bfs(self, srow, scol, newcolor):
        rows = len(self.grid)
        cols = len(self.grid[0])
        currentcolor = self.grid[srow][scol]
        if currentcolor == newcolor:
            return

        queue = [(srow, scol)]
        self.grid[srow][scol] = newcolor
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            r, c = queue.pop(0)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and self.grid[nr][nc] == currentcolor:
                    self.grid[nr][nc] = newcolor
                    queue.append((nr, nc))

    def flood_fill_dfs(self, srow, scol, newcolor):
        rows = len(self.grid)
        cols = len(self.grid[0])
        currentcolor = self.grid[srow][scol]
        if currentcolor == newcolor:
            return

        visited = set()
        stack = [(srow, scol)]

        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            self.grid[x][y] = newcolor

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and self.grid[nx][ny] == currentcolor:
                    stack.append((nx, ny))

    def get_neighbors_color_counts(self):
        visited = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]
        queue = [(0, 0)]
        start_color = self.grid[0][0]
        visited[0][0] = True
        color_count = [0] * NUM_COLORS
        while queue:
            x, y = queue.pop(0)
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and not visited[nx][ny]:
                    if self.grid[nx][ny] == start_color:
                        visited[nx][ny] = True
                        queue.append((nx, ny))
                    else:
                        color_count[self.grid[nx][ny]] += 1
        return color_count

    def is_uniform(self):
        target = self.grid[0][0]
        for row in self.grid:
            if any(cell != target for cell in row):
                return False
        return True

    def auto_solve_bfs(self):
        while not self.is_uniform():
            color_count = self.get_neighbors_color_counts()
            best_color = max(range(NUM_COLORS), key=lambda c: color_count[c])
            self.flood_fill_bfs(0, 0, best_color)
            self.draw_grid()
            self.master.update()
            time.sleep(0.3)

    def auto_solve_dfs(self):
        while not self.is_uniform():
            color_count = self.get_neighbors_color_counts()
            best_color = max(range(NUM_COLORS), key=lambda c: color_count[c])
            self.flood_fill_dfs(0, 0, best_color)
            self.draw_grid()
            self.master.update()
            time.sleep(0.3)

    def reset_grid(self):
        self.grid = [[random.randint(0, NUM_COLORS - 1) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.draw_grid()

if __name__ == "__main__":  
    root = tk.Tk()
    root.title("Flood-fill Game")
    game = FloodFillGame(root)
    root.mainloop()
