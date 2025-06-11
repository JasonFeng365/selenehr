import random
from os import system

import sys
import hashlib
random.seed(hashlib.sha1(("".join(sys.argv).encode())).hexdigest())
testcaseNumber = int(sys.argv[1])
args = sys.argv[2:]

args = list(map(int, args))
length = args[0]

isPrime = [True]*101
primes = []
for i in range(2, 101):
	if isPrime[i]:
		primes.append(i)
		for j in range(i*i, 101, i): isPrime[j]=False

arr = random.sample(primes, length)
random.shuffle(arr)

up = min(1<<(length+10), 10**9)
k = random.randint(up//2, up)

inputPath = f"testcases/input/input{testcaseNumber:02d}.txt"
outputPath = f"testcases/output/output{testcaseNumber:02d}.txt"
with open(inputPath, 'w') as f:
	f.write(" ".join(map(str, [length, k])))
	f.write('\n')
	f.write(" ".join(map(str, arr)))

cmd = f"python sol.py < {inputPath} > {outputPath}"
system(cmd)