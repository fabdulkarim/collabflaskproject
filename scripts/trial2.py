from scriptFadhil import fadhilProcess

import sys

a,b = fadhilProcess(sys.argv[1], sys.argv[2], sys.argv[3])

print("Quotes Hari ini adalah")
print(a)
print("- {}".format(b))