import numpy as np
from nistrng import *

def read_bits_from_file(filename):
    with open(filename, 'r') as file:
        bit_string = file.read().strip()
    return [int(bit) for bit in bit_string]
    
binary_sequence = read_bits_from_file("binary_output.txt")

eligible_battery: dict = check_eligibility_all_battery(np.array(binary_sequence), SP800_22R1A_BATTERY)
# Print the eligible tests
print("Eligible test from NIST-SP800-22r1a:")
for name in eligible_battery.keys():
    print("-" + name)
# Test the sequence on the eligible tests
results = run_all_battery(np.array(binary_sequence), eligible_battery, False)
# Print results one by one
print("Test results:")
for result, elapsed_time in results:
   if result.passed:
      print("- PASSED - score: " + str(np.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
   else:
      print("- FAILED - score: " + str(np.round(result.score, 3)) + " - " + result.name + " - elapsed time: " + str(elapsed_time) + " ms")
