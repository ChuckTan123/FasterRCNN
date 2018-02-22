import json

with open("annotation.json", "r") as f:
    jf = json.load(f)

small = {}
idx = 0
for key in jf:
    small[key] = jf[key]
    idx += 1
    if idx >= 10:
        break

with open("annotation_small.json", "w") as f:
    json.dump(small, f)

keys = small.keys()

with open("idx_small.txt", "w") as f:
    f.write("\n".join(keys))