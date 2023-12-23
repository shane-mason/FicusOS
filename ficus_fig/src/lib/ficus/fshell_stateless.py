#
# MIT License (MIT)
# Copyright (c) 2023 Shane C Mason
# FicusOS
#
import random

class FShellStatic:
    def hello(tokens=None, context=None):
        opts = ["Bonjour", "Hola", "Nǐn hǎo", "Ciao", "Konnichiwa", "Guten Tag", "Olá", "Anyoung haseyo", "Goddag", "Shikamoo", "Yassas", "Merhaba", "Shalom"]
        return random.choice(opts)
    
    def future(tokens=None, context=None):
        return "So bright that you gotta wear shades!"
    
    def test(tokens=None, context=None):
        opts = ["You passed.", "Did I pass?", "Noun: A critical examination, observation, or evaluation", "Verb: to put to test or proof"]    
        return random.choice(opts)
    
    def echo(tokens=None, context=None):
        return " ".join(tokens[1:])
    
    def about(self, tokens=None, context=None):
        return """FICUS OS 0.0.1
-> it works sometimes."""

    