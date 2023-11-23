#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
import random

class FShellDeadletter:
    
    #not enabled
    def not_enabled(self, tokens=None, context=None):
        opts = ["This isn't linux. I don't do that.", "Not old-school unix dude.", "You want root access too? lol!", "That's not what I do."]
        return random.choice(opts)

    def sudo(tokens=None, context=None):
        return FShellDeadletter.not_enabled(tokens, context)
    
    def touch(tokens=None, context=None):
        return FShellDeadletter.not_enabled(tokens, context)

    def less(tokens=None, context=None):
        return FShellDeadletter.not_enabled(tokens, context)
    
    def man(tokens=None, context=None):
        return FShellDeadletter.not_enabled(tokens, context)
    
    def whoami(tokens=None, context=None):
        return "FShellDeadletter are who you are."
    
    def head(tokens=None, context=None):
        return FShellDeadletter.not_enabled(tokens, context)
    
    def tail(tokens=None, context=None):
        return FShellDeadletter.not_enabled(tokens, context)
    
    def diff(tokens=None, context=None):
        return FShellDeadletter.not_enabled(tokens, context)

    def ssh(tokens=None, context=None):
        return FShellDeadletter.not_enabled(tokens, context)
    
    def wget(tokens=None, context=None):
        return FShellDeadletter.not_enabled(tokens, context)

    def uname(tokens=None, context=None):
        resp = "FICUS CORE - 0.0.1"
        return resp
    