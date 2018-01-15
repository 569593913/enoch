from analyze.simulation.Simulator import *
from analyze.strategy.sequence.StrategyS1 import *

def runSingle():
    s1 = StrategyS1()
    sim = Simulator(s1)
    code = '000002'
    sim.runSingle(code)







runSingle()