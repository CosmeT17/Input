# Sensitive Input: Final Version
from readchar import readkey

# Print function
prt = lambda str : print(str, end = '', flush = True)

# Keys ----------------------------------------------------------------------------------------
ENTER = '\x0d' # (CTRL+M) '/r'
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
# ---------------------------------------------------------------------------------------------

# Variables -----------------------------------------------------------------------------------
var = {
    "i_stream": [],
    "line_num": 0,
    "max_len": 0, # Default: 100 character limit [with prompt] - 50 minimum
    "pos": 0,
    "prev_pos": 0,

    # For Testing Purposes --------------------------------------------------------------------
    "testing": False,
    "input_length": 0,
    "prev_input_length": 0,
    "lines_to_remove": 0,
    "chars_to_remove": 1
    # -----------------------------------------------------------------------------------------
}
# ---------------------------------------------------------------------------------------------

# Testing Functions ---------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------------------------

# Functions -----------------------------------------------------------------------------------
# Prints the current line from the current position to the end
def print_line_right(end_pos, deletion = False, deletion_amount = 1):
    line = var["i_stream"][var["line_num"]]
    
    for pos in range(var["pos"], len(line)):
        prt(line[pos])

    if deletion: prt(' ' * deletion_amount + LEFT * deletion_amount)
    var["pos"] = end_pos
    prt(LEFT * (len(line) - var["pos"]))

# Prints the current line from start_pos to the beginning
def print_line_left(start_pos):
    prt((LEFT + " " + LEFT) * (var["pos"] - start_pos - 1))

    for pos in range(start_pos, -1, -1):
        prt(LEFT + var["i_stream"][var["line_num"]][pos] + LEFT)

# Inserts the pressed character to the input stream and prints it to the screen
def print_char(keypress, wrapping):
    line_num = var["line_num"]
    i_stream = var["i_stream"]
    max_len = var["max_len"]
    pos = var["pos"]

    # No text wrapping - wring bell at limit
    if not wrapping:
        if pos == max_len:
            prt(BELL)
            return
    
    # Array Handling --------------------------------------------------------------------------
    try: i_stream[line_num].insert(pos, keypress)
    except IndexError: i_stream.append([keypress])

    for line_num in range(line_num, len(i_stream)):
        if len(i_stream[line_num]) > max_len:
            last_char = i_stream[line_num].pop()
            try: i_stream[line_num + 1].insert(0, last_char)
            except IndexError: i_stream.append([last_char])
    # -----------------------------------------------------------------------------------------

    # Print Handling --------------------------------------------------------------------------
    if pos == max_len:
        var["line_num"] += 1
        print_line_left(len(i_stream[var["line_num"]]) - 1)
        prt(RIGHT)
        var["pos"] = 1
    else: print_line_right(pos + 1)  
    # -----------------------------------------------------------------------------------------

# Deletes the character before position
def backspace():
    var["pos"] -= 1
    if var["pos"] != -1: prt(LEFT)
    delete_char()

# Deletes the character at position
def delete_char():
    if var["pos"] > -1:
        # Delete character at position, ring bell if deleting at empty spot
        try: var["i_stream"][var["line_num"]].pop(var["pos"])
        except IndexError:
            prt(BELL)
            return 

        delete = True
        for line_num in range(var["line_num"], len(var["i_stream"])):
            if len(var["i_stream"][line_num]) != 0:
                # Moving the characters left-wards
                try: 
                    var["i_stream"][line_num].append(var["i_stream"][line_num + 1].pop(0))
                    delete = False
                except IndexError: pass
            else:
                # The last line became empty remove it
                var["i_stream"].pop()
                # The input stream became empty, delete the only char from the console
                if len(var["i_stream"]) == 0: 
                    prt(' ' + LEFT)
                    return
                # The current line has been deleted, move to the previous line
                elif var["line_num"] ==  len(var["i_stream"]):
                    move_left()
                    return
        print_line_right(var["pos"], delete)
        
    # # Pressing backspace at position 0 not in 1st line, move to previous line
    elif var["line_num"] != 0:
        var["pos"] = 0
        move_left()

    # Pressing backspace at position 0 line 1, ring the bell
    else:
        var["pos"] = 0
        prt(BELL)

# Nicely formats the input stream on the input line after the user hits enter
def print_input():
    if len(var["i_stream"]) > 1:
        start_of_line()
        prt("".join(var["i_stream"][0]) + "...")
    print()

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
    input = ''
    for line in var["i_stream"]: input += "".join(line)
    return input
    
#  Places the cursor at the start of the line (CTRL+A)
def start_of_line():
    # Wring the bell if cursor already at the start
    if var["pos"]  == 0:
        prt(BELL)
    else:
        prt(LEFT * var["pos"])
        var["pos"] = 0

#  Places the cursor at the end of the line (CTRL+E)
def end_of_line():    
    if len(var["i_stream"]) != 0:
        # Wring the bell if cursor already at the end
        if var["pos"] == len(var["i_stream"][var["line_num"]]):
            prt(BELL)
        else:
            prt(RIGHT * (len(var["i_stream"][var["line_num"]]) - var["pos"]))
            var["pos"] = len(var["i_stream"][var["line_num"]])
    # Wring the bell if the input stream is empty
    else: prt(BELL)

#  Places the cursor at the start of the text (CTRL+Y)
def start_of_text():
    # If on first line, go to start_of_line()
    if var["line_num"] == 0: start_of_line()
    
    else:
        prt(LEFT * var["pos"])
        var["line_num"] = 0
        var["pos"] = 0
        print_line_right(0)

#  Places the cursor at the end of the text (CTRL+Z)
def end_of_text():
    # If on last line, go to end_of_line()
    if var["line_num"] == len(var["i_stream"]) - 1: end_of_line()

    else:
        prt(LEFT * var["pos"])
        var["line_num"] = len(var["i_stream"]) - 1
        var["pos"] = 0
        line_len = len(var["i_stream"][var["line_num"]])
        print_line_right(line_len, True, var["max_len"] - line_len)
        
# Deletes the input stream and clears the console (CTRL+X)
def clear_all():
    if len(var["i_stream"]) != 0:
        prt(LEFT * var["pos"])
        prt(' ' * len(var["i_stream"][var["line_num"]]))
        prt(LEFT * len(var["i_stream"][var["line_num"]]))

        # For Testing Purposes ----------------------------------------------------------------
        var["lines_to_remove"] = len(var["i_stream"])
        # -------------------------------------------------------------------------------------
        
        var["line_num"] = 0
        var["pos"] = 0
        
        var["i_stream"].clear()
    else: prt(BELL)

def clear_line():
    # Wring the bell if the input stream is empty
    if len(var["i_stream"]) == 0:
        prt(BELL)
        return
    
    # The current line is the first one
    if var["line_num"] == 0:
        # Clear the only single line
        if len(var["i_stream"]) == 1: clear_all()

        # There are more lines
        else:
            # Go to the next line
            end_of_line()
            move_right()

            # Remove the current line, which is now the previous line
            var["i_stream"].pop(var["line_num"] - 1)
            var["line_num"] = 0

    # The current line is not the first line
    else:
        # Go to the previous line
        start_of_line()
        move_left()
    
        # Remove the current line, which is now the next line
        var["i_stream"].pop(var["line_num"] + 1)

    # For Testing Purposes --------------------------------------------------------------------
    var["lines_to_remove"] += 1
    try: var["chars_to_remove"] += var["max_len"] - len(var["i_stream"][-1])
    except IndexError: pass
    # -----------------------------------------------------------------------------------------

# Deletes everything after the cursor, inclusive (CTRL+K) 
def delete_in_front():
    # Wring the bell if the input stream is empty or if the cursor is at the end of the last line
    if len(var["i_stream"]) == 0 or var["line_num"] == len(var["i_stream"]) - 1 and var["pos"] == len(var["i_stream"][var["line_num"]]):
        prt(BELL)

    else:
        # Remove all the lines in the input stream after the cursor
        for line_num in range(var["line_num"] + 1, len(var["i_stream"])): 
            var["i_stream"].pop()
            
            # For Testing Purposes ------------------------------------------------------------
            var["lines_to_remove"] += 1
            # ---------------------------------------------------------------------------------
    
        # Remove all the characters in the current line after the cursor (inclusive)
        chars_to_remove = range(var["pos"], len(var["i_stream"][var["line_num"]]))
        for char_num in chars_to_remove: 
            var["i_stream"][var["line_num"]].pop()
            prt(' ')
            
            # For Testing Purposes ------------------------------------------------------------
            var["chars_to_remove"] += 1
            # For Testing Purposes ------------------------------------------------------------
        prt(LEFT * len(chars_to_remove))
    
        # Remove the current line from input stream if no characters are left
        if len(var["i_stream"][var["line_num"]]) == 0:
            # For Testing Purposes ------------------------------------------------------------
            var["lines_to_remove"] += 1
            # For Testing Purposes ------------------------------------------------------------
            
            var["i_stream"].pop()
            if var["line_num"] != 0: move_left()

# Deletes everything before the cursor (CTRL+U) 
def delete_in_back():
    # Wring the bell if the input stream is empty or if the cursor is at the beginning of the first line
    if len(var["i_stream"]) == 0 or var["line_num"] == 0 and var["pos"] == 0:
        prt(BELL)

    else:
        # Remove all the lines in the input stream before the cursor
        for line_num in range(var["line_num"] - 1, -1, -1): 
            var["i_stream"].pop(line_num)
    
            # For Testing Purposes ------------------------------------------------------------
            var["lines_to_remove"] += 1
            # ---------------------------------------------------------------------------------
        var["line_num"] = 0
            
        # Remove all the characters in the input stream before the cursor
        chars_to_remove = range(0, var["pos"])
        for line_num in range(0, len(var["i_stream"])):
            for char_num in chars_to_remove:
                # Remove the characters before the cursor in the current line
                try: 
                    var["i_stream"][line_num].pop(0)
    
                # The last line was completely shifted back and does not exist anymore
                except IndexError: break
                
                try:
                    # If current line not last, append the characters in the next line to fill in the gaps
                    if line_num != len(var["i_stream"]) - 1:
                        var["i_stream"][line_num].append(var["i_stream"][line_num + 1][char_num])
    
                    # If there are no more characters left in the last line, remove it
                    elif len(var["i_stream"][line_num]) == 0:
                        var["i_stream"].pop()
    
                        # For Testing Purposes ----------------------------------------------
                        var["lines_to_remove"] += 1
                        # -------------------------------------------------------------------
    
                # There are no more characters left to append from the next line, remove it
                except IndexError:
                    var["i_stream"].pop()
                    var["lines_to_remove"] += 1

        # For Testing Purposes ----------------------------------------------------------------
        var["chars_to_remove"] += var["max_len"] - len(var["i_stream"][-1])
        # -------------------------------------------------------------------------------------
        
        # Updating the console
        if var["pos"] != 0:
            var["pos"] = 0
            prt(LEFT * len(chars_to_remove))
            print_line_right(0, True, var["max_len"] - len(var["i_stream"][0]))

# Moves the cursor to the right, changes to the next line when needed (RIGHT ARROW)
def move_right():
    try:
        # Move the cursor to the right
        if var["pos"] != len(var["i_stream"][var["line_num"]]):
            prt(RIGHT)
            var["pos"] += 1

        # Move to the next line
        elif var["line_num"] != len(var["i_stream"]) - 1:
            var["line_num"] += 1
            print_line_left(len(var["i_stream"][var["line_num"]]) - 1)
            var["pos"] = 0
            
        # Wring the bell if the cursor is at the right-most position
        else:
            prt(BELL)

    # Wring the bell if the input stream is empty
    except IndexError:
        prt(BELL)

# Moves the cursor to the left, changes to the previous line when needed (LEFT ARROW)
def move_left():
    # Move the cursor to the left
    if var["pos"] != 0:
        prt(LEFT)
        var["pos"] -= 1

    # Move to the previous line
    elif var["line_num"] != 0:
        var["line_num"] -= 1
        print_line_right(var["max_len"])
    
    # Wring the bell if the cursor is at the left-most position
    else:
        prt(BELL)

# Changes to the next line if possible (DOWN ARROW)
def next_line():
    if var["line_num"] < len(var["i_stream"]) - 1:
        prev_pos = var["pos"]
        
        end_of_line()
        move_right()

        # Place the cursor where it was previously if possible
        if prev_pos <= len(var["i_stream"][var["line_num"]]):
            prt(RIGHT * prev_pos)
            var["pos"] = prev_pos
            
        # Place the cursor at the end of the line
        else:
            var["prev_pos"] = prev_pos
            end_of_line()
        
    # Wring the bell if on the last line
    else:
        prt(BELL)
        var["prev_pos"] = 0

# Changes to the previous line if possible, remembers the previous position (UP ARROW)
def previous_line():
    if var["line_num"] != 0:
        prev_pos = var["prev_pos"] if var["prev_pos"] != 0 else var["pos"]
        
        start_of_line()
        move_left()

        # Place the cursor where it was previously
        prt(LEFT * (var["max_len"] - prev_pos))
        var["pos"] = prev_pos
        
    # Wring the bell if on the first line
    else:
        prt(BELL)
        
# Raises a KeyboardInterrupt (CTRL+C)
def keyboard_interrupt():
    prt(BELL)
    raise KeyboardInterrupt()

# Raises an EOFError if input stream is empty (CTRL+D)
def eof_error():
    if len(var["i_stream"]) == 0:
        prt(BELL)
        raise EOFError()
    else: delete_char()
# ---------------------------------------------------------------------------------------------

# Dictionary that maps special keypresses to the appropriate function
key_func = {
    ENTER: lambda: print_input(),
    DELETE: lambda: delete_char(),
    BACKSPACE: lambda: backspace(),
    RIGHT: lambda: move_right(),
    LEFT: lambda: move_left(),
    DOWN: lambda: next_line(),
    UP: lambda: previous_line(),
    START_OF_LINE: lambda: start_of_line(),
    END_OF_LINE: lambda: end_of_line(),
    START_OF_TEXT: lambda: start_of_text(),
    END_OF_TEXT: lambda: end_of_text(),
    CLEAR_ALL: lambda: clear_all(),
    CLEAR_LINE: lambda: clear_line(),
    DELETE_IN_FRONT: lambda: delete_in_front(),
    DELETE_IN_BACK: lambda: delete_in_back(),
    BELL: lambda: prt(BELL),
    KEYBOARD_INTERRUPT: lambda: keyboard_interrupt(),

    # Alternate keypresses
    ALTERNATE_ENTER: lambda: print_input(),
    ALTERNATE_BACKSPACE: lambda: backspace(),
    ALTERNATE_DELETE: lambda: eof_error(),
    ALTERNATE_RIGHT: lambda: move_right(),
    ALTERNATE_LEFT: lambda: move_left(),
}

# Main Function -------------------------------------------------------------------------------
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
        # For Testing Purposes ----------------------------------------------------------------
        var["testing"] = testing
        if testing: var["input_length"] = test_print(prompt)
        # -------------------------------------------------------------------------------------
        keypress = readkey()
        
        if keypress in key_func:
            key_func[keypress]()
            
            if keypress == ENTER or keypress == ALTERNATE_ENTER:
                return get_input_str()

            if keypress != UP and keypress != DOWN:
                var["prev_pos"] = 0
        
        elif keypress.isprintable():
            var["prev_pos"] = 0
            print_char(keypress, wrapping)
# ---------------------------------------------------------------------------------------------
    
# TEST ----------------------------------------------------------------------------------------
test = sensitive_input("Prompt: ",  10, wrapping = True, testing = True)
print(test)
# ---------------------------------------------------------------------------------------------

# TO DO:
#  * KeybaordInterrupt -- raise KeyboardInterrupt()
#  * BEEP
#  * print_input()
#  * get_input_str():
#  * delete_char()
#  * clear_all()
#  * fix test_print() when printing stream after deletion
#  * start_of_text()
#  * end_of_text()
#  * delete_in_front()
#  * delete_in_back()
#  * next_line()
#  * previous_line()

#  * clear_line() : TEST
    
#  * fix tabs
#  * paste from clipboard/ copy?
#  * remember previous inputs
#  * add escape character sequence
#  * add text box option, delete testing mode
#  * fix input lag by recording how long it takes between keypresses
#  * test out more escape routes
#  * testing
#
#  * Final Touches -> Done!!!!! YAY
