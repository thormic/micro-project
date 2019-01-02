import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def monteCarlo (probabilityShow = 0.935, nbSeats = 100, revenuePerSeat = 450.0, nbFlights = 10000, maxOverbooking = 16):

    def show_up(probability_show):
        if random.random() <= probability_show:
            return True
        else: 
            return False 

    def simulate_flight(nb_tickets_sold, probability_show):
        n = 0 # number of folks who bought tix that will show up
        for i in range(0,nb_tickets_sold):
            if show_up(probability_show):
                n = n + 1
        return n

    def simulate_net_revenue(nb_tickets_sold, nb_seats, 
                            probability_show, revenue_per_seat, voucher_cost):
        # how many ticket purchasers actually showed up?
        nb_shows = simulate_flight(nb_tickets_sold, probability_show)
        # no one bumped from flight if less or equal folks show up than for
        #   the number of seats we have
        if nb_shows <= nb_seats:
            return revenue_per_seat * nb_shows
        # if more customers show up than seats we hv, must pay out vouchers
        else:
            vouchers_out = nb_shows - nb_seats
            return nb_seats * revenue_per_seat - voucher_cost * vouchers_out

    probability_show = probabilityShow
    nb_seats = nbSeats
    revenue_per_seat = revenuePerSeat # USD
    voucher_cost = revenue_per_seat * 2.0 # USD
    nb_flights = nbFlights
    max_overbooking = maxOverbooking

    revenue = np.zeros((nb_flights, max_overbooking))

    for tix_overbooked in range(0, max_overbooking):
        nb_tickets_sold = nb_seats + tix_overbooked
        for f in range(0, nb_flights): # simulate nb_flights flights
            revenue[f][tix_overbooked] = simulate_net_revenue(nb_tickets_sold, nb_seats, probability_show, revenue_per_seat, voucher_cost)
        
    # print(revenue)
    
    # f, ax = plt.subplots()
    # l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    # ax.boxplot(revenue)
    # ax.set_xticklabels(l)
    # plt.show()


for i in range(350, 500):
    monteCarlo(revenuePerSeat = i)


col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
index = range(10000)
df = pd.DataFrame(data=revenue[0:,0:], index=index, columns=col)
df.head(5)
df.tail(5)

df.describe()