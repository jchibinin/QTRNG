import numpy as np
from scipy import stats

def read_bits_from_file(filename):
    with open(filename, 'r') as file:
        bit_string = file.read().strip()
    return [int(bit) for bit in bit_string]

def frequency_test(bits, significance_level=0.01):
    n = len(bits)
    ones_count = sum(bits)
    zeros_count = n - ones_count
    
    chi_square = ((ones_count - n/2)**2 + (zeros_count - n/2)**2)/(n/2)
    p_value = 1 - stats.chi2.cdf(chi_square, 1)
    
    return p_value > significance_level

def runs_test(bits, significance_level=0.01):
    n = len(bits)
    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i-1]:
            runs += 1
    
    expected_runs = (2*n - 1)/3
    variance = (16*n - 29)/90
    z_score = (runs - expected_runs)/np.sqrt(variance)
    p_value = 2*(1 - stats.norm.cdf(abs(z_score)))
    
    return p_value > significance_level

def longest_run_test(bits, significance_level=0.01):
    n = len(bits)
    max_run = 0
    current_run = 0
    
    for bit in bits:
        if bit == 1:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 0
            
    expected_length = np.floor(np.log2(n)) - 1
    return max_run <= expected_length

def run_all_tests(filename, significance_level=0.01):
    try:
        bits = read_bits_from_file(filename)
        
        if not bits:
            print("File empty")
            return
            clr
        freq_result = frequency_test(bits, significance_level)
        runs_result = runs_test(bits, significance_level)
        longest_result = longest_run_test(bits, significance_level)
        
        print("bits seq: "+str(len(bits)))
        print("freq monobit test:" + str(freq_result) )
        print("seq test: "+ str(runs_result) )
        print("longest seq ones: " + str(longest_result))
        
    except FileNotFoundError:
        print("File  not found")
    except Exception as e:
        print("exeption:"+ str(e))

if __name__ == "__main__":
    run_all_tests("binary_output.txt")
