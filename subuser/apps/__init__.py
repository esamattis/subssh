
import uptime
import svn
import git

all = {}


for module in locals().values():
    if hasattr(module, "cmds"):
        all.update(module.cmds)
        

