import pygame
import pygame_gui
from spots import *
from algorithms import *
from sprite import *
import time
from termcolor import colored
import pickle
import copy
import json

WIDTH = 500
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
ICON = pygame.image.load('icon.png')
maze = []
pygame.display.set_icon(ICON)
pygame.display.set_caption("Robotic Waiter")

sprite_sheet_image = pygame.image.load("pacman.png").convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)

animation_list = []
aniamtion_steps = 3
for x in range(aniamtion_steps):
    animation_list.append(sprite_sheet.get_image(x, 25, 25, 1, BLACK))

# Initialize pygame_gui
pygame.init()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Create input field and button
# input_field = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((150, 510), (200, 30)), manager=manager)

# submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 550), (100, 30)), text='Submit', manager=manager)
numberoftables_TextEntry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 510), (200, 30)), manager=manager)
numberoftables_Button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10+210, 510), (200, 30)), text='Enter Number of tables', manager=manager)
# commands_TextEntry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 550), (200, 30)), manager=manager)

saveLayout_Button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 550), (100, 30)), text='Save Layout', manager=manager)
loadLayout_Button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 550), (100, 30)), text='Load Layout', manager=manager)

def draw_pacman(path, grid, rows, width, start):
    current_time = pygame.time.get_ticks()
    frame = 0
    animation_cd = 1
    last_update = pygame.time.get_ticks()
    curr_pos = start.get_pos()
    while len(path) > 0:
        next_pos = path.pop()
        nxt_pos = tuple(ti * 25 for ti in next_pos)

        if next_pos[0] < curr_pos[0]:
            flipped_surface = pygame.transform.flip(animation_list[frame], True, False)
        elif next_pos[1] < curr_pos[1]:
            flipped_surface = pygame.transform.rotate(animation_list[frame], 90)
        elif next_pos[1] > curr_pos[1]:
            flipped_surface = pygame.transform.rotate(animation_list[frame], -90)
        else:
            flipped_surface = animation_list[frame]

        draw(WIN, grid, rows, width)

        WIN.blit(flipped_surface, nxt_pos, special_flags=pygame.BLEND_RGBA_ADD)
        pygame.display.update()
        time.sleep(0.09)

        frame += 1
        if frame > 2:
            frame = 0
        last_update = current_time
        curr_pos = next_pos

def write_preset(maze, number):
    try:
        with open('maze{}.pckl'.format(number), 'wb') as fp:
            pickle.dump(maze, fp)

        print(colored('Wrote preset to file', 'cyan'))
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")

def save_restaurant_layout(grid):
    mazebarrierslocal = []
    mazestartlocal=[]
    mazetableslocal=[]
    for row in grid:
        for spot in row:
            if spot.is_barrier():
                mazebarrierslocal.append(spot.get_pos())
            elif spot.is_start():
                mazestartlocal.append(spot.get_pos())
            elif spot.is_end():
                mazetableslocal.append(spot.get_pos())
    try:
        with open('restaurantlayoutbarriers.pckl', 'wb') as fp:
            pickle.dump(mazebarrierslocal, fp)
        with open('restaurantlayoutstart.pckl', 'wb') as fp:
            pickle.dump(mazestartlocal, fp)
        with open('restaurantlayouttables.pckl', 'wb') as fp:
            pickle.dump(mazetableslocal, fp)
        print(f"Saved preset maze  successfully.")
    except Exception as e:
        print("Oops!", e.__class__, "occurred while saving the maze.")

def load_restaurant_layout(grid):
    localstart = None
    localtables=[]
    try:
        with open('restaurantlayoutbarriers.pckl', 'rb') as fp:
            maze = pickle.load(fp)
        for i in range(len(maze)):
            x, y = maze[i]
            spot = grid[x][y]
            spot.make_barrier()
        
        with open('restaurantlayoutstart.pckl', 'rb') as fp:
            maze = pickle.load(fp)
        for i in range(len(maze)):
            x, y = maze[i]
            spot = grid[x][y]
            spot.make_start()
            localstart=spot
        
        with open('restaurantlayouttables.pckl', 'rb') as fp:
            maze = pickle.load(fp)
        for i in range(len(maze)):
            x, y = maze[i]
            spot = grid[x][y]
            spot.make_end()
            localtables.append(spot)

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
    return localstart,localtables,len(localtables)

def load_preset_maze(grid, number):
    try:
        with open('maze{}.pckl'.format(number), 'rb') as fp:
            maze = pickle.load(fp)
        for i in range(len(maze)):
            x, y = maze[i]
            spot = grid[x][y]
            spot.make_barrier()
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")

def reset(grid):
    for row in grid:
        for spot in row:
            spot.reset()

def get_score(grid):
    count = 0
    for row in grid:
        for spot in row:
            if spot.is_path():
                count += 1
    print("Cost:", colored(count, 'yellow'))
    return count

def update_title(algo, time=0):
    pygame.display.set_caption(f"Pacman Maze Solver : {algo} -> {round(time,3)}s")
    if time == 0:
        pygame.display.set_caption(f"Pacman Maze Solver")

def restartmap(grid, start, tables):
    reset(grid)
    load_restaurant_layout(grid)
    start.make_start()
    for i in range(len(tables)):
        print(tables[i].get_pos())
        tables[i].make_end()
    # end.make_end()
    # end2.make_end()

def main(win, width):
    isFirstdone = False
    isSeconddone = False
    firstcost = 0
    secondcost = 0

    firstpath = None
    secondpath = None

    ROWS = 20
    grid = make_grid(ROWS, width)

    start = None
    currentTableIndex=0
    numberoftables=0
    tables = []
    # end = None
    # end2 = None

    run = True
    first_run = True
    while run:
        time_delta = pygame.time.Clock().tick(30) / 1000.0
        if first_run:
            draw(win, grid, ROWS, width)
        if get_path():
            first_run = False
            draw_pacman(get_path(), grid, ROWS, width, start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == numberoftables_Button:
                    if len(tables)>0:
                        for i in range(len(tables)):
                            if tables[0]!= None:
                                tables[0].reset()
                            tables.pop(0)
                    numberoftables = int(numberoftables_TextEntry.get_text())
                    currentTableIndex=0
                    tables = [None for _ in range(numberoftables+1)] 
                    print("Number of tables are: ", numberoftables)

                if event.ui_element == saveLayout_Button:
                    save_restaurant_layout(grid)

                if event.ui_element == loadLayout_Button:
                    update_title("")
                    first_run = True
                    start = None
                    
                    reset(grid)
                    print(colored('Loaded preset', 'green'))
                    start, tables, numberoftables =load_restaurant_layout(grid)
                    currentTableIndex=numberoftables

            if pygame.mouse.get_pressed()[0]:  # LEFT
                first_run = True
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                
                # Check if row and col are within valid range
                if 0 <= row < ROWS and 0 <= col < ROWS:
                    spot = grid[row][col]
                    if not start:
                        start = spot
                        start.make_start()
                        print("start: ")


                    elif  currentTableIndex<numberoftables and spot not in tables and spot != start:
                        currentspot = spot
                        currentspot.make_end()
                        tables.append(currentspot)
                        print("table number: ", currentTableIndex,"")
                        currentTableIndex=currentTableIndex+1

                    elif currentTableIndex==numberoftables and spot not in tables and spot != start:
                        spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                first_run = True
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                
                # Check if row and col are within valid range
                if 0 <= row < ROWS and 0 <= col < ROWS:
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot in tables:
                        removedtableindex = tables.index(spot)
                        tables[removedtableindex]=None
                        tables.pop(removedtableindex)
                        end = None
                        currentTableIndex=currentTableIndex-1
                    # elif spot == end2:
                    #     end2 = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and currentTableIndex==numberoftables and numberoftables_TextEntry.is_focused==False:
                    print("hiiii")
                    jsondata=[]
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    i=0

                    for tabledestination in tables:
                        # print(tabledestination.get_pos(),"  ",tables[0].get_pos())
                        restartmap(grid, start, tables)
                        # first destination
                        st = time.time()
                        Astar(lambda: draw(win, grid, ROWS, width), grid, start, tabledestination)
                        et = time.time()
                        firstcost = get_score(grid)
                        # print("Time taken for {}: ".format(colored('A*', 'green')), colored(et - st, 'blue'))
                        print("cost is: ",firstcost)
                        update_title("A*", et - st)
                        pathroute = copy.deepcopy(get_path())
                        print("route is: ",pathroute)
                        startwithdestination= "k"+str(i)
                        jsonroute=[]
                        jsonroute.append(start.get_pos())
                        while len(pathroute) > 0:
                            next_pos = pathroute.pop()
                            jsonroute.append(next_pos)
                        jsondata.append({
                            startwithdestination:jsonroute,
                            "cost":firstcost
                        })
                        # print("hello: ",jsondata)
                        draw_pacman(get_path(), grid, ROWS, width, start)
                        pygame.time.delay(2000)
                        restartmap(grid, start, tables)

                        # //restartmap(grid, start, tables)
                        # first destination
                        st = time.time()
                        Astar(lambda: draw(win, grid, ROWS, width), grid, tabledestination, start)
                        et = time.time()
                        firstcost = get_score(grid)
                        # print("Time taken for {}: ".format(colored('A*', 'green')), colored(et - st, 'blue'))
                        print("cost is: ",firstcost)
                        update_title("A*", et - st)
                        pathroute = copy.deepcopy(get_path())
                        print("route is: ",pathroute)
                        startwithdestination= str(i)+"k"
                        jsonroute=[]
                        jsonroute.append(tabledestination.get_pos())
                        while len(pathroute) > 0:
                            next_pos = pathroute.pop()
                            jsonroute.append(next_pos)
                        jsondata.append({
                            startwithdestination:jsonroute,
                            "cost":firstcost
                        })
                        # print("hello: ",jsondata)
                        draw_pacman(get_path(), grid, ROWS, width, start)
                        pygame.time.delay(2000)
                        restartmap(grid, start, tables)




                        i=i+1
                    
                    
                    for i in range(len(tables)):
                        print("distances according to {} table".format(i+1))
                        for j in range(len(tables)):
                            if i == j:
                                continue
                            # print(tabledestination.get_pos(),"  ",tables[0].get_pos())
                            restartmap(grid, start, tables)
                            # first destination
                            st = time.time()
                            Astar(lambda: draw(win, grid, ROWS, width), grid, tables[i], tables[j])
                            et = time.time()
                            firstcost = get_score(grid)
                            print("Time taken for {}: ".format(colored('A*', 'green')), colored(et - st, 'blue'))
                            print("cost is: ",firstcost)
                            update_title("A*", et - st)
                            pathroute = copy.deepcopy(get_path())
                            print("route is: ",pathroute)
                            startwithdestination= str(i)+str(j)
                            jsonroute=[]
                            jsonroute.append(tables[i].get_pos())
                            while len(pathroute) > 0:
                                next_pos = pathroute.pop()
                                jsonroute.append(next_pos)
                            jsondata.append({
                                startwithdestination:jsonroute,
                                "cost":firstcost
                            })
                            draw_pacman(get_path(), grid, ROWS, width, start)
                            pygame.time.delay(2000)
                            restartmap(grid, start, tables)

                    
                    json_data = json.dumps(jsondata,indent=4)
                    with open('astardistancesdata.json', 'w') as file:
                        file.write(json_data)
                    # print("helloz: ",json_data)


                if event.key == pygame.K_c and numberoftables_TextEntry.is_focused==False:
                    first_run = True
                    start = None
                    end = None
                    end2 = None
                    grid = make_grid(ROWS, width)
                    update_title("")
                if event.key == pygame.K_r and start and currentTableIndex==numberoftables and numberoftables_TextEntry.is_focused==False:
                    update_title("")
                    first_run = True
                    for row in grid:
                        for spot in row:
                            if spot.is_open() or spot.is_closed() or spot.is_path():
                                spot.reset()
                    print(colored('Reset path', 'red'))

                
                if event.key == pygame.K_1 and numberoftables_TextEntry.is_focused==False:
                    update_title("")
                    first_run = True
                    start = None
                    end = None
                    end2 = None
                    reset(grid)
                    print(colored('Loaded preset', 'green'))
                    load_preset_maze(grid, 0)

        manager.update(time_delta)
        manager.draw_ui(WIN)
        pygame.display.update()

    pygame.quit()

main(WIN, WIDTH)
