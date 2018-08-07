import sys



with open("dummy.txt", "w") as f:
	for i in range(5000):
		f.write(str(i + 1) + '\n')
	f.close()