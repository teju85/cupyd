import os
import json

def read_rc():
    imgs = {}
    rcFile = os.getenv("RC_FILE", default=None)
    if rcFile is not None:
        with open(rcFile) as fp:
            data = json.load(fp)
            for img in data.keys():
                imgs[img] = data[img]
    return imgs
