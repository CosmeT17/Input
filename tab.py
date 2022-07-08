# Input: Final Version
from readchar import readkey
from math import ceil

# Keys ----------------------------------------------------------------------------------------
ENTER = '\x0d' # (CTRL+M) '/r'
TAB = '\x09' # Horizontal Tab (CTRL+I) '/t'
BACKSPACE = '\x7f' # Backspace (CTRL+8)
DELETE = "\x1b\x5b\x33\x7e" # "\x1b[3~"
LEFT = "\x1b\x5b\x44" # Left Arrow "\x1b[D"
RIGHT = "\x1b\x5b\x43" # Right Arrow "\x1b[C"
UP = "\x1b\x5b\x41" # Up Arrow "\x1b[A"
DOWN = "\x1b\x5b\x42" # Down Arrow "\x1b[B"
START_OF_LINE = '\x01' # (CTRL+A)
END_OF_LINE = '\x05' # (CTRL+E)
START_OF_TEXT = '\x19' # End of Medium (CTRL+Y)
END_OF_TEXT = '\x1a' # Substitute Character (CTRL+Z)
CLEAR_ALL = '\x18' # Cancel (CTRL+X)
CLEAR_LINE = '\x0c' # Form Feed (CTRL+L) '/f'
DELETE_IN_FRONT = '\x0b' # Vertical Tab (CTRL+k)
DELETE_IN_BACK = '\x15' # Negative Acknowledge (CTRL+U)
BELL = '\x07' # Ring terminal Bell (CTRL+G)
KEYBOARD_INTERRUPT = '\x03' # End of Text (CTRL+C)

# Alternate keypresses
ALTERNATE_ENTER = '\x0a' # Line Feed (CTRL+J) '\n'
ALTERNATE_BACKSPACE = '\x08' # Backspace (CTRL+H) '/b'
ALTERNATE_DELETE = '\x04' # End of Transmission (CTRL+D)
ALTERNATE_LEFT = '\x02' # Start of Text (CTRL+B)
ALTERNATE_RIGHT = '\x06' # Acknowledge (CTRL+F)

# Keeps track of tab spaces
TAB_SPACE = '\x13' # Device Control 1 (CTRL+S)
# ---------------------------------------------------------------------------------------------------------

# Variables -----------------------------------------------------------------------------------------------
var = {
    "i_stream": [],
    "line_num": 0,
    "max_len": 0, # Default: 100 character limit [with prompt] - 50 minimum
    "prev_pos": 0,
    "pos": 0,
    "tab_len": 4,
    
    # For Testing Purposes --------------------------------------------------------------------------------
    "testing": False,
    "input_length": 0,
    "prev_input_length": 0,
    "lines_to_remove": 0,
    "chars_to_remove": 1
    # -----------------------------------------------------------------------------------------------------
}
# ---------------------------------------------------------------------------------------------------------

# Auxiliary Functions -------------------------------------------------------------------------------------
# Print function
def prt(str):
    for char in str:
        if char != TAB_SPACE: print(char, end = '', flush = True)
        else: print('_', end = '', flush = True)

# Prints the current line from the current position to the end
def print_line_right(end_pos, deletion = False, deletion_amount = 1): 
    for pos in range(var["pos"], len(var["i_stream"][var["line_num"]])):
        prt(var["i_stream"][var["line_num"]][pos])

    if deletion: prt(' ' * deletion_amount + LEFT * deletion_amount)
    var["pos"] = end_pos
    prt(LEFT * (len(var["i_stream"][var["line_num"]]) - var["pos"]))

# Prints the current line from start_pos to the beginning
def print_line_left(start_pos):
    prt((LEFT + " " + LEFT) * (var["pos"] - start_pos - 1))

    for pos in range(start_pos, -1, -1):
        prt(LEFT + var["i_stream"][var["line_num"]][pos] + LEFT)

# Converts the input stream into a single string
def get_input_str():
    # For Testing Purposes --------------------------------------------------------------------
    # Deleting the testing info
    if var["testing"]:
        print()
        for i in range(4): print(' ' * (15 + len(str(var["input_length"]))))
        print()
        for line in var["i_stream"]: print(' ' * (len(line) + 2))
        prt(UP * (len(var["i_stream"]) + 6))
    # -----------------------------------------------------------------------------------------

    # Making the input stream a single string
    tab_space_skips = 0
    input = ''
    for line in var["i_stream"]: 
        for char in line:
            if char != TAB_SPACE: input += char

            elif tab_space_skips == 0:
                input += TAB
                tab_space_skips = var["tab_len"] - 1
            
            else: tab_space_skips -= 1
    return input
# ---------------------------------------------------------------------------------------------------------

# Functions -----------------------------------------------------------------------------------------------
# Inserts the pressed character to the input stream and prints it to the screen
def print_char(keypress, wrapping):
    # No text wrapping - wring bell at limit
    if not wrapping:
        if var["pos"] == var["max_len"] or (keypress == TAB and var["max_len"] - var["pos"] < var["tab_len"]):
            prt(BELL)
            return

    if keypress != TAB:
        # Array Handling --------------------------------------------------------------------------------------
        try: var["i_stream"][var["line_num"]].insert(var["pos"], keypress)
        except IndexError: var["i_stream"].append([keypress])
    
        for line_num in range(var["line_num"], len(var["i_stream"])):
            if len(var["i_stream"][line_num]) > var["max_len"]:
                last_char = var["i_stream"][line_num].pop()
                try: var["i_stream"][line_num + 1].insert(0, last_char)
                except IndexError: var["i_stream"].append([last_char])
        # -----------------------------------------------------------------------------------------------------
    
        # Print Handling --------------------------------------------------------------------------------------
        if var["pos"] == var["max_len"]:
            var["line_num"] += 1
            print_line_left(len(var["i_stream"][var["line_num"]]) - 1)
            prt(RIGHT)
            var["pos"] = 1
        else: print_line_right(var["pos"] + 1)  
        # -----------------------------------------------------------------------------------------------------
    # Tab was pressed, insert four tab spaces
    else:
        for tab_space in range(var["tab_len"]): print_char(TAB_SPACE, wrapping)

# Moves the cursor to the left, changes to the previous line when needed (LEFT ARROW)
def move_left():
    # Not at the beginning of the line
    if var["pos"] != 0:
        # Move the cursor to the left
        if var["i_stream"][var["line_num"]][var["pos"] - 1] != TAB_SPACE:
            prt(LEFT)
            var["pos"] -= 1

        # Skip to the beginning of the tab
        elif var["pos"] >= var["tab_len"]:
            prt(LEFT * var["tab_len"])
            var["pos"] -= var["tab_len"]

        # Need to go to previous lines
        else:
            tab_spaces_left_over = (var["tab_len"] - var["pos"])
            lines_to_skip = ceil(tab_spaces_left_over / var["max_len"])
            tab_spaces_remainder = tab_spaces_left_over % var["max_len"]
            if tab_spaces_remainder == 0: tab_spaces_remainder = var["max_len"]
                
            prt(LEFT * var["pos"])
            var["pos"] = 0
            var["line_num"] -= lines_to_skip
            print_line_right(var["max_len"] - tab_spaces_remainder)
            
    # Move to the previous line
    elif var["line_num"] != 0:
        var["line_num"] -= 1
        print_line_right(var["max_len"])
    
    # Wring the bell if the cursor is at the left-most position
    else:
        prt(BELL)

# Moves the cursor to the right, changes to the next line when needed (RIGHT ARROW)
def move_right():
    try:
        # Not at the end of the line
        if var["pos"] != len(var["i_stream"][var["line_num"]]):
            # Move the cursor to the right
            if var["i_stream"][var["line_num"]][var["pos"]] != TAB_SPACE:
                prt(RIGHT)
                var["pos"] += 1
    
            # Skip to the end of the tab
            elif var["max_len"] - var["pos"] >= var["tab_len"]:
                prt(RIGHT * var["tab_len"])
                var["pos"] += var["tab_len"]

             # Need to go to previous lines
            else:
                tab_spaces_in_line = var["max_len"] - var["pos"]
                tab_spaces_left_over = var["tab_len"] - tab_spaces_in_line
                lines_to_skip = ceil(tab_spaces_left_over / var["max_len"])
                tab_spaces_remainder = tab_spaces_left_over % var["max_len"]
                if tab_spaces_remainder == 0: tab_spaces_remainder = var["max_len"]
                
                var["line_num"] += lines_to_skip
                prt(RIGHT * tab_spaces_in_line)
                var["pos"] += tab_spaces_in_line
                print_line_left(len(var["i_stream"][var["line_num"]]) - 1)
                prt(RIGHT * tab_spaces_remainder)
                var["pos"] = tab_spaces_remainder
        
        # Move to the next line
        elif var["line_num"] != len(var["i_stream"]) - 1:
            var["line_num"] += 1
            print_line_left(len(var["i_stream"][var["line_num"]]) - 1)
            var["pos"] = 0
                
        # Wring the bell if the cursor is at the right-most position
        else: prt(BELL)

    # # Wring the bell if the input stream is empty
    except IndexError:
        prt(BELL)

#  Places the cursor at the start of the line (CTRL+A)
def start_of_line():
    # Wring the bell if cursor already at the start
    if var["pos"]  == 0:
        prt(BELL)

    # First char in the line is not a tab, go to the start
    elif var["i_stream"][var["line_num"]][0] != TAB_SPACE:
        prt(LEFT * var["pos"])
        var["pos"] = 0

    # First char is part of a tab
    else:
        # Count how many tab spaces there are before the cursor and the remainder
        num_tab_spaces = 1
        for char in var["i_stream"][var["line_num"]][1:var["pos"]]: 
            if char == TAB_SPACE: num_tab_spaces += 1
            else: break
        tab_spaces_remainder = num_tab_spaces % var["tab_len"]
                
        move_distance = var["pos"] - tab_spaces_remainder
        # Go to the beginning/end of the tab
        if move_distance != 0:
            prt(LEFT * move_distance)
            var["pos"] = tab_spaces_remainder
            
        # Cannot move left, wring bell
        else: prt(BELL)
            
# Nicely formats the input stream on the input line after the user hits enter
def print_input():
    if len(var["i_stream"]) > 1:
        prt(LEFT * var["pos"])
        var["pos"] = 0
        prt("".join(var["i_stream"][0]) + "...")
    print()
# ---------------------------------------------------------------------------------------------------------

# Testing Functions ---------------------------------------------------------------------------------------
# Prints useful information and the input stream
def test_print(prompt):
    # Calculating extra variables
    length = len(var["i_stream"][var["line_num"]]) if len(var["i_stream"]) !=  0  else  0
    input_length = 0 
    for line in var["i_stream"]: input_length += len(line)

    # Printing variables
    print(f"\n\nLine: {var['line_num'] + 1}/{len(var['i_stream'])}{' '  * (len(str(len(var['i_stream']))) - len(str(var['line_num'] + 1)))}")
    print(f"Position: {var['pos']}/{var['max_len']}{' '  * (len(str(var['max_len'])) - len(str(var['pos'])))}")
    print(f"Line Length: {length}{' ' *  (len(str(var['max_len'])) - len(str(length)))}")
    print(f"Input Length: {input_length}{' ' * (len(str(var['prev_input_length'])) - len(str(input_length)))}\n")

    # Print input stream
    for line_num in range(len(var["i_stream"])):
        prt('[')
        for char in var["i_stream"][line_num]:
            prt(char)
        if line_num == len(var["i_stream"]) - 1: 
            prt(' ' * var["chars_to_remove"] + LEFT * var["chars_to_remove"])
            var["chars_to_remove"] = 1
        prt('] \n')

    # Deleting the input stream from console if the input stream is cleared
    prt((' ' * var["max_len"] + '  \n') * var["lines_to_remove"] + "   \n" + UP * (var["lines_to_remove"]))
    var["lines_to_remove"] = 0
    
    # Returning to input
    prt((len(var["i_stream"]) + 8) * UP) # 7 -> 8
    prt(RIGHT * (len(prompt) + var["pos"]))
    var["prev_input_length"]  = input_length
    return input_length
# ---------------------------------------------------------------------------------------------------------
     
# Dictionary that maps special keypresses to the appropriate function
key_func = {
    ENTER: lambda: print_input(),
    LEFT: lambda: move_left(),
    RIGHT: lambda: move_right(),
    START_OF_LINE: lambda: start_of_line(),
}

# Main Function -------------------------------------------------------------------------------------------
def sensitive_input(prompt = "", max_length = 0, wrapping = True, testing = False):
    # Printing the prompt
    prt(prompt)

    # Reseting the variables
    if max_length <= 0: var["max_len"] = 100 - len(prompt) if len(prompt) < 50 else 50
    else: var["max_len"] = max_length
    var["i_stream"].clear()
    var["line_num"] = 0
    var["pos"] = 0

    while True:
        # For Testing Purposes ----------------------------------------------------------------------------
        var["testing"] = testing
        if testing: var["input_length"] = test_print(prompt)
        # -------------------------------------------------------------------------------------------------
        keypress = readkey()
        
        if keypress in key_func:
            key_func[keypress]()
            
            if keypress == ENTER or keypress == ALTERNATE_ENTER:
                return get_input_str()

            # if keypress != UP and keypress != DOWN:
            #     var["prev_pos"] = 0
        
        elif keypress.isprintable() or keypress == TAB:
            # var["prev_pos"] = 0
            print_char(keypress, wrapping)
# ---------------------------------------------------------------------------------------------------------
    
# TEST ----------------------------------------------------------------------------------------------------
test = sensitive_input("Prompt: ",  10, wrapping = True, testing = True)
print([test])
# ---------------------------------------------------------------------------------------------------------
