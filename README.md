# Polynomial Rolling Code Estimator

A Python tool that tries to predict the next HEX code in a rolling code algorithm using Polynomial approximation and CRC &amp; binary verification.
This tool was made to reverse-engineer the rolling code that is shipped with the Explorer QRZ-1 handheld radio, which is seen upon trying to access the firmware unlock key-combo.

## Features

- Reads hexadecimal values from a file and converts them to decimal.
- Performs polynomial regression of varying degrees (from 1 to n-1, where n is the number of data points).
- Generates polynomial estimation functions and calculates their r^2 scores.
- Predicts the next decimal value using the polynomial functions.
- Interacts with the `reveng` tool using the subprocess module.
- Performs bitwise operations and checks on the predicted decimal values.

## Requirements

- Python 3.x
- numpy
- sklearn
- [reveng tool](https://sourceforge.net/projects/reveng/)
- [diffbits tool](https://github.com/samyk/samytools/blob/master/diffbits) by samyk

## Usage

1. Update the `hex_path` variable with the path to your file containing hexadecimal values. Ideally, this should be all the rolling codes you know of so far in order. The larger the sample size, the better the possibility of success.
2. Update the `reveng_path` variable with the path to your `reveng` executable.
3. Identify the CRC algorithm using reveng:
    - `reveng -w 8 -l -F -s <HEX samples separated by whitespace>`
    - The output (if successful) would look something like: `-w 8 -p 0x01 -i 0x36 -x 0x00 -v`
    - Use this as the `reveng_model` variable in the script
4. Identify the constant CRC HEX code:
    - `reveng <your CRC alg here> <any of your HEX code here>`
    - Using the model with any of your rolling codes should produce the same result.
    - One such example of the output of this command is `5a`.
    - Use this as the `crc_hex` variable in the script
5. Find common bits:
    - Use the diffbits Perl tool to find common bits with all your codes
    - This can be done by running `perl diffbits.pl <txt file with your Hex codes>`
    - The common bits are highlighted in green:
    - Change line #83 if statement to whatever bits your get that are similar
    - <img src="https://github.com/CyberPixel44/guess-poly-rolcode/assets/37630423/6bf176b2-1005-4fe5-8ed0-2d38c76c593a" height="300px">

5. Run the script using Python.

```bash
python estimator.py
```

## Output

The script prints the polynomial estimation functions, their corresponding r^2 scores, and the predicted decimal values.

## Note

This script assumes that the `reveng` tool is installed and accessible from the command line. Please ensure that you have the necessary permissions to execute the `reveng` tool.

## License

This project is licensed under the MIT License
