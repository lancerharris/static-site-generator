
import os
import shutil

def cp_source_contents_to_destination(source, destination):
    if not os.path.exists(source):
        raise Exception("source directory does not exist")
    
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    os.mkdir(destination)

    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        if os.path.isdir(s):
            os.mkdir(d)
            cp_source_contents_to_destination(s, d)
        else:
            shutil.copy(s, d)