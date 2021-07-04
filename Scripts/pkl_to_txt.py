import sys 
import pickle


if len(sys.argv) != 3:
    print("Not enough arguments")
    print("insert pkl filename and output filename")
    print("pkl_to_txt.py <pkl> <output>")
    exit()

filename=sys.argv[1]
output_filename=sys.argv[2]

try:
    pkl_file = open(filename, 'rb')
except OSError:
    print("Could not open/read file:")
    exit()
data = pickle.load(pkl_file)
pkl_file.close()

X_train = data["data"]
y_train= data["label"]

f = open(output_filename+".txt", "a")

for i in range(0, len(X_train)):
    f.write("Sample "+str(i)+": \n"+"features: "+str(X_train[i])+"label: "+str(y_train[i])+"\n")

f.close()
