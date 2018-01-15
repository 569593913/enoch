from analyze.simulation.Trader import *

def testBuy():
    trader = Trader(20000)
    trader.buy("1234",1,10,100)
    trader.buy("1234",1,10,100)
    trader.buy("1234",2,11,200)
    trader.buy("2345",1,50,5000)
    print trader

def testSell():
    trader = Trader(10000)
    trader.buy("1234", 1, 1, 100)
    trader.fresh(1,{"1234":2})
    trader.sell("1234", 200000, 200)
    print trader

def testHold():
    trader = Trader()
    trader.buy("1234", 1, 10, 100)
    print trader.isHold("1234")
# testBuy()
testSell()
# testHold()