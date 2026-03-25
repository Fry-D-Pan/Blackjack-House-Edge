from autoPlay import autoPlaySetup
import os

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux (posix)
    else:
        _ = os.system('clear')

# Call the function to clear the screen

def main():
    clear_terminal()
    autoPlaySetup()
if __name__ == "__main__":
    main()

