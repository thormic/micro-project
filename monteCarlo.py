import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def monteCarlo (probabilityShow = 0.935, nbSeats = 100, revenuePerSeat = 450.0,
                nbFlights = 10000, maxOverbooking = 16, interDomestic = 0):

    def show_up(probabilityShow):
        if random.random() <= probabilityShow:
            return True
        else:
            return False

    def simulate_flight(nb_tickets_sold, probabilityShow):
        n = 0 # number of people who bought tix that will show up
        for i in range(0,nb_tickets_sold):
            if show_up(probabilityShow):
                n = n + 1
        return n

    def simulate_net_revenue(nb_tickets_sold, nbSeats,
                             probabilityShow, revenuePerSeat, voucher_cost):
        # how many ticket purchasers actually showed up?
        nb_shows = simulate_flight(nb_tickets_sold, probabilityShow)
        # no one bumped from flight if less or equal people show up than for
        #   the number of seats we have
        if nb_shows <= nbSeats:
            return revenuePerSeat * nb_shows
        # if more customers show up than seats we have, must pay out vouchers
        else:
            vouchers_out = nb_shows - nbSeats
            return nbSeats * revenuePerSeat - voucher_cost * vouchers_out


    voucher_cost = revenuePerSeat * 2.0 # USD

    revenue = np.zeros((nbFlights, maxOverbooking))

    for tix_overbooked in range(0, maxOverbooking):
        nb_tickets_sold = nbSeats + tix_overbooked
        for f in range(0, nbFlights): # simulate nbFlights flights
            revenue[f][tix_overbooked] = simulate_net_revenue(nb_tickets_sold,
                                                              nbSeats,
                                                              probabilityShow,
                                                              revenuePerSeat,
                                                              voucher_cost)

    # print(revenue)

    # f, ax = plt.subplots()
    # l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    # ax.boxplot(revenue)
    # ax.set_xticklabels(l)
    # plt.show()


    col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    index = range(10000)
    df = pd.DataFrame(data=revenue[0:,0:], index=index, columns=col)

    maxValue = max(df.mean())
    dictionary = dict(df.mean())

    for keys, values in dictionary.items():
        if (values == maxValue):
            print(keys)

monteCarlo()
