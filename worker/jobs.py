import hashlib
import math

CURRENT_JOB = ''
    
def fib(n):
    if int(n) <= 0:
        return []
    a, b = 0, 1
    
    ctr = 0
    while ctr < int(n):
        a, b = b, a + b
        ctr += 1
        
    return a
    
def brute_force(target, file, hash_type):
    file_data = file['binary_data']
    print(hash_type)
    file_data = file_data.splitlines()
    
    for line in file_data:
        if hash_type == "md5":
            hashed_line = hashlib.md5(line.encode()).hexdigest()
        elif hash_type == "SHA256":
            hashed_line = hashlib.sha256(line.encode()).hexdigest()
        elif hash_type == "SHA512":
            hashed_line = hashlib.sha512(line.encode()).hexdigest()
        if target == hashed_line:
            output = "Found key - {} - in wordlist".format(line)
            return output
    output = "Did not find key in wordlist".format(line)
    return output
    
def count_occurrence(letter, file):
    file_data = file['binary_data']
    
    letter_ctr = 0
    for char in file_data:
        if letter == char:
            letter_ctr += 1
     
    return letter_ctr

def calculate_entropy(file):
    byte_data = file['binary_data']
    
    if isinstance(byte_data, str):
        byte_data = byte_data.encode()  # Just in case

    if not byte_data:
        return 0.0

    byte_count = [0] * 256
    for b in byte_data:
        byte_count[b] += 1

    entropy = 0.0
    length = len(byte_data)

    for count in byte_count:
        if count == 0:
            continue
        p = count / length
        entropy -= p * math.log2(p)

    return str(entropy)
     
def start_job(job_name, user_input, file_input, hash_input):
    global CURRENT_JOB
    output = ''

    if job_name == "heavy_calc":
        CURRENT_JOB = "Fibonacci"
        output = fib(user_input)
    elif job_name == "brute_force":
        CURRENT_JOB = "Brute Force"
        output = brute_force(user_input, file_input, hash_input)
    elif job_name == "count_occurrence":
        CURRENT_JOB = "Count Occurrences"
        output = count_occurrence(user_input, file_input)
    elif job_name == "calculate_entropy":
        CURRENT_JOB = "Calculate Entropy"
        output = calculate_entropy(file_input)
    
    return output
     
def get_current_job():
    return CURRENT_JOB