import os
def clear():
    os.system('cls' if os.name == 'nt' else 'clear') # clears screen above

def getValidInput(message, options=None, number=False):
    """
    Get valid input from the user.

    Parameters:
    - message: The message to display when asking for input.
    - options: A list of valid options.
    - input_type: The type to which the input should be converted if list of options is empty

    Returns:
    - The user's valid input.
    """
    while True:
        user_input = input(message).lower()  # Convert input to lowercase for case-insensitivity

        if number:
            try:
                # Try to convert the input to the specified type
                user_input = float(user_input)
                return user_input  # Return the valid input

            except ValueError:
                clear()
                print(f'Invalid input: {user_input}, please enter a number.')

        else:
            if user_input in options:
                return user_input  # Return the valid input
            clear()
            print(f"Invalid input: {user_input}. Please enter one of the following options: {', '.join(options)}")

