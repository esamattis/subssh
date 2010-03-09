
import uptime
import svn
import git
import whoami

all = {}

for module in locals().values():
    if hasattr(module, "cmds"):
        all.update(module.cmds)
        

