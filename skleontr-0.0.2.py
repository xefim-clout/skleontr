"""
This file is part of Skleontr.

Skleontr is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Skleontr is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Skleontr.  If not, see <https://www.gnu.org/licenses/>.
"""



import curses
import os
import openai




def cmd_cleanup():     #clear last executed command from screen
    command_screen.clrtoeol()
    command_screen.move (1, 1)
    command_screen.clrtoeol()
    command_screen.border()


def opt_cleanup():     #clear last executed command from screen
    opt_screen.border()
    opt_screen.refresh()
    command_screen.move (1, 1)


def stat_log1 (status):   #update command line status - results and errors
    command_screen.move (2, 1)
    command_screen.addstr (status)


def stat_log2 (*params):
    global engine
    global response_length
    global temperature
    global top_p
    global freq_pen
    global pres_pen
    global best_of
    global stop_seq
    global start_text
    global restart_text
    global sens_comp
    global uns_comp

    opt_screen.move (1, 1)    #clear the options screen
    opt_screen.clrtobot()

    opt_screen.move (1, 1)
    opt_screen.addstr ('Engine: ' + str(engine))
    opt_screen.move (2, 1)
    opt_screen.addstr ('Response Length: ' + str(response_length))
    opt_screen.move (3, 1)
    opt_screen.addstr ('Temperature: ' + str(temperature))
    opt_screen.move (4, 1)
    opt_screen.addstr ('Top P: ' + str(top_p))
    opt_screen.move (5, 1)
    opt_screen.addstr ('Frequency penalty: ' + str(freq_pen))
    opt_screen.move (6, 1)
    opt_screen.addstr ('Presence penalty: ' + str(pres_pen))
    opt_screen.move (7, 1)
    opt_screen.addstr ('Best of: ' + str(best_of))
    opt_screen.move (8, 1)
    opt_screen.addstr ('Stop sequence: ' + str(stop_seq))
    opt_screen.move (9, 1)
    opt_screen.addstr ('Start text: ' + str(start_text))
    opt_screen.move (10, 1)
    opt_screen.addstr ('Restart text: ' + str(restart_text))
    opt_screen.move (11, 1)
    opt_screen.addstr ('Sensitive completions: ' + str(sens_comp))
    opt_screen.move (12, 1)
    opt_screen.addstr ('Unsafe completions: ' + str(uns_comp))


def stat_log (*params):    # UPDATE ALL WINDOWS after applying changes
    window_number = params[0]    #each status window has unique number
    stat_text = params[1]    #status text
    text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
    text_screen.clrtobot()
    draw_text (paragraph_cursor, text_cursor)

    if window_number == 1:         #output on command window
        stat_log1 (str(stat_text))
        cmd_cleanup()

    elif window_number == 2:       #output on options window
        stat_log2()
        opt_cleanup()

def data (*params):     #test function
    #screen.refresh()
    stat_log1 ('3465464677')


def printz (*params):
    command_screen.addstr (params[0] + '\n')  #adds newline to text


def exit (*params):
    global exit_flag
    command_screen.addstr ('exiting!.....')
    exit_flag = True


def read_file (filename):
    '''
    Splits words into separate entries by spaces ' '.
    [[word, word, word],[word, word],[word, word, word]]
    To get one space into list, separate it with spaces.
    '''
    global text_buffer
    global paragraph_cursor
    global text_cursor

    text_buffer = []

    with open (filename, 'r') as f:    #split newline character in a paragraph of its own
       for line in f:
          if line[0] == '.':    #if line begins with a dot '.' then append the whole line
              text_buffer.append ([line])
          else:
              text_buffer.append (line.split(' '))

    #for line in text_buffer:     #substitute empty elements with spaces ' '.
    #    for word in line:
    #        if word == '': line[line.index(word)] = ' '

    text_screen.move (0, 0)
    text_screen.clrtobot()

    paragraph_cursor = len (text_buffer) - 1
    text_cursor = len (text_buffer[-1]) - 2

    draw_text (paragraph_cursor, text_cursor)   #put cursor on last word of last paragraph
    stat_log (1, 'Opened file: ' + str(filename))


def draw_text (para_cursor, cursor, sel_cursor = 1):
    # separate text buffer into:
    # [text before selected] + [selected text] + [text after selected]
    # !!Needs heavy editing (cursor and spacing management)

    #cur_y, cur_x = text_screen.getyx()   #gets the values of the REAL curses cursor

    text_screen.move (0, 0)
    para_count = 0    #paragraph counter for displaying cursor(selected text) in correct position

    for paragraph in text_buffer:
        if len (paragraph[:cursor]) > 0:  #this eliminates printing one space at the beginning of text
            temp_text_1 = (' '.join(paragraph[:cursor]) + ' ').replace('\n ', '\n')
        else:
            temp_text_1 = ('').replace('\n ', '\n')

        #temp_text_1 = temp_text_1.lstrip()   #remove paragraph leading space EVEN MORE!

        if para_count == para_cursor:    #if current paragraph (being printed) is the selected paragraph
            if paragraph[cursor] == '\n':
                active_text = (' \n').replace('\n ', '\n')    #<------ !!getting rid of trailing space
            elif paragraph[cursor] == ' ':                    #        after a newline '\n'.
                active_text = (' ').replace('\n ', '\n')
            else:
                active_text = (' '.join (paragraph[cursor:cursor + sel_cursor])).replace('\n ', '\n')

            if paragraph[cursor] == '\n':
                temp_text_2 = ('').replace('\n ', '\n') #getting rid of new paragraph leading space HARDCORE
            else: temp_text_2 = (' ' + ' '.join (paragraph[cursor+sel_cursor:])).replace('\n ', '\n')

            text_screen.addstr (temp_text_1)
            text_screen.addstr (active_text, curses.A_STANDOUT)
            text_screen.addstr (temp_text_2)

        else:
            temp_text_2 = (' '.join (paragraph[cursor:])).replace('\n ', '\n')
            text_screen.addstr (temp_text_1 + temp_text_2)

        para_count += 1

    text_screen.refresh()

    command_screen.move (1, 1)   #move curses text cursor to command screen

    #text_screen.move (cur_y, cur_x)   #restore original curses cursor position

    #debug YX coordinates
    #screen.addstr (str(screen.getyx()[0]) + ' ' +  str(screen.getyx()[1]) + '\n')


def select (*params):
    global paragraph_cursor
    global text_cursor
    global select_cursor

    global text_buffer
    global copy_buffer

    stat_log1 ('Selection mode: [esc]exit, [c]copy, [d]delete, [space]select.')    #display status
    cmd_cleanup()

    while True:
        char = command_screen.getch()

        if char == curses.KEY_LEFT:
            #screen.addstr ("LEFT Key\n")
            select_cursor -= 1
            if select_cursor < 1: select_cursor = 1
            draw_text (paragraph_cursor, text_cursor, select_cursor)   #update screen

        elif char == curses.KEY_RIGHT:
            #screen.addstr ("RIGHT Key\n")
            select_cursor += 1
            if select_cursor > len (text_buffer[paragraph_cursor]) - text_cursor:
                select_cursor = len (text_buffer[paragraph_cursor]) - text_cursor
            draw_text (paragraph_cursor, text_cursor, select_cursor)   #update screen

        # if special command input char '/' is pressed
        elif char == 47:
            stat_log1 ('Another level deeper into command mode! PLS EXIT NAO!')
            cmd_cleanup()
            work()

        elif char == 99:    #character 'c'     #  <------ pull this out into a separate function
            copy_buffer = text_buffer[paragraph_cursor][text_cursor:text_cursor+select_cursor]
            stat_log1 ('Copied text!')
            cmd_cleanup()
            #print ('Buffer: ' + str((paragraph_cursor, text_cursor, select_cursor)))    #debug
            select_cursor = 1
            break

        elif char == 100:    #character 'd'
            delete()
            cmd_cleanup()
            select_cursor = 1
            break
            #print ('Buffer: ' + str(paragraph_cursor))   #debug

        # If ENTER is pressed      <-------- EDIT THIS FUNCTION!!
        elif char == 10:
            stat_log1 ('Back to command mode!')   #Return to command menu and keep track of selected text
            cmd_cleanup()              #so it can be edited with commands. do this with 'space' also
            select_cursor = 1
            break

        # If SPACE is pressed      <-------- EDIT THIS FUNCTION!!
        elif char == 32:
            stat_log1 ('Back to command mode!')
            cmd_cleanup()
            select_cursor = 1
            break

        #if 'ESC' is pressed
        elif char == 27:
            draw_text (paragraph_cursor, text_cursor, 1)    #deselect text
            stat_log (1, 'Command mode.......')
            cmd_cleanup()
            select_cursor = 1
            break

        else: pass


def paste (*params):
    global text_buffer
    global copy_buffer

    temp_cursor = text_cursor    # insert the copied text BEFORE selected word
    for word in copy_buffer:
        text_buffer[paragraph_cursor].insert (temp_cursor, word)
        temp_cursor += 1

    text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
    text_screen.clrtobot()
    draw_text (paragraph_cursor, text_cursor)
    stat_log (1, 'Pasted text.......')
    cmd_cleanup()


def insert (*params):
    global text_buffer
    global copy_buffer

    insert_buffer = str(params[0]).split(' ')[:]  # this inserts empty space if user inputs 3 spaces

    temp_cursor = text_cursor    # insert the copied text BEFORE selected word
    for word in insert_buffer:
        text_buffer[paragraph_cursor].insert (temp_cursor, word)
        temp_cursor += 1

    text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
    text_screen.clrtobot()
    draw_text (paragraph_cursor, text_cursor)
    stat_log1 ('Pasted text.......')
    cmd_cleanup()


def delete (*params):
    global text_buffer
    global text_cursor
    global paragraph_cursor
    global select_cursor

    if len (text_buffer[0]) == 0:
        text_buffer = [[' ']]
        text_cursor = 0
        paragraph_cursor = 0
        select_cursor = 1
        return  #if nothing to delete - don't do anything

    if len (text_buffer[paragraph_cursor]) < 2:
        text_buffer.pop (paragraph_cursor)    #delete empty paragraph (a newline symbol)
        text_cursor = 0
        if paragraph_cursor > len (text_buffer) - 1: paragraph_cursor = len (text_buffer) - 1
        if paragraph_cursor < 0: paragraph_cursor = 0

    else:
        for i in range (len(text_buffer[paragraph_cursor][text_cursor:text_cursor+select_cursor])):
            text_buffer[paragraph_cursor].pop(text_cursor)
        if paragraph_cursor > len (text_buffer) - 1: paragraph_cursor = len (text_buffer) - 1

    if len (text_buffer) == 0:
        text_buffer = [[' ']]
        paragraph_cursor = 0

    if text_cursor > len (text_buffer[paragraph_cursor]) - 1: text_cursor = len (text_buffer[paragraph_cursor]) - 1
    if text_cursor < 0: text_cursor = 0

    select_cursor = 1

    text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
    text_screen.clrtobot()
    draw_text (paragraph_cursor, text_cursor)
    stat_log (1, 'Deleted text.......')
    cmd_cleanup()


def change_text (new_text):    #   <-------- UPDATE THIS FUNCTION TO WORK WITH SELECTED TEXT
    global text_buffer
    global paragraph_cursor    # !! enter selection mode from command menu by pressing 'space'
    global text_cursor         # !! confirm selection also with 'space'(in the selection function)

    #if new_text == '\n':   #then split following text into a new paragraph
    old_text = text_buffer[paragraph_cursor][text_cursor]
    text_buffer[paragraph_cursor][text_cursor] = new_text
    text_screen.move (0, 0)
    text_screen.clrtobot()
    draw_text (paragraph_cursor, text_cursor)
    stat_log (1, 'Changed \"' + str(old_text) + '\" to \"' + str(new_text) + '\"')
    cmd_cleanup()


def change_text_interactive():
    stat_log (1, 'Editing the text. Press ENTER to save, ESC to exit.')
    cmd_cleanup()
    command_screen.refresh()

    inputt = ''

    curses.noecho()
    curses.curs_set (0)
    text_screen.keypad (False)

    old_text = text_buffer[paragraph_cursor][text_cursor]    #copy previous entry
    text_buffer[paragraph_cursor][text_cursor] = '???'   #custom input cursor hack

    text_screen.move (0, 0)
    text_screen.clrtobot()
    draw_text (paragraph_cursor, text_cursor)

    while True:
        charr = text_screen.getch()

        #if 'ESC' is pressed
        if charr == 27:
            inputt = old_text
            break

        if charr == 10: break

        inputt += chr (charr)
        text_buffer[paragraph_cursor][text_cursor] = inputt + '???'

        text_screen.move (0, 0)
        text_screen.clrtobot()
        draw_text (paragraph_cursor, text_cursor)

    text_buffer[paragraph_cursor][text_cursor] = inputt

    text_screen.move (0, 0)
    text_screen.clrtobot()
    draw_text (paragraph_cursor, text_cursor)
    stat_log (1, 'Changed \"' + str(old_text) + '\" to \"' + str(inputt) + '\"')
    cmd_cleanup()

    curses.echo()
    curses.curs_set (1)
    text_screen.keypad (True)


def line_break (*params):
    global text_buffer
    global paragraph_cursor
    global text_cursor
    global select_cursor

    temp_buffer = []

    temp_buffer = text_buffer[paragraph_cursor][text_cursor:]
    text_buffer[paragraph_cursor].insert (text_cursor, '\n')
    text_cursor += 1
    select_cursor = len (text_buffer[paragraph_cursor][text_cursor:])
    delete()

    paragraph_cursor += 1
    text_buffer.insert (paragraph_cursor, temp_buffer)

    text_cursor = 0
    select_cursor = 1

    text_screen.move (0, 0)    #  <------ !!correct this for curses pad type (scrolling) window
    text_screen.clrtobot()
    draw_text (paragraph_cursor, text_cursor)
    stat_log (1, 'New line break added.......')
    cmd_cleanup()


def save_buffer (*params):
    global text_buffer
    filename = str (params[0])

    with open (filename, 'w') as f:    #split newline character in a paragraph of its own
       for line in text_buffer:
          f.writelines (' '.join(line))

    stat_log (1, 'Saved to file: ' + filename)


def chat (*params):
    global text_buffer
    global paragraph_cursor
    global text_cursor
    global select_cursor

    chat_buffer = [[]]
    temp_buffer = text_buffer
    paragraph_cursor = 0
    text_cursor = 0

    promptt = 'The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?'

    chat_buffer = [[line + '\n'] for line in promptt.split('\n')]
    text_buffer = chat_buffer
    text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
    text_screen.clrtobot()
    draw_text (paragraph_cursor, text_cursor)
    stat_log (1, 'Chat mode with OpenAI..... Type /exit to return to editing mode.')
    cmd_cleanup()

    while True:
        inputt = command_screen.getstr()
        inputt = inputt.decode('UTF-8')

        if inputt == '/exit': break
        if inputt.split(' ')[0] == '/save':
            save_buffer (inputt.split(' ')[1])
            break

        inputt = 'Human: ' + inputt + '\nAI:'
        chat_buffer.append ([inputt])

        stat_log (1, 'Chat mode with OpenAI.........')
        cmd_cleanup()

        promptt = ''
        for line in chat_buffer:
            promptt += ''.join(line)

        response = openai.Completion.create(
            engine="davinci",
            prompt=promptt,
            temperature=0.8,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.1,
            presence_penalty=0.3,
            stop=["\n", " Human:", " AI:"])

        response_text = response ["choices"][0]["text"]
        chat_buffer.append ([response_text + '\n'])
        text_buffer = chat_buffer

        text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
        text_screen.clrtobot()
        draw_text (paragraph_cursor, text_cursor)


    text_buffer = temp_buffer    #return back to previous text buffer

    text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
    text_screen.clrtobot()
    draw_text (paragraph_cursor, text_cursor)
    stat_log (1, 'Back to command mode!')
    cmd_cleanup()


def work():
    #screen.addstr ('/')   # indicate the command character on screen

    #inputt = str(input())   #split input into command and params (if existing)
    inputt = command_screen.getstr()
    inputt = inputt.decode('UTF-8')

    command = inputt.split(' ')[0]
    #print (command)   #debug
    #input ('enter!.....')   #debug

    params = ' '.join(inputt.split(' ')[1:])
    #print (params)   #debug
    #input ('enter!.....')   #debug

    if command in actions:   #if command name in list, call according function
        actions[command](params)
        cmd_cleanup()
    else:
        stat_log (1, 'No such command!....')
        cmd_cleanup()



### Variables and data ###


#dictionary of text /commands associated with according function names
actions = {'data': data, 'print': printz, 'ed': change_text, 'edit': change_text, 'ch': change_text,
           'change': change_text, 'open': read_file, 'sel': select, 'select': select,
           'del': delete, 'delete': delete, 'in': insert, 'ins': insert, 'insert': insert, 'paste': paste,
           'chat': chat, 'save': save_buffer, 'exit': exit}


engine = 'davinci'
response_length = 64
temperature = 0.7
top_p = 1
freq_pen = 0
pres_pen = 0
best_of = 0
stop_seq = '\"\"\"'
start_text = 0
restart_text = 0
sens_comp = 0
uns_comp = 0


openai.api_key = os.getenv ("API_KEY")    # get api key from environmental variable

action_buffer = []   #action_buffer stores all command history
text_buffer = []     #current text is stored in text_buffer

exit_flag = False

#this is a sample text buffer with one paragraph
text_buffer = [['John', 'went', 'to', 'the', '"Skrong"', 'shop', 'to', 'buy', 'some', 'sauce.',
               'The', 'shop', 'was', 'closed,', 'so', 'John', 'bought', 'the', 'juice', 'on', 'the', 'street.']]

copy_buffer = []

paragraph_cursor = 0
text_cursor = 0
select_cursor = 1    #minimal word selection = 1, can't be 0!!



### Initialize screen and get the terminal screen dimensions
stdscr = curses.initscr()
height,width = stdscr.getmaxyx()
stdscr.clear()


# Init each window.
# Curses is max glitching the command screen size in Gnome virtual terminals!

command_screen = curses.newwin (height - 31, width - 31, height - 4, 30)
text_screen = curses.newwin (height - 4, width - 31, 0, 31)
opt_screen = curses.newwin (height, 30, 0, 0)


text_screen.refresh()

command_screen.border()
command_screen.refresh()

opt_screen.border()
opt_screen.refresh()

#turn screen scrolling on
command_screen.scrollok (True)
text_screen.scrollok (True)
opt_screen.scrollok (True)

# Turn off Echo
#curses.noecho()
#Instant Response
curses.cbreak()

#Use Special Keys
command_screen.keypad (True)  # <---- enable special keys for command window
text_screen.keypad (True)


draw_text (0, text_cursor)   #display the text buffer; paragraph = 0
read_file ('input_text.txt')    #!!debug
command_screen.move (1, 1)   #move command window cursor
stat_log (1, 'Welcome to Skleontr!!  Type /help to see the list of commands........')
command_screen.refresh()
stat_log (2, 'dummy text for now')  #implement parameter passing instead of dummy
opt_screen.refresh()


### Main loop ###

try:
    while True:
        char = command_screen.getch()
            #if 'ESC' is pressed
        if char == 27:
            command_screen.addstr ('Exiting......')
            break

        elif char == curses.KEY_UP:
            #screen.addstr ('UP')
            paragraph_cursor -= 1
            text_cursor = 0
            if paragraph_cursor < 0: paragraph_cursor = 0

            text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
            text_screen.clrtobot()
            draw_text (paragraph_cursor, text_cursor)   #update screen

        elif char == curses.KEY_DOWN:
            #screen.addstr ("DOWN")
            paragraph_cursor += 1
            text_cursor = 0
            if paragraph_cursor > len (text_buffer) - 1:
                paragraph_cursor = len (text_buffer) - 1
                text_cursor = len (text_buffer[paragraph_cursor]) - 1

            text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
            text_screen.clrtobot()
            draw_text (paragraph_cursor, text_cursor)   #update screen

        elif char == curses.KEY_LEFT:
            #screen.addstr ("LEFT")
            text_cursor -= 1

            if text_cursor < 0 and paragraph_cursor <= 0:
                text_cursor = 0
                paragraph_cursor = 0

            elif text_cursor < 0:
                paragraph_cursor -= 1
                text_cursor = len (text_buffer[paragraph_cursor]) - 1

            text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
            text_screen.clrtobot()
            draw_text (paragraph_cursor, text_cursor)   #update screen

        elif char == curses.KEY_RIGHT:
            #screen.addstr ("RIGHT")
            text_cursor += 1
            if text_cursor > len (text_buffer[paragraph_cursor]) - 1 and paragraph_cursor >= len (text_buffer) - 1:
                text_cursor = len (text_buffer[paragraph_cursor]) - 1
                paragraph_cursor = len (text_buffer) - 1

            elif text_cursor > len (text_buffer[paragraph_cursor]) - 1:
                paragraph_cursor += 1
                text_cursor = 0

            text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
            text_screen.clrtobot()
            draw_text (paragraph_cursor, text_cursor)   #update screen

        elif char == 99:    #character 'c'
            copy_buffer = text_buffer[paragraph_cursor][text_cursor:text_cursor+select_cursor]

            select_cursor = 1
            text_screen.move (0, 0)    #  <------ !!correct this for pad-style (scrolling) window
            text_screen.clrtobot()
            draw_text (paragraph_cursor, text_cursor)
            text_screen.refresh()

            stat_log (1, 'Copied text!')
            cmd_cleanup()
            #print ('Buffer: ' + str(paragraph_cursor))   #debug

        elif char == 100:    #character 'd' to delete word or selection
            delete()
            cmd_cleanup()
            select_cursor = 1
            #print ('Buffer: ' + str(paragraph_cursor))   #debug

        elif char == 101:    #character 'e' for "edit word"
            change_text_interactive()

        elif char == 118:    # if 'v' is pressed paste copy buffer
            paste()       # paste copied text

        elif char == 105:
            stat_log (1, 'Write the TEXT to insert!.....')
            input = command_screen.getstr()
            input = input.decode('UTF-8')
            insert (input)

        # if special command input char '/' is pressed
        elif char == 47:
            work()

        # If ENTER is pressed
        elif char == 10:
            line_break()
            #screen.addstr ("Enter.......")

        # If SPACE is pressed
        elif char == 32:
            #screen.addstr ("Enter.......")
            select()

        else:
            stat_log (1, 'Type / for command mode!')
            cmd_cleanup()

        #check exit_flag
        if exit_flag == True:
            break
finally:
    #When 'ESC' is pressed and program ends
    curses.nocbreak(); command_screen.keypad(0); curses.echo()
    curses.endwin()






