
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]


cols_rev = cols[::-1]
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
diag_unit1 = [[rows[i]+cols[i] for i in range(len(rows))]]
diag_unit2 = [[rows[i]+cols_rev[i] for i in range(len(rows))]]


square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
is_diagnoal = 1
if is_diagnoal:
    unitlist = row_units + col_units + square_units + diag_unit1 + diag_unit2
else:
    unitlist = row_units + col_units + square_units
boxes = cross(rows, cols)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # Pick out all possible naked twins box that has only 2 values
    nt_candiadate = [box for box in values.keys() if len(values[box]) == 2]
    # Search all peer of naked twins candidate that has the same value 
    naked_twins_list = [[box1, box2] for box1 in nt_candiadate for box2 in peers[box1] if values[box1] == values[box2]]

    # loop naked twins 
    for nakedTwins in naked_twins_list:
        nt_val = values[nakedTwins[0]]
        # check each unit
        for unit in unitlist:
            if all(x in unit for x in nakedTwins):
                # remove naked twins from the units
                unit_peer = [box for box in unit if box not in nakedTwins]
                # remove the value of naked twin from peers in the unit
                for peer in unit_peer:
                    digit = values[peer]
                    if len(digit) > 1:
                        for value in nt_val:
                            assign_value(values, peer, values[peer].replace(value, ''))
    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    
    assert len(grid) == 81
    values=[]
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        else:
            values.append(c)
    
    dictionary = dict(zip(boxes, values))
    return dictionary

def display(values):
    """
    Display the values as a 2-D grid.
    
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    find out all box that has only value and remove the value from its peerss
    
    Args:
        values(dict): The sudoku in dictionary form
    return:
        values(dict): The sudoku in dictionary form
    """
    solved_boxes = [box for box in values.keys() if len(values[box])== 1]
    
    for box in solved_boxes:
        digit = values[box]
        for peer in peers[box]:
            new_value = values[peer].replace(digit, '')
            assign_value(values, peer, new_value)
    
    if len([box for box in values.keys() if len(values[box]) == 0]):
        zero_value = [box for box in values.keys() if len(values[box]) == 0]
        print("elim box with zero value: {}".format(zero_value))
    
    display(values)
    return values

def only_choice(values):
    """
    Replace the value of box if this box has an unique value in unit
    
    Args:
        values(dict): The sudoku in dictionary form
    return:
        values(dict): The sudoku in dictionary form
    """
    
    print("\n[only_choice function]")
    for unit in unitlist:

        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)

    if len([box for box in values.keys() if len(values[box]) == 0]):
            zero_value = [box for box in values.keys() if len(values[box]) == 0]
            print("only box with zero value: {}".format(zero_value))
    
    display(values)
    return values

def reduce_puzzle(values):
    """
    Perform eliminate, only_choice and naked_twins to solve the puzzle

    Args:
        values(dict): The sudoku in dictionary form
    return:
        values(dict): The sudoku in dictionary form
    """

    print("[reduct_puzzle function]")
    stalled = False
    while(not stalled):
        solved_value_before = [box for box in values.keys() if len(values[box]) == 1]
        
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_value_after = [box for box in values.keys() if len(values[box]) == 1]
        
        stalled = solved_value_before == solved_value_after
        
        if len([box for box in values.keys() if len(values[box]) == 0]):
            zero_value = [box for box in values.keys() if len(values[box]) == 0]
            print("box with zero value: {}".format(zero_value))                                       
            return False
    
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    """
    Args:
        values(dict): The sudoku in dictionary form
    return:
        values(dict): The sudoku in dictionary form
    """

    print("\n[search function]")
    


    values = reduce_puzzle(values)
    if values is False:
        print("return False")
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        print("Solved")
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        # print("\n\ntry {} of value[{}]".format(value, s))
        new_sudoku = values.copy()
        new_sudoku[s] = value
        print("[search]")
        display(new_sudoku)

        attempt = search(new_sudoku)
        if attempt:
            print("attempt")
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
