import pickle as pkl
import pandas as pd
import sys 

if len(sys.argv) != 3:
    print("Not enough arguments")
    print("insert pkl filename and output filename")
    print("pkl_to_csv.py <pkl> <output>")
    exit()

filename=sys.argv[1]
output_filename=sys.argv[2]

with open(filename, "rb") as f:
    data = pkl.load(f)

X_train = data["data"]
y_train= data["label"]

df = pd.DataFrame(X_train)
df2 = pd.DataFrame(y_train)
df.to_csv(output_filename+"_features.csv")
df2.to_csv(output_filename+"_labels.csv")
