'''
Created on Mar 8, 2010

@author: epeli
'''



def parse_cmd(f):
    
    def parse(username, ssh_original_command): 
        parts = ssh_original_command.split()
        cmd = parts[0]
        args = [arg.strip('"').strip("'") for arg in parts[1:]]
        return f(username, cmd, args)
    
    return parse



if __name__ == "__main__":
    
    @parse_cmd
    def test(cmd, args):
        print cmd, args
        
        
    test("customcmd arg1 arg2")
