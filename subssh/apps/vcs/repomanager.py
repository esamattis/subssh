'''
Created on Mar 22, 2010

@author: epeli
'''

import os
import inspect

from subssh import tools
from abstractrepo import InvalidPermissions
from subssh import customlogger

logger = customlogger.get_logger(__name__)

def public_cmd(public_name=""):
    """Methods decorated with this will be usable on subssh prompt
    """
    def decorator(f):
        if public_name:
            f.public_name = public_name
        else:
            f.public_name = f.__name__.replace("_", "-")
        decorator.__name__ = f.__name__
        decorator.__doc__ = f.__doc__
        decorator.__dict__ = f.__dict__    
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
    def ls_repos(self, username, cmd, args):
        repos = []
        
        logger.info(self.path_to_repos)
        for repo_in_fs in os.listdir(self.path_to_repos):
            try:
                repo = self.klass(os.path.join(self.path_to_repos, 
                                               repo_in_fs),
                                  username)
            except InvalidPermissions:
                continue
            else:
                repos.append(repo.name)
        
        for name in sorted(repos):
            tools.writeln(name)
            
                
        
    
    
    @public_cmd()
    @tools.require_args(exactly=1)
    def delete_repo(self, username, cmd, args):
        """
        usage: %(name)s <repo name>
        """
        repo = self.get_repo_object(username, args[0])
        repo.delete()
    
    @public_cmd()
    @tools.require_args(exactly=2)    
    def rename_repo(self, username, cmd, args):
        """
        usage: %(name)s <repo name> <new repo name>
        """
        repo = self.get_repo_object(username, args[0])
        repo.rename(args[1])        
        

    @public_cmd()
    @tools.require_args(exactly=3)
    def set_permissions(self, username, cmd, args):
        """
        usage: %(name)s <username> <permissions> <repo name>
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
    @tools.require_args(at_least=1)
    def init_repo(self, username, cmd, args):
        """
        usage: %(name)s <repository name>
        """
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
    