import os
from datetime import datetime
def clear():
    os.system('cls' if os.name == 'nt' else 'clear') # clears screen above

def getValidInput(message, options=None, decimal=False, integer=False, intRange=None, isDate=False, caseSensitive=False):
    """
    Get valid input from the user.

    Parameters:
    - message: The message to display when asking for input.
    - options: A list of valid options.
    - decimal: Boolean if number is a float
    - integer: Boolean if number is an integer
    - intRange: range for integer to be within, inclusive


    Returns:
    - The user's valid input.
    """
    while True:
        if caseSensitive:
            user_input = input(message)
        else:
            user_input = input(message).lower()  # Convert input to lowercase for case-insensitivity
        
        if decimal: # if we are parsing a float
            try:
                user_input = float(user_input)
                return user_input

            except ValueError:
                clear()
                print(f'Invalid input: {user_input}, please enter a number.\n')     
        elif integer and intRange is None: # if we are parsing an integer without an integer range
            try:
                user_input = int(user_input)
                return user_input
            except ValueError:
                clear()
                print(f'Invalid input: {user_input}, please enter an integer.\n')
        elif integer and intRange is not None: # if we are parsing an integer with an integer range
            try:
                user_input = int(user_input)
                if user_input in range(intRange[0], intRange[1] + 1):
                    return user_input
                else:
                    clear()
                    print(f'Invalid input, please enter an integer in the range {", ".join([str(x) for x in intRange])}\n')
            except ValueError:
                clear()
                print(f'Invalid input: {user_input}, please enter an integer.\n')
        elif isDate: # if we are parsing a date
                try:
                    input_date = datetime.strptime(user_input, '%m-%d-%Y').date()
                    current_date = datetime.now().date()

                    # Check if the input date is after today's date
                    if input_date > current_date:
                        return user_input
                    else:
                        clear()
                        print("Please enter a date that is after today.\n")
                except ValueError:
                    clear()
                    print("Invalid date format. Please enter a date in the format MM-DD-YYYY.\n")
        else: # if we are making sure the string is in the list of options
            if user_input in options:
                return user_input  # Return the valid input
            clear()
            print(f"Invalid input: {user_input}. Please enter one of the following options: {', '.join(options)}\n")

