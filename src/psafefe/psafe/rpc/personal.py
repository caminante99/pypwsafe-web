#===============================================================================
# This file is part of PyPWSafe.
#
#    PyPWSafe is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    PyPWSafe is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyPWSafe.  If not, see http://www.gnu.org/licenses/old-licenses/gpl-2.0.html 
#===============================================================================
''' The user's personal psafe control
Created on Aug 16, 2011

@author: Paulson McIntyre <paul@gpmidi.net>
'''
from rpc4django import rpcmethod
from psafefe.psafe.rpc.errors import *
from psafefe.psafe.rpc.auth import auth
from psafefe.psafe.models import *
from psafefe.psafe.functions import setDatabasePasswordByUser

# Psafe entry methods
@rpcmethod(name = 'psafe.personal.setPsafePasswordByPK', signature = ['boolean', 'string', 'string', 'int', 'string'])
@auth
def setPsafePasswordByPK(username, password, safePK, safePassword, **kw):
    """ Update the given user's personal psafe to include the password to the given safe.  
    
    @param username: Requesting user's login
    @type username: string
    @param password: Requesting user's login
    @type password: string
    @param safePK: The database id of the safe that the password is for.  
    @type safePK: int
    @param safePassword: The password to use when decrypting the given psafe. 
    @type safePassword: string
    @return: boolean, True on success
    @raise EntryDoesntExistError: The safe you are trying to save a password for doesn't exist or the requesting user doesn't have access to it.  
    """
    try:
        pws = PasswordSafe.objects.get(pk = safePK)
    except PasswordSafe.DoesNotExist:
        raise EntryDoesntExistError
    
    repo = pws.repo
    if repo.user_can_access(kw['user'], mode = "R"):
        # User should have access to the requested safe
        setDatabasePasswordByUser(
                                  user = kw['user'],
                                  userPassword = password,
                                  psafe = pws,
                                  psafePassword = safePassword,
                                  wait = True,
                                  )
        return True
    # User doesn't have access so it might as well not exist
    raise EntryDoesntExistError

@rpcmethod(name = 'psafe.personal.setPsafePasswordByUUID', signature = ['boolean', 'string', 'string', 'int', 'string'])
@auth
def setPsafePasswordByUUID(username, password, safeUUID, safePassword, **kw):
    """ Update the given user's personal psafe to include the password to the given safe.
      
    @param username: Requesting user's login
    @type username: string
    @param password: Requesting user's login
    @type password: string
    @param safeUUID: The database UUID of the safe that the password is for.  
    @type safeUUID: int
    @param safePassword: The password to use when decrypting the given psafe. 
    @type safePassword: string
    @return: boolean, True on success
    @raise EntryDoesntExistError: The safe you are trying to save a password for doesn't exist or the requesting user doesn't have access to it.  
    """
    try:
        # TODO: Add in better handling of more than one entry with the same UUID
        pws = PasswordSafe.objects.get(uuid = safeUUID)
    except PasswordSafe.DoesNotExist:
        raise EntryDoesntExistError
    
    repo = pws.repo
    if repo.user_can_access(kw['user'], mode = "R"):
        # User should have access to the requested safe
        setDatabasePasswordByUser(
                                  user = kw['user'],
                                  userPassword = password,
                                  psafe = pws,
                                  psafePassword = safePassword,
                                  wait = True,
                                  )
        return True
    # User doesn't have access so it might as well not exist
    raise EntryDoesntExistError



@rpcmethod(name = 'psafe.personal.createPersonalPSafe', signature = ['boolean', 'string', 'string'])
@auth
def createPersonalPSafe(username, password, **kw):
    """ Create and initialize a personal psafe for the calling user if the user 
    doesn't already have one.
     
    @param username: Requesting user's login
    @type username: string
    @param password: Requesting user's login
    @type password: string
    @return: boolean, True on success, error otherwise
    """
    from psafefe.psafe.functions import getUsersPersonalSafe
    p = getUsersPersonalSafe(user = kw['user'], userPassword = password, wait = True)
    return True

