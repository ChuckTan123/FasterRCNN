import json

with open("cat_small/annotation.json", "r") as f:
    js = json.load(f)
with open("cat_small/index.txt", "w") as f:
    f.write("\n".join(js.keys()))