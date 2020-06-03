from arbitrageCore.multi_exchange import create_weighted_multi_exchange_digraph
from arbitrageCore.bellman_multi_graph import bellman_ford_multi
from arbitrageCore.general import print_profit_opportunity_for_path_multi
import time
import math
from ccxt import exchanges
from stem import Signal
from stem.control import Controller
from urllib.request import urlopen

'''if __name__ == '__main__':
  with Controller.from_port() as controller:
    controller.authenticate()

    print("Tor is running version %s" % controller.get_version())
    newIP=urlopen("http://icanhazip.com").read()
    print("NewIP Address: %s" % newIP)   '''

def consultarCamino(exchanges,source,money,unique_paths):

        graph = create_weighted_multi_exchange_digraph(exchanges, name=True, log=True,fees=True)

        graph, paths = bellman_ford_multi(graph, source, unique_paths=unique_paths)

        vectorTransactions=[]
        #print("TODOS LOS POSIBLES TRADE:")
        for path in paths:
            transaccion=print_profit_opportunity_for_path_multi(graph, path, print_output=False, round_to=None, shorten=False, money=money)
            if transaccion != None:
                vectorTransactions.append(transaccion)
        #[('BTC', 'DAI', 9140.052479999997, 9.140052479999996, 'kraken', 'BTC/DAI', 'sell')]
        #inicia desde el primer exchange pasado y la moneda pasada
        vectorFiltradoMonedaInicial=list(filter(lambda x: x[0][0]==source and exchanges[0]==x[0][4],vectorTransactions))
        #print("TODOS LOS POSIBLES TRADE PARA "+source+":")
        #print(vectorFiltradoMonedaInicial)
        if len(vectorFiltradoMonedaInicial)>0:
            #print("TRADE ELEGIDO PARA " + source + ":")
            #print(vectorFiltradoMonedaInicial[0])
            return vectorFiltradoMonedaInicial[0]
        else:

            return []



def transaccionesOptimas(listaDeExchange,inicio,cantidad):

    exchangesConErrores=['anxpro', 'bcex', 'bibox', 'binance', 'btctradeim', 'btcturk', 'coingi', 'coinmarketcap', 'coolcoin', 'coss', 'dsx', 'fcoin', 'fcoinjp', 'flowbtc', 'kkex', 'stronghold', 'theocean', 'vaultoro', 'whitebit', 'xbtce','livecoin', 'stex']
    exchangesSinErrores=['_1btcxe', 'acx', 'aofex', 'bequant', 'bigone', 'binanceje', 'binanceus', 'bit2c', 'bitbank', 'bitbay', 'bitfinex', 'bitfinex2', 'bitflyer', 'bitforex', 'bithumb', 'bitkk', 'bitmart', 'bitmax', 'bitmex', 'bitso', 'bitstamp', 'bitstamp1', 'bittrex', 'bitz', 'bl3p', 'bleutrade', 'braziliex', 'btcalpha', 'btcbox', 'btcmarkets', 'btctradeua', 'buda', 'bw', 'bybit', 'bytetrade', 'cex', 'chilebit', 'coinbase', 'coinbaseprime', 'coinbasepro', 'coincheck', 'coinegg', 'coinex', 'coinfalcon', 'coinfloor', 'coinmate', 'coinone', 'coinspot', 'crex24', 'deribit', 'digifinex', 'exmo', 'exx', 'foxbit', 'ftx', 'fybse', 'gateio', 'gemini', 'hbtc', 'hitbtc', 'hollaex', 'huobipro', 'huobiru', 'ice3x', 'idex', 'independentreserve', 'indodax', 'itbit', 'kraken', 'kucoin', 'kuna', 'lakebtc', 'latoken', 'lbank', 'liquid', 'luno', 'lykke', 'mercado', 'mixcoins', 'oceanex', 'okcoin', 'okex', 'paymium', 'poloniex', 'probit', 'rightbtc', 'southxchange', 'surbitcoin', 'therock', 'tidebit', 'tidex', 'timex', 'topq', 'upbit', 'vbtc', 'yobit', 'zaif', 'zb']


    #print(listaDeExchange)
    puertoTor=-1
    tiempo = time.perf_counter()
    listaExcluidos = []
    try:
        vectorTransactions =consultarCamino(listaDeExchange, inicio, cantidad, False)

        tiempo = time.perf_counter() - tiempo

        #print("Tiempo de Busqueda: " + str(round(tiempo, 2)) + "seg")
        profit=0
        if vectorTransactions!=[]:
            profit=vectorTransactions[-1][3]-cantidad
            #print("Profit Estimado: "+str(profit)+ " "+inicio)



        return vectorTransactions, profit
    except:
        print("Error conseguir camino")

        return [],0



'''monto=0.001
origen="BTC"

profitPorcent=0
vectorTransactions,profit=transaccionesOptimas(['kraken','bittrex'],"BTC",monto)
profitPorcent=profit*100/monto
while profitPorcent<10:
    vectorTransactions,profit=transaccionesOptimas(['kraken','bittrex'],"BTC",monto)
    time.sleep(3)
    profitPorcent = profit * 100 / monto
    print(".",end="")
print("ProfitPorcent: "+str(profitPorcent),end="")
print(" Se Encontro profitPorcent:"+str(profitPorcent)+" Transacciones "+ str(vectorTransactions))'''