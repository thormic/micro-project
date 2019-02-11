import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
for analysis:
- change isEU parameter
- change arbitrarily isDomestic parameter
- change nbSeats
- change nbFlights
- change isSmallFlight
- play with probabilities
'''

def monteCarlo (probabilityShowDomestic = 0.9, probabilityShowInter = 0.9375,
                nbSeats = 100, revenuePerSeat = 450.0, nbFlights = 10000,
                maxOverbooking = 16, probabilityDomestic = 6/7, isEU = False,
                isSmallFlight = True, isDomestic = None):

    def isDomestic(probabilityDomestic, isDomestic):
        if isDomestic is None:
            return random.random() <= probabilityDomestic
        else:
            return isDomestic

    def show_up(probabilityShowDomestic, probabilityShowInter):
        if isDomestic(probabilityDomestic, isDomestic):
            return random.random() <= probabilityShowDomestic
        else:
            return random.random() <= probabilityShowInter

    def simulate_flight(nb_tickets_sold, probabilityShowDomestic, probabilityShowInter):
        n = 0 # number of people who bought ticket that will show up
        for i in range(0,nb_tickets_sold):
            if show_up(probabilityShowDomestic, probabilityShowInter):
                n = n + 1
        return n

    def simulate_net_revenue(nb_tickets_sold, nbSeats, probabilityShowDomestic,
                             probabilityShowInter, revenuePerSeat, voucherCost):
        # how many ticket purchasers actually showed up?
        nb_shows = simulate_flight(nb_tickets_sold, probabilityShowDomestic, probabilityShowInter)
        # no one bumped from flight if less or equal people show up than for
        #   the number of seats we have
        if nb_shows <= nbSeats:
            return revenuePerSeat * nb_shows
        # if more customers show up than seats we have, must pay out vouchers
        else:
            vouchers_out = nb_shows - nbSeats
            return nbSeats * revenuePerSeat - voucherCost * vouchers_out

    if isEU:
        if isSmallFlight:
            voucherCost = 453.42 # USD = 400 EUR
        else:
            voucherCost = 680.13 # USD = 600 EUR
    else:
        if isSmallFlight:
            voucherCost = min(revenuePerSeat * 2.0, 675) #USD
        else:
            voucherCost = min(revenuePerSeat * 2.0, 1350) #USD

    revenue = np.zeros((nbFlights, maxOverbooking))

    for tix_overbooked in range(0, maxOverbooking):
        nb_tickets_sold = nbSeats + tix_overbooked
        for f in range(0, nbFlights): # simulate nbFlights flights
            revenue[f][tix_overbooked] = simulate_net_revenue(nb_tickets_sold,
                                                              nbSeats,
                                                              probabilityShowDomestic,
                                                              probabilityShowInter,
                                                              revenuePerSeat,
                                                              voucherCost)

    # print(revenue) # ? print revenue matrix

    plt.style.use('bmh')
    f, ax = plt.subplots()
    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    plt.ylabel('Profit')
    plt.xlabel('Overbooked tickets')
    ax.boxplot(revenue)
    ax.set_xticklabels(l)
    plt.show()

    index = range(10000)
    df = pd.DataFrame(data=revenue[0:,0:], index=index, columns=l)

    maxValue = max(df.mean())
    dictionary = dict(df.mean())

    # dict_var = dict(df.var())

    for keys, values in dictionary.items():
        if (values == maxValue):
            print(keys, values)

    # for keys, values in dict_var.items():
    #     print(keys, values)

    # print(np.mean(df.var()))

    df_var = pd.DataFrame(df.var())
    f, ax = plt.subplots()
    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    plt.ylabel('Variance')
    plt.xlabel('Overbooked tickets')
    ax.plot(df_var)
    plt.xlim(0,15)
    plt.tight_layout()
    plt.show()

import time
start = time.time()

# ? first simulation EU, domestic and international
monteCarlo(isEU = True) # 11 overbooked tickets

# ? second simulation US, domestic and international
# monteCarlo() # 10 overbooked tickets

# ? third simulation US, domestic,revenue = 100
# monteCarlo(isDomestic = True, revenuePerSeat = 100) # 9 tickets

# ? fourth simulation EUR, international, long, revenue = 700
# monteCarlo(isEU = True, isSmallFlight=False, isDomestic=False, revenuePerSeat=700)

end = time.time()
print("time passed: ", end - start)
