#!/usr/bin/python3

import os
import sys

# Define a function
def greet(name):
    """
    This function greets the user
    """
    print(f"Hello, {name}!")

# Main function
def main():
    """
    Main function
    """
    name = input("Enter your name: ")
    greet(name)

# Check if the script is being run directly
if __name__ == "__main__":
    main()
