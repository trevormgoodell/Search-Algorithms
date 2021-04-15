import pygame
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from math import trunc
from data_structs import *
from search_algorithms import *
import time

def init():
    def onsubmit():
        col_valid = False
        row_valid = False
        global columns
        global rows
        try:
            columns = int(x_box.get())
        except:
            messagebox.showerror("ColumnsError", "Please enter a positive integer value for Number of Columns")
        try:
            rows = int(y_box.get())
        except:
            messagebox.showerror("RowsError", "Please enter a positive integer value for Number of Rows")

        if columns <= 0:
            messagebox.showerror("showerror", "Please enter a positive integer value for Number of Columns")
        else:
            col_valid = True

        if rows <= 0:
            messagebox.showerror("ColumnsError", "Please enter a positive integer value for Number of Rows")
        else:
            row_valid = True

        if col_valid and row_valid:
            watch_algo_val=watch_var.get()
            algo=algo_var.get()
            window.quit()
            window.destroy()
    global window
    window = Tk()
    x_label = Label(window, text="Number of Columns:")
    x_box = Entry(window)
    y_label = Label(window, text="Number of Rows:")
    y_box = Entry(window)

    x_label.grid(columnspan=2, row=0)
    x_box.grid(columnspan=1, column=2, row=0) 
    y_label.grid(columnspan=2, row=1)
    y_box.grid(columnspan=1, column=2, row=1)

    global watch_var
    watch_var = IntVar()
    watch_var.set(1)
    watch_algo = ttk.Checkbutton(window, text="Display Steps", onvalue=1, offvalue=0, variable=watch_var)

    watch_algo.grid(columnspan=1, row=2)

    global algo_var
    algo_var = StringVar(window)
    algo_var.set("A*")
    choose_algo = OptionMenu(window, algo_var, "BFS", "DFS", "A*", "BDA*")
    choose_algo.grid(columnspan=1, column=2, row=2)

    submit = Button(window, text="Done", command=onsubmit)
    submit.grid(columnspan=1, column=1, row=3)

    window.update()
    window.mainloop()

def setup(screen):
    def mouse_press(pos, screen, val):
        t = pos[0]
        w = pos[1]
        screen_size = screen.get_size()
        col = int(trunc(t / (screen_size[0] / columns)))
        row = int(trunc(w / (screen_size[1] / rows)))
        try:
            if (row, col) != start and (row, col) != end:
                grid[row][col].moveto = val
        except:
            pass

    def on_click():
        global start
        global end
        start = start_box.get().replace('(', '').replace(')', '').split(',')
        end = end_box.get().replace('(', '').replace(')', '').split(',')
        start = (int(start[0]), int(start[1]))
        end = (int(end[0]), int(end[1]))

        start_row_valid = False
        start_col_valid = False
        end_row_valid = False
        end_col_valid = False

        if start[0] < 0 or start[0] > rows - 1:
            messagebox.showerror("StartXError", "X Coordinate of Start must be in the range [0, " + str(rows-1) + "]")
        else:
            start_row_valid = True
        if start[1] < 0 or start[1] > columns - 1:
            messagebox.showerror("StartYError", "Y Coordinate of Start must be in the range [0, " + str(columns-1) + "]")
        else:
            start_col_valid = True
        if end[0] < 0 or end[0] > rows - 1:
            messagebox.showerror("EndXError", "X Coordinate of End must be in the range [0, " + str(rows-1) + "]")
        else:
            end_row_valid = True
        if end[1] < 0 or end[1] > columns - 1:
            messagebox.showerror("EndYError", "Y Coordinate of End must be in the range [0, " + str(columns-1) + "]")
        else:
            end_col_valid = True

        if start_row_valid and start_col_valid and end_row_valid and end_col_valid:

            for row_ind in range(rows):
                for col_ind in range(columns):
                    grid[row_ind][col_ind].start = start
                    grid[row_ind][col_ind].end = end

            grid[start[0]][start[1]].color = (0,255,0)
            grid[end[0]][end[1]].color = (255,0,0)
            grid[start[0]][start[1]].show(0)
            grid[end[0]][end[1]].show(0)

            setting_grid = True
            messagebox.showinfo("Setting Grid", "Use left click to set obstacles for the algorithm\nRight click will delete them\nHit space when you're done")
            while setting_grid:
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if pygame.mouse.get_pressed()[0]:
                        try:
                            pos = pygame.mouse.get_pos()
                            mouse_press(pos, screen, False)
                        except AttributeError:
                            pass
                    if pygame.mouse.get_pressed()[-1]:
                        try:
                            pos = pygame.mouse.get_pos()
                            mouse_press(pos, screen, True)
                        except AttributeError:
                            pass
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            setting_grid = False
                            break


            window.quit()
            window.destroy()

        pass
    window = Tk()
    
    start_label = Label(window, text="Start Coordinate (row,col):")
    start_box = Entry(window)
    end_label = Label(window, text="End Coordinate (row,col):")
    end_box = Entry(window)

    done = Button(window, text="Done", command=on_click)

    start_label.grid(columnspan=2, row=0)
    start_box.grid(columnspan=1, column=2, row=0) 
    end_label.grid(columnspan=2, row=1)
    end_box.grid(columnspan=1, column=2, row=1)
    done.grid(columnspan=1, row=2)

    window.mainloop()

def search_algorithm(algo, start, end, show_steps, grid):
    results = []
    if algo == "BFS":
        results = BFS(start, end, show_steps, grid)
    if algo == "DFS":
        results = DFS(start, end, show_steps, grid)
    if algo == "A*":
        results = A_STAR(start, end, show_steps, grid)
    if algo == "BDA*":
        results = bidirectional_A_STAR(start, end, show_steps, grid)
    return results

def main():
    init()

    pygame.init()
    screen = pygame.display.set_mode((800,800))

    global grid
    grid = [0 for i in range(rows)]
    base_color = (255,255,255)
    show_steps = int(watch_var.get())
    
    for row in range(rows):
        grid[row] = [square(col, row, screen, base_color, columns, rows, show_steps, (0,0), (0,0), grid) for col in range(columns)]

    for col in range(columns):
        for row in range(rows):
            grid[row][col].show(1)

    need_setup = True
    search = True
    cont = True

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            pygame.quit()
        pygame.display.update()

        if need_setup:
            setup(screen)
            need_setup = False

        if search:
            start_time = time.time()
            path = search_algorithm(algo_var.get(), start, end, show_steps, grid)
            end_time = time.time()
            for (row, col) in path:
                if (row, col) != start and (row, col) != end:
                    grid[row][col].color = (53, 167,165)
                    grid[row][col].show(0)
            examined_cnt = 0
            blocked_cnt = 0
            for row_ind in range(rows):
                for col_ind in range(columns):
                    if grid[row_ind][col_ind].frontier:
                        examined_cnt += 1
                    if not grid[row_ind][col_ind].moveto:
                        blocked_cnt += 1
            answer_str = "Path Length: {path_len}\nRun Time: {run_time}s\nNodes examined: {num}\nBlocked squares: {blocked_cnt}"
            root = Tk()
            root.withdraw()
            messagebox.showinfo("Answer", answer_str.format(path_len=len(path), run_time=round(end_time-start_time,3), num=examined_cnt, blocked_cnt=blocked_cnt))

            search = False

        if cont:
            val = messagebox.askquestion("Again?", "Again?")
            if val == "yes":
                window.quit()
                pygame.display.quit()
                pygame.quit()
                main()
            cont = False

if __name__ == "__main__":
    main()