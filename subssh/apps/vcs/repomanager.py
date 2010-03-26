'''
Created on Mar 22, 2010

@author: epeli
'''

import os
import inspect
from string import Template

from subssh import tools
from subssh import customlogger
from subssh import config
from abstractrepo import InvalidPermissions

logger = customlogger.get_logger(__name__)




def parse_url_configs(url_configs):
    urls = []
    for url_config in url_configs.split("\n"):
        urls.append( tuple(url_config.split("|")) )
    return urls
        
        


class RepoManager(object):
    
    cmd_prefix = ""
    cmd_suffix = ""
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
        

                
        
    
    def real(self, repo_name):
        """
        Return real path of the repository
        """
        return os.path.join(self.path_to_repos, 
                            self.prefix + repo_name + self.suffix)
    
    def get_repo_object(self, username, repo_name):
        return self.klass(self.real(repo_name), username)
    
    

    @tools.exposable_as()
    def web(self, user, repo_name, action=""):
        """
        Enable anonymous webview.
        
        usage: $cmd <repo name> <enable|disable>
        """
        repo = self.get_repo_object(user.username, repo_name)
        webpath = os.path.join(self.webdir, repo.name_on_fs)
        
        if action == "enable":
            if not os.path.exists(webpath):
                os.symlink(repo.repo_path, webpath)
        elif action == "disable":
            if os.path.exists(webpath):
                os.remove(webpath)
        else:
            raise tools.InvalidArguments("Second argument must be 'enable' "
                                         "or 'disable'")
    
    
    @tools.exposable_as()
    def ls(self, user, action=""):
        """
        List repositories.
        
        usage: $cmd [mine|all]
        """
        repos = []
        
        
        request_user = user.username
        try:
            if action == 'all':
                request_user = config.ADMIN
        except IndexError:
            pass
        
        
        logger.info(self.path_to_repos)
        for repo_in_fs in os.listdir(self.path_to_repos):
            try:
                repo = self.klass(os.path.join(self.path_to_repos, 
                                               repo_in_fs),
                                  request_user)
            except InvalidPermissions:
                continue
            else:
                repos.append(repo.name)
        
        for name in sorted(repos):
            tools.writeln(name)
            
            
    @tools.exposable_as()
    def info(self, user, repo_name):
        """
        Show information about repository.
        
        Shows repository paths, owner and permissions.
        
        usage: $cmd <repo name>
        """
        repo = self.get_repo_object(config.ADMIN, repo_name)
        
        
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
        
        
    
    
    
    @tools.exposable_as()
    def delete(self, user, repo_name):
        """
        Delete repository.
        
        usage: $cmd <repo name>
        """
        repo = self.get_repo_object(user.username, repo_name)
        repo.delete()
    
    @tools.exposable_as()
    def add_owner(self, user, repo_name, username):
        """
        Add owner to repository.
        
        usage: $cmd <repo name> <username>
        """
        repo = self.get_repo_object(user.username, repo_name)
        repo.add_owner(username)
        repo.save()
        
        
    @tools.exposable_as()
    def remove_owner(self, user, repo_name, username):
        """
        Remove owner from repository.
        
        usage: $cmd <repo name> <username>
        """
        repo = self.get_repo_object(user.username, repo_name)
        repo.remove_owner(username)
        repo.save()    
    
    
    
    @tools.exposable_as()
    def rename(self, user, repo_name, new_name):
        """
        Rename repository.
        
        usage: $cmd <repo name> <new repo name>
        """
        repo = self.get_repo_object(user.username, repo_name)
        repo.rename(new_name)        
        

    @tools.exposable_as()
    def set_permissions(self, user, username, permissions, repo_name):
        """
        Set read/write permissions to repository.
        
        usage: $cmd <username> <permissions> <repo name>
        
        Permissions can be 'r', 'w', or 'rw'
        
        Eg. $cmd myfriend rw myrepository
        
        Only owners can change permissions. Owners can also add and remove
        other owners. 
        
        """
        repo = self.get_repo_object(user.username, repo_name)
        repo.set_permissions(username, permissions)
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
        
        
    @tools.exposable_as()
    def init(self, user, repo_name):
        """
        Create new repository.
        
        usage: $cmd <repository name>
        """
         
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
            
        self.create_repository(repo_path, user.username)
        
        self._set_default_permissions(repo_path, user.username)
    

    def create_repository(self, repo_path, username):
        raise NotImplementedError
    