# Copyright 2020-2021 nunopenim @github
# Copyright 2020-2021 prototype74 @github
#
# Licensed under the PEL (Penim Enterprises License), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the PE License

from .registration import pre_register_cmd
from userbot import tgclient
from userbot.include.language_processor import SystemUtilitiesText as msgResp
from telethon.events import ChatAction, MessageEdited, NewMessage
from logging import getLogger, Logger
from re import compile, sub

class EventHandler:
    def __init__(self, log: Logger = None, traceback: bool = True):
        """
        Initialize EventHandler to catch Telethon Events such as NewMessage or ChatAction

        Args:
            log (Logger): passing an already existing logger. Default None
            logging (boolean): Create a traceback in case of unhandled exceptions. Default True

        Example:
            from userbot.sysutils.event_handler import EventHandler
            from logging import getLogger

            log = getLogger(__name__)
            ehandler = EventHandler()  # initialize with default logger
            ehandler = EventHandler(log)  # initialize with an already existing logger
            ehandler = EventHandler(log, False)  # initialize with an already existing logger without Tracebacks
        """
        self.log = log if isinstance(log, Logger) else getLogger(__name__)
        self.traceback = traceback

    def __removeRegEx(self, pattern: str) -> str:
        """
        Removes any word characters from pattern

        Args:
            pattern (string): pattern to remove word characters

        Returns:
            string without word characters
        """
        return sub(r"\W", "", pattern)

    #def __isRegExCMD(self, pattern: str) -> bool:  # TODO
    #    """
    #    Check if pattern has regular expressions
    #
    #    Args:
    #        pattern (string): pattern to check for regex
    #
    #    Returns:
    #        True if valid regex found else False
    #    """
    #    pattern_no_regex = self.__removeRegEx(pattern)
    #    if pattern == pattern_no_regex:
    #        return False
    #    try:
    #        compile(pattern)
    #    except:
    #        return False
    #    return True

    def on(self, command: str, alt: str = None, hasArgs: bool = False, **args):
        """
        Default listen on function which uses MessageEdited and NewMessage events.
        Recommended for outgoing messages/updates.

        Args:
            command (string): command to listen to (must not be None)
            alt (string): alternative way to 'command' (must be None)
            hasArgs (bool): whether 'command' takes arguments (default to False)

        Note:
            Function accepts any further arguments as supported by MessageEdited and NewMessage events

        Example:
            from userbot.sysutils.event_handler import EventHandler
            ehandler = EventHandler()

            @ehandler.on(command="example", outgoing=True)
            async def example_handler(event):
                await event.edit("hi!")

        Returns:
            MessageEdited.Event or NewMessage.Event
        """
        def decorator(function):
            if not function:
                return None
            if not callable(function):
                return None
            cmd = command
            curr_alt = alt
            if curr_alt:
                curr_alt = self.__removeRegEx(curr_alt)
            if not pre_register_cmd(cmd, curr_alt, hasArgs, function):
                self.log.error(f"Unable to add command '{cmd}' in function '{function.__name__}' "\
                                "to event handler as previous registration failed")
                return None
            async def func_callback(event):
                try:
                    await function(event)
                except Exception as e:
                    # This block will be executed if the function, where the events are
                    # being used, has no own exception handler(s)
                    try:
                        # get current executed command
                        curr_cmd = event.pattern_match.group(0).split(" ")[0][1:]
                    except:
                        curr_cmd = cmd
                    self.log.error(f"Command '{curr_cmd}' stopped due to an unhandled exception "
                                   f"in function '{function.__name__}'", exc_info=True if self.traceback else False)
                    try:  # in case editing messages isn't allowed (channels)
                        await event.edit(f"`{msgResp.CMD_STOPPED.format(f'{curr_cmd}.exe')}`")
                    except:
                        pass
            if curr_alt:
                cmd_regex = fr"^\.(?:{cmd}|{curr_alt})(?: |$)(.*)" if hasArgs else fr"^\.(?:{cmd}|{curr_alt})$"
            else:
                cmd_regex = fr"^\.{cmd}(?: |$)(.*)" if hasArgs else fr"^\.{cmd}$"
            tgclient.add_event_handler(func_callback, MessageEdited(pattern=cmd_regex, **args))
            tgclient.add_event_handler(func_callback, NewMessage(pattern=cmd_regex, **args))
            return func_callback
        return decorator

    def on_NewMessage(self, command: str, alt: str = None, hasArgs: bool = False, **args):
        """
        Listen to NewMessage events only.

        Args:
            command (string): command to listen to (must not be None)
            alt (string): alternative way to 'command' (must be None)
            hasArgs (bool): whether 'command' takes arguments (default to False)

        Note:
            Function accepts any further arguments as supported by NewMessage events

        Example:
            from userbot.sysutils.event_handler import EventHandler
            ehandler = EventHandler()

            @ehandler.on(command="example", outgoing=True)
            async def example_handler(event):
                await event.edit("hi!")

        Returns:
            NewMessage.Event
        """
        def decorator(function):
            if not function:
                return None
            if not callable(function):
                return None
            cmd = command
            curr_alt = alt
            if curr_alt:
                curr_alt = self.__removeRegEx(curr_alt)
            if not pre_register_cmd(cmd, curr_alt, hasArgs, function):
                self.log.error(f"Unable to add command '{cmd}' in function '{function.__name__}' "\
                                "to event handler as previous registration failed")
                return None
            async def func_callback(event):
                try:
                    await function(event)
                except Exception as e:
                    try:
                        curr_cmd = event.pattern_match.group(0).split(" ")[0][1:]
                    except:
                        curr_cmd = cmd
                    self.log.error(f"Command '{curr_cmd}' stopped due to an unhandled exception "
                                   f"in function '{function.__name__}'", exc_info=True if self.traceback else False)
                    try:
                        await event.edit(f"`{msgResp.CMD_STOPPED.format(f'{curr_cmd}.exe')}`")
                    except:
                        pass
            if curr_alt:
                cmd_regex = fr"^\.(?:{cmd}|{curr_alt})(?: |$)(.*)" if hasArgs else fr"^\.(?:{cmd}|{curr_alt})$"
            else:
                cmd_regex = fr"^\.{cmd}(?: |$)(.*)" if hasArgs else fr"^\.{cmd}$"
            tgclient.add_event_handler(func_callback, NewMessage(pattern=cmd_regex, **args))
            return func_callback
        return decorator

    def on_ChatAction(self, **args):
        """
        Listen to chat activities (join, leave, new pinned message etc.) in any or certain chats.

        Note:
            Function accepts any further arguments as supported by ChatAction events

        Example:
            from userbot.sysutils.event_handler import EventHandler
            ehandler = EventHandler()

            @ehandler.on_ChatAction()
            async def example_handler(event):
                if event.user_joined:
                    await event.reply("Welcome!")

        Returns:
            ChatAction.Event
        """
        def decorator(function):
            async def func_callback(event):
                try:
                    await function(event)
                except Exception as e:
                    self.log.error(f"Function '{function.__name__}' stopped due to an unhandled exception",
                                   exc_info=True if self.traceback else False)
            tgclient.add_event_handler(func_callback, ChatAction(**args))
            return func_callback
        return decorator
