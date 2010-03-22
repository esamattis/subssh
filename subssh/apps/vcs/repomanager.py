'''
Created on Mar 22, 2010

@author: epeli
'''

import os
import inspect

from subssh import tools


def public_cmd(public_name=""):
    """Decorator for marking methos as public"""
    def decorator(f):
        if public_name:
            f.public_name = public_name
        else:
            f.public_name = f.__name__.replace("_", "-")
        return f
    return decorator

class RepoManager(object):
    def __init__(self, path_to_repos, klass, prefix="", suffix="", 
                 cmd_prefix=""):
        self.klass = klass
        self.cmd_prefix = cmd_prefix
        self.path_to_repos = path_to_repos
        self.prefix = prefix
        self.suffix = suffix
        
        
        self.cmds = {}
        for key, method in inspect.getmembers(self):
            public_name = getattr(method, "public_name", None)
            if public_name:
                self.cmds[cmd_prefix + public_name] = method
                
        
    
    def real(self, repo_name):
        """Return real path of the repository"""
        return os.path.join(self.path_to_repos, 
                            self.prefix + repo_name + self.suffix)
    
    def get_repo_object(self, username, repo_name):
        return self.klass(self.real(repo_name), username)
    
    
    
    @public_cmd()
    def delete_repo(self, username, cmd, args):
        """
        %(name)s <repo name>
        """
        repo = self.get_repo_object(username, args[0])
        repo.delete()
        
    @public_cmd()    
    def rename_repo(self, username, cmd, args):
        """
        %(name)s <repo name> <new repo name>
        """
        repo = self.get_repo_object(username, args[0])
        repo.rename(args[1])        
        
    @public_cmd()    
    def set_permissions(self, username, cmd, args):
        """
        %(name)s <username> <permissions> <repo name>
        """
        repo = self.get_repo_object(username, args[2])
        repo.set_permissions(args[0], args[1])
        repo.save()
        
        
    def _set_default_permissions(self, repo_path, owner):
        """Set default permission to a repository.
        
        Overrides previous permissions if any"""
        
        f = open(os.path.join(repo_path, self.klass.owner_filename), "w")
        f.write(owner)
        f.close()        
        
        repo = self.klass(repo_path, owner)
        repo.set_default_permissions()
        repo.save()        
        
        
    @public_cmd()    
    def init_repo(self, username, cmd, args):
        repo_name = " ".join(args).strip()
         
        if not tools.safe_chars_only_pat.match(repo_name):
            tools.errln("Bad repository name. Allowed characters: %s (regexp)" 
                        % tools.safe_chars)
            return 1                
        
        repo_path = self.real(repo_name)
        if os.path.exists(repo_path):
            tools.errln("Repository '%s' already exists." % repo_name)
            return 1
    
        if not os.path.exists(repo_path):
            os.makedirs(repo_path)
            
        self.create_repository(repo_path, username)
        
        self._set_default_permissions(repo_path, username)
    
    
    def create_repository(self, repo_path, username):
        raise NotImplementedError
    