import json

with open("cat_full/annotation.json", "r") as f:
    js = json.load(f)
with open("cat_full/index.txt", "w") as f:
    f.write("\n".join(js.keys()))