'''
Created on Mar 22, 2010

@author: epeli
'''

import os
import inspect
from string import Template

from subssh import tools
from abstractrepo import InvalidPermissions
from subssh import customlogger
from subssh import config

logger = customlogger.get_logger(__name__)

def public_cmd(public_name=""):
    """
    Methods decorated with this will be usable on subssh prompt
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


def parse_url_configs(url_configs):
    urls = []
    for url_config in url_configs.split("\n"):
        urls.append( tuple(url_config.split("|")) )
    return urls
        
        


class RepoManager(object):
    
    cmd_prefix = ""
    suffix = ""
    prefix = ""
    klass = None
    
    def __init__(self, path_to_repos, webdir="", urls=[]):
        self.path_to_repos = path_to_repos
        self.urls = urls
        self.webdir = webdir
        
        if self.webdir and not os.path.exists(self.webdir):
            os.makedirs(self.webdir)
        
        
        if not os.path.exists(self.path_to_repos):
            os.makedirs(self.path_to_repos)
        
        self.cmds = {}
        for key, method in inspect.getmembers(self):
            public_name = getattr(method, "public_name", None)
            if public_name:
                self.cmds[self.cmd_prefix + public_name] = method
                
        
    
    def real(self, repo_name):
        """
        Return real path of the repository
        """
        return os.path.join(self.path_to_repos, 
                            self.prefix + repo_name + self.suffix)
    
    def get_repo_object(self, username, repo_name):
        return self.klass(self.real(repo_name), username)
    
    

    @public_cmd()
    @tools.require_args(exactly=2)    
    def web(self, username, cmd, args):
        """
        usage: $cmd <repo name> <enable|disable>
        """
        repo = self.get_repo_object(username, args[0])
        webpath = os.path.join(self.webdir, repo.name_on_fs)
        
        if args[1] == "enable":
            if not os.path.exists(webpath):
                os.symlink(repo.repo_path, webpath)
        elif args[1] == "disable":
            if os.path.exists(webpath):
                os.remove(webpath)
        else:
            raise tools.InvalidArguments("Second argument must be 'enable' "
                                         "or 'disable'")
    
    
    @public_cmd()
    @tools.require_args(at_most=1)
    def ls(self, username, cmd, args):
        """
        List repositories
        
        usage: $cmd [mine|all]
        """
        repos = []
        
        
        user = username
        try:
            if args[0] == 'all':
                user = config.ADMIN
        except IndexError:
            pass
        
        
        logger.info(self.path_to_repos)
        for repo_in_fs in os.listdir(self.path_to_repos):
            try:
                repo = self.klass(os.path.join(self.path_to_repos, 
                                               repo_in_fs),
                                  user)
            except InvalidPermissions:
                continue
            else:
                repos.append(repo.name)
        
        for name in sorted(repos):
            tools.writeln(name)
            
            
    @public_cmd()
    @tools.require_args(exactly=1)      
    def info(self, username, cmd, args):
        """
        Print repository owner and permissions
        
        usage: $cmd <repo name>
        """
        repo = self.get_repo_object(config.ADMIN, args[0])
        
        
        tools.writeln()
        tools.writeln("Access:")
        for url_name, url_tmpl in self.urls:
            url = Template(url_tmpl).substitute(name=repo.name, 
                                                name_on_fs=repo.name_on_fs,
                                                hostname=config.DISPLAY_HOSTNAME,
                                                hostusername=tools.hostusername(),)
            tools.writeln("    %s: %s" %(url_name, url) )
        
        
        tools.writeln()
        tools.writeln("Owners: %s" % ", ".join(repo.get_owners()).strip(", "))
        tools.writeln()
        
        tools.writeln("Permissions:")
        for username, perm in repo.get_all_permissions():
            tools.writeln("    %s = %s" %(username, perm) )
        
        
    
    
    
    @public_cmd()
    @tools.require_args(exactly=1)
    def delete(self, username, cmd, args):
        """
        usage: $cmd <repo name>
        """
        repo = self.get_repo_object(username, args[0])
        repo.delete()
    
    @public_cmd()
    @tools.require_args(exactly=2)    
    def rename(self, username, cmd, args):
        """
        usage: $cmd <repo name> <new repo name>
        """
        repo = self.get_repo_object(username, args[0])
        repo.rename(args[1])        
        

    @public_cmd()
    @tools.require_args(exactly=3)
    def set_permissions(self, username, cmd, args):
        """
        usage: $cmd <username> <permissions> <repo name>
        """
        repo = self.get_repo_object(username, args[2])
        repo.set_permissions(args[0], args[1])
        repo.save()
        
        
    def _set_default_permissions(self, repo_path, owner):
        """
        Set default permission to a repository.
        
        Overrides previous permissions if any
        """
        
        f = open(os.path.join(repo_path, self.klass.owner_filename), "w")
        f.write(owner)
        f.close()        
        
        repo = self.klass(repo_path, owner)
        repo.set_default_permissions()
        repo.save()        
        
        
    @public_cmd()
    @tools.require_args(at_least=1)
    def init(self, username, cmd, args):
        """
        usage: $cmd <repository name>
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
    