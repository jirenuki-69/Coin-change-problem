import os

def make_denoms():
    n = int(input('Ingrese la cantidad de denominaciones que tendrá: '))
    count = []
    coins = []
    coins2 = []
    for i in range(n):
        coin = int(input('Ingrese la denominación: '))
        coins2.append(coin)
        n2 = int(input('Ahora ingrese la cantidad de repeticiones que tendrá la denominación {}: '.format(coin)))
        count.append(n2)
        for j in range(n2):
            coins.append(coin)
    return coins, count, coins2

def greedy_coin_change(monedas, cambio):
    monedas = sorted(monedas, reverse = True)
    solucion = []
    for i in monedas:
        if i <= cambio:
            solucion.append(i)
            cambio -= i
        else:
            continue
        if cambio == 0:
            break
    if not cambio == 0:
        return None
    return solucion

def make_values(monedas):
    monedas = sorted(monedas)
    coins = []
    count = []
    for i in monedas:
        if i not in coins:
            coins.append(i)
            count.append(1)
        else:
            count[coins.index(i)] += 1
    values = [{} for i in range(len(coins))]
    for i in range(len(coins)):
        values[i] = {'Value': coins[i], 'Count': count[i]}
    return values

def recursiveCoinChange(monedas, cambio, indice = 0, cont = 0, minimun = None):
    global iter
    iter += 1
    if cambio == 0:
        if minimun == None or cont < minimun:
            minimun = cont
            return []
        else:
            return None
    if indice >= len(monedas):
            return None
    optimo = None
    coin = monedas[indice]
    puedoTomar = min(cambio // coin['Value'], coin['Count'])
    for i in range(puedoTomar, -1, -1):
        total = recursiveCoinChange(monedas, cambio - coin['Value'] * i, indice + 1, cont + i, minimun)
        if total != None:
            if i:
                total.append({'Value': coin['Value'], 'Count': i})
            optimo = total
    return optimo

def makeSolution(solucion):
    output = []
    for i in solucion:
        for j in range(i['Count']):
            output.append(i['Value'])
    return output

def createTable(n, denoms):
    table = [[] for i in range(len(denoms))]
    for i in range(n + 1):
        table[0].append(i)
    for i in range(1, len(denoms)):
        for j in range(denoms[i]):
            table[i].append(table[i - 1][j])
        table[i].append(1)
        for j in range(denoms[i] + 1, n + 1):
            table[i].append(1 + (table[i][j - denoms[i]]))

    return table

def dynamicCoinChange(table, n, denoms, count, coin = []):
    global iter
    iter += 1
    if n == 0:
        return
    min = table[0][n]
    new_change = [None for i in range(len(denoms))]
    for i in range(len(table)):
        if table[i][n] <= min and denoms[i] <= n and count[i] > 0  and (count[i] + count[i - 1] >= table[i][n]):
            if table[i][n] < min:
                min = table[i][n]
                for j in range(len(new_change)):
                    new_change[j] = None
                new_change[denoms.index(denoms[i])] = denoms[i]
            elif table[i][n] == min:
                new_change[denoms.index(denoms[i])] = denoms[i]
    for i in range(len(new_change)):
        if new_change[i] != None:
            coin.append(denoms[i])
            dynamicCoinChange(table, n - denoms[i], denoms, count, coin)
        else:
            continue
    return coin

n = int(input('Ingrese el dinero a cambiar: '))
denominaciones, count, denoms = make_denoms()
os.system('cls')
solucion = greedy_coin_change(denominaciones, n)
iter = 0
table = createTable(n, denoms)

if solucion != None:
    print(f'\t*** SOLUCIÓN GREEDY *** \n{solucion}')
    print(f'La solución greedy ofrece un cambio con un total de {len(solucion)} monedas')
else:
    print('No se pudo hallar un cambio en greedy')

coins = make_values(denominaciones)

solucion = recursiveCoinChange(coins, n)

if solucion != None:
    solucion = makeSolution(solucion)
    print(f'\t*** SOLUCIÓN RECURSIVA *** \n{solucion}')
    print(f'La cantidad mínima utilizada es de {len(solucion)} monedas')
    print(f'{iter} Llamadas')
else:
    print('No se pudo hallar un cambio en recursiva')

iter = 0
solucion = dynamicCoinChange(table, n, denoms, count)
if solucion != []:
    print(f'\t*** SOLUCIÓN DINÁMICA *** \n{solucion}')
    print(f'{iter} Llamadas')
else:
    print('No hay cambio posible por dar en dinámica')
