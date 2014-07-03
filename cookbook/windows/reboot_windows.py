"""
http://github.com/RiverMeadow/local-migrations-windows/blob/develop/windows_migration/core/utils/reboot.py
"""
import win32api
import win32security
import win32process

import ntsecuritycon
import win32con


class RebootHelper:
    """
    Provides functionality to help to reboot windows machine
    """

    # Ranges are:
    # 000-0FF Reserved by windows,
    # 100-1FF Last, 200-2FF Middle, 300-3FF First,
    # 400-4FF Reserved by windows
    SHUTDOWN_LAST_ORDER = 0x101  # shutdown last

    # shutdown timeout
    SHUTDOWN_TIMEOUT_SEC = 30

    # Force applications to be closed
    FORCE_APP_CLOSURE = True

    # Make sure it reboots at the end
    REBOOT_AFTER = True

    def reboot(self, message):
        """
        Initiates reboot of the machine
        @param message: message to display to the user
        @type message: str
        @return: None
        @rtype: None
        """
        # get necessary security context
        flags = ntsecuritycon.TOKEN_ADJUST_PRIVILEGES | ntsecuritycon.TOKEN_QUERY
        token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
        privilege_id = win32security.LookupPrivilegeValue(None, ntsecuritycon.SE_SHUTDOWN_NAME)
        new_privileges = [(privilege_id, ntsecuritycon.SE_PRIVILEGE_ENABLED)]
        win32security.AdjustTokenPrivileges(token, 0, new_privileges)
        # make sure this process is getting shutdown at the end
        win32process.SetProcessShutdownParameters(self.SHUTDOWN_LAST_ORDER,
                                                  win32con.SHUTDOWN_NORETRY)
        win32api.InitiateSystemShutdown("",  # machine name
                                        message,
                                        self.SHUTDOWN_TIMEOUT_SEC,
                                        self.FORCE_APP_CLOSURE,
                                        self.REBOOT_AFTER)

