"""
A simple config-file based authentication module.
"""

__authors__ = ['"Hans Lellelid" <hans@xmpl.org>']
__copyright__ = "Copyright 2009 Hans Lellelid"
__license__ = """Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 
  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

from ConfigParser import RawConfigParser
from coilmq.auth import Authenticator
from coilmq.config import config

def make_simple():
    """
    Create a L{SimpleAuthenticator} instance using values read from coilmq configuration.
    
    @return: The configured L{SimpleAuthenticator}
    @rtype: L{SimpleAuthenticator}
    @raise RuntimeError: If there is a configuration error. 
    """
    authfile = config.get('coilmq', 'authenticator_authfile')
    if not authfile:
        raise RuntimeError('Missing configuration parameter: authenticator_authfile')
    sa = SimpleAuthenticator()
    sa.from_configfile(authfile)
    return sa
    
class SimpleAuthenticator(Authenticator):
    """
    A simple configfile-based authenticator.
    
    @param store:  Authentication key-value store (of logins to passwords).
    @type store: C{dict} of C{str} to C{str}
    """
    def __init__(self, store=None):
        """
        Initialize the authenticator to use specified config file (or file-like object).
        
        @param store:  Authentication store, C{dict} of logins to passwords.
        @type store: C{dict} of C{str} to C{str}
        """
        if store is None:
            store = {}
        self.store = store
    
    def from_configfile(self, configfile):
        """
        Initialize the authentication store from a "config"-style file.
        
        Auth "config" file is parsed with C{ConfigParser.RawConfigParser} and must contain
        an [auth] section which contains the usernames (keys) and passwords (values).
        
        Example auth file:
            [auth]
            someuser = somepass
            anotheruser = anotherpass
        
        @param configfile: Path to config file or file-like object. 
        @type configfile: C{any}
        """
        cfg = RawConfigParser()
        if hasattr(configfile, 'read'):
            cfg.readfp(configfile)
        else:
            filesread = cfg.read(configfile)
            if not filesread:
                raise ValueError('Could not parse auth file: %s' % configfile)
            
        if not cfg.has_section('auth'):
            raise ValueError('Config file contains no [auth] section.')
        
        self.store = dict(cfg.items('auth'))
        
    def authenticate(self, login, passcode):
        """
        Authenticate the login and passcode.
         
        @return: Whether user is authenticated.
        @rtype: C{bool} 
        """
        return login in self.store and self.store[login] == passcode
    