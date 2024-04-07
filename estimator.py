import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import subprocess

hex_path = "" # Path to the file containing the hex values as a txt. Use double \\ for windows path
reveng_path = "" # Path to the reveng executable. Use double \\ for windows path
reveng_model = "-w 8 -p 0x01 -i 0x36 -x 0x00 -v" # Model for the reveng command
crc_hex = b'5a' # CRC hex value to match

# Read hex values from file
with open(hex_path, 'r') as file:
    hex_list = [line.strip() for line in file]

# Convert hexes to decimal
decimal_list = [int(hex_value, 16) for hex_value in hex_list]

# Generate x values starting from 1
x_values = np.arange(1, len(decimal_list) + 1).reshape(-1, 1)

# Create a list to store the polynomial estimation functions
polynomial_functions = []

r_dict = {}

# Loop through degrees from 1 to 7
for degree in range(1, len(decimal_list) - 1):
    # Create a polynomial regression model
    model = np.polyfit(x_values.flatten(), decimal_list, degree)

    # Get the coefficients of the polynomial
    coefficients = model.tolist()

    # Create the polynomial estimation function
    polynomial_function = f"y = {coefficients[-1]}"

    for i in range(degree, 0, -1):
        polynomial_function += f" + {coefficients[degree - i]}x^{i}"

    # Append the polynomial estimation function to the list
    polynomial_functions.append(polynomial_function)

    # Predict the y values using the model
    y_values = np.polyval(model, x_values.flatten())

    # Calculate the r^2 value
    r2 = r2_score(decimal_list, y_values)

    # Print the decimal values, polynomial estimation function, and r^2 value
    print("-----------------------------------------------------------------")
    print(f"Degree {degree}:")
    print("Decimal values:", decimal_list)
    print("Polynomial estimation function:", polynomial_function)
    print("r^2 value:", r2)
    print()

    # Store the r^2 value in a dictionary
    r_dict[degree] = [r2, polynomial_function]
    matching_decimals = []

    # Loop through the polynomial functions
    for polynomial_function in polynomial_functions:
        # Evaluate the polynomial function for the next x value
        next_x = len(decimal_list) + 1
        next_decimal = np.polyval(np.poly1d(np.polyfit(x_values.flatten(), decimal_list, len(polynomial_function.split('x')) - 1)), next_x)

        # Check if the decimal has 10 digits when rounded
        if len(str(round(next_decimal))) == 10:
            matching_decimals.append((next_decimal, polynomial_function))

    # Sort the matching decimals in descending order of r^2 value
    matching_decimals.sort(reverse=True)

# Print the matching decimals
for decimal, polynomial_function in matching_decimals:
    rounded_decimal = round(decimal)
    hex_num = hex(rounded_decimal)[2:].upper()
    command = f'{reveng_path} {reveng_model} {hex_num}'
    output = subprocess.check_output(command, shell=True)
    
    # Check if the 1st and 16th bit of the rounded decimal in binary are 1
    binary = bin(int(hex_num, 16))[2:].zfill(16)
    if binary[0] == '1' and binary[16] == '1': # Edit statement to match the desired bits that match from using diffbits tool
        if output.strip() == crc_hex:
            print(f"Output of command for decimal {rounded_decimal} is equal to 5a")
        else:
            # Keep adding/subtracting integers from the decimal until a match is found
            while output.strip() != crc_hex and binary[0] != '1' and binary[16] != '1':
                rounded_decimal += 1  # or rounded_decimal -= 1 for subtraction
                binary = bin(int(hex_num, 16))[2:].zfill(16)
                hex_num = hex(rounded_decimal)[2:].upper()
                command = f'{reveng_path} {reveng_model} {hex_num}'
                output = subprocess.check_output(command, shell=True)
            if len(binary) == 32:
                print(f"Output of command for decimal {rounded_decimal} is equal to {hex_num} with binary {binary}")