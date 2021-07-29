# Contact: Sara Ferreira [sara (dot) ferreira (at) fc (dot) up (dot) pt]
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

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
