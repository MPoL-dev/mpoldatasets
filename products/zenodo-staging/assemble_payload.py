# start off assuming everything in local list goes into payload
local = {}
with open("locallist.chk", "r") as f:
    for line in f:
        md5, fname = line.split()
        local[fname] = md5


# load zenodo dictionary
zenodo = {}
with open("zenodolist.chk", "r") as f:
    for line in f:
        md5, fname = line.split()
        zenodo[fname] = md5

# iterate through local dictionary and pop items that have a matching key in zenodo dictionary
with open("payloadlist.txt", "w") as f:
    for (key, val) in local.items():
        if key in zenodo and val == zenodo[key]:
            continue
        else:
            f.write("{:}\n".format(key))
