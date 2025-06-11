n, k = map(int, input().split())
arr = list(map(int, input().split()))

def staLinear():
	res=[]
	count=0
	for i in range(1, k+1):
		for n in arr:
			if i%n==0:
				count+=1
				res.append(i)
				break
	return count

def staPie():
	res = 0
	for mask in range(1, 1<<n):
		odd=0
		mult=1
		valid=True
		for i in range(n):
			if mask & (1<<i):
				mult *= arr[i]
				if mult > k:
					valid=False
					break
				odd^=1
		if not valid: continue
		cur = k//mult
		# print(bin(mask), cur)
		if odd: res += cur
		else: res -= cur
	return res


# print(staLinear())
# print(staPie())

res = staPie()
# linear = staLinear()
# if res != linear: print(res, linear)
print(res)