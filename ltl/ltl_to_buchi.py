import numpy as np

class State():
    def __init__(self, incoming = None, outgoing = None, loop = None, endState = None, selfloop_status = None, outgoing_status = None):
        self.name = None
        self.incoming = incoming
        self.outgoing = outgoing
        self.loop = loop
        self.endState = endState
        self.selfloop_status = selfloop_status
        self.outgoing_status = outgoing_status
        
class LTL_To_Buchi():
    def __init__(self, ltl):
        self.ltl = ltl[0].split(" ")
        
    def createAutomata(self):
        states = []
        for i in range(5):
            state = State()
            states.append(state)

        ###---State 0 ---###
        states[0].name = 0
        states[0].incoming = {1 : "P1&P2&P3",2 : "P1&P2&P3", 3 : "P1&P2&P3", 4 : "P0"} #array gibi yazarsak daha iyi olur & ile yazmaktan
        states[0].outgoing = {1 : "!P1", 2: "P1&!P2", 3 : "P1&P2&!P3", 4 : "!P0&P1&P2&P3"}
        states[0].loop = "P0&P1&P2&P3"
        states[0].endstate = True
        states[0].selfloop_status = "Positive"
        states[0].outgoing_status = [None,"Negative","Positive","Positive","Positive"]

        ###---State 1 ---###
        states[1].name = 1
        states[1].incoming = {0: "!P1"}
        states[1].outgoing = {0 : "P1&P2&P3", 2 : "P1&!P2", 3 : "P1&P2&!P3"}
        states[1].loop = "!P0&!P1"
        states[1].endstate = False
        states[1].selfloop_status = "Negative"
        states[1].outgoing_status = ["Positive",None,"Positive","Positive","Positive"]

        ###---State 2 ---###
        states[2].name = 2
        states[2].incoming = {0: "P1&!P2", 1: "P1&!P2"}
        states[2].outgoing = {0 : "P1&P2&P3", 3 : "P1&P2&!P3"}
        states[2].loop = "!P0&!P1&!P2"
        states[2].endstate = False
        states[2].selfloop_status = "Negative"
        states[2].outgoing_status = ["Positive",None,"Positive","Positive",None]

        ###---State 3 ---###
        states[3].name = 3
        states[3].incoming = {0: "P1&P2&!P3", 1: "P1&P2&!P3", 2: "P1&P2&!P3"}
        states[3].outgoing = {0 : "P1&P2&P3"}
        states[3].loop = "!P0&!P1&P2&!P3"
        states[3].endstate = False
        states[3].selfloop_status = "Negative"
        states[3].outgoing_status = ["Positive",None,None,None,None]

        ###---State 4 ---###
        states[4].name = 4
        states[4].incoming = {0: "!P0&P1&P2&P3"}
        states[4].outgoing = {0 : "P0"}
        states[4].loop = "!P0"
        states[4].endstate = False
        states[4].selfloop_status = "Negative"
        states[4].outgoing_status = ["Positive",None,None,None,None]

        return states