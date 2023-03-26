'''
Jack Youssef
3/20/2023

Contains the main driver function, which completes a maze using stack and queue implementations.
These search functions are then compared to determine the relative efficiencies.

Other files: abstractcollection.py, abstractstack.py, arrays.py, arraystack.py, grid.py, linkedqueue.py, node.py, & maze1.maz.

CSC 242 Lab 7: 
    "Modify the maze-solving application of Chapter 7 so that it uses a queue instead of a stack.
    Run each version of the application on the same maze and count the number of choice points
    required by each version. Can you conclude anything from the differences in these results? Are
    there best cases and worst cases of the maze problems for stacks and queues? Please write up
    a detailed explanation of your reasoning for your answers and place them into the header doc
    strings section of your driver program."

Findings:
    Can you conclude anything from the differences in these results? 
        - For this scenario, maze1.maz, the stack method took 150 choices and the queue method took 259 choices to solve the maze.
        - The stack method solved the maze using fewer choices.
    Are there best cases and worst cases of the maze problems for stacks and queues?
        - The stack method will not always yield a solution using fewer choices than the queue method.
        - Considering the methodology behind each method, a queue checks each possible solution path at the same time.
        - The stack method, however, checks one solution at a time.
        - This likely means that mazes with more possible paths (decisions possible) to a solution makes a queue implementation slower than a stack one.
        - This is because with each new decision to make (bisects of the maze), the queue method will add that path until it ends or the maze is solved.
        - In this scenario, the stack was faster because the maze had fewer long branches with a dead end.
    
'''

from grid import Grid
from arraystack import ArrayStack
from linkedqueue import LinkedQueue

def main():
    ''' Main driver function. Takes a "Maze" file (maze1.maz), displays the maze,
    attempts to find a solution, displays the result, displays the maze once more, 
    then writes the solution of the original input maze to a file called solution.txt. 
    
    This is done using both stack and queue implementations, then the steps are counted and compared.
    '''

    # opens file, copies contents, and initiates maze Grid
    with open('maze1.maz', 'r') as infile:
        rows = 0
        grid_queue = []
        for line in infile:
            #print(line, end="")
            rows += 1
            copy = str(line).strip()
            grid_queue.append(copy)
        columns = len(line) 
                                                    
        maze = Grid(rows, columns)
        maze_solution = Grid(rows, columns)
        queue_maze_solution = Grid(rows, columns)
    
    # updates contents of Grid
    row_index = 0
    for row in grid_queue:
        column_index = 0
        for item in row:
            if item == 'P':
                start = [row_index, column_index]  # marking start position
            maze[row_index][column_index] = item
            maze_solution[row_index][column_index] = item
            queue_maze_solution[row_index][column_index] = item
            column_index += 1
        row_index += 1

    # display maze
    print('Maze:\n')
    print(maze)
    
    # stack implementation
    stack_choice_count = 0
    stack_path = ArrayStack()
    stack_path.push(start)
    while len(stack_path) != 0:
        current = stack_path.pop()
        if maze_solution[current[0]][current[1]] == 'T':
            print('STACK Solution:\n')
            print('STACK Choice Count: ' + str(stack_choice_count) + '\n')
            found = True
            break
        elif maze_solution[current[0]][current[1]] != '.':
            maze_solution[current[0]][current[1]] = '.'
            stack_choice_count += 1
            if maze_solution[current[0] - 1][current[1]] != ('*' or '.'):
                stack_path.push([current[0] - 1, current[1]])
            if maze_solution[current[0] + 1][current[1]] != ('*' or '.'):
                stack_path.push([current[0] + 1, current[1]])
            if maze_solution[current[0]][current[1] - 1] != ('*' or '.'):
                stack_path.push([current[0], current[1] - 1])    
            if maze_solution[current[0]][current[1] + 1] != ('*' or '.'):
                stack_path.push([current[0], current[1] + 1])      
    if len(stack_path) == 0:
        print('No solution found!')
        found = False   


    # prints solution, if exists
    if found:
        print(maze_solution)
        
        # queue implementation
        queue_choice_count = 0
        queue_path = LinkedQueue()
        queue_path.add(start)
        while len(queue_path) != 0:
            current = queue_path.pop()
            if queue_maze_solution[current[0]][current[1]] == 'T':
                print('QUEUE Solution:\n')
                print('QUEUE Choice Count: ' + str(queue_choice_count) + '\n')
                break
            elif queue_maze_solution[current[0]][current[1]] != '.':
                queue_maze_solution[current[0]][current[1]] = '.'
                queue_choice_count += 1
                if queue_maze_solution[current[0] - 1][current[1]] != ('*' or '.'):
                    queue_path.add([current[0] - 1, current[1]])
                if queue_maze_solution[current[0] + 1][current[1]] != ('*' or '.'):
                    queue_path.add([current[0] + 1, current[1]])
                if queue_maze_solution[current[0]][current[1] - 1] != ('*' or '.'):
                    queue_path.add([current[0], current[1] - 1])    
                if queue_maze_solution[current[0]][current[1] + 1] != ('*' or '.'):
                    queue_path.add([current[0], current[1] + 1])  
        
        # print queue, original, and outputs to file
        print(queue_maze_solution)
        
        print('Original maze:\n')
        print(maze)
    
        with open('solution.txt', 'w') as outfile:
            outfile.write('STACK Implementation: \nChoice Count: ' + str(stack_choice_count) + '\n\n')
            outfile.write(str(maze_solution) + '\n')
            outfile.write('------ \n\n')
            outfile.write('QUEUE Implementation: \nChoice Count: ' + str(queue_choice_count) + '\n\n')
            outfile.write(str(queue_maze_solution) + '\n')


if __name__ == '__main__': 
    main()
    
    