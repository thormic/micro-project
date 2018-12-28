
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    
probability_show = 0.935
nb_seats = 100
revenue_per_seat = 350.0 # USD
voucher_cost = revenue_per_seat * 2.0 # USD
nb_flights = 10000
max_overbooking = 15

revenue = np.zeros((nb_flights, max_overbooking))



for tix_overbooked in range(0, max_overbooking):
    nb_tickets_sold = nb_seats + tix_overbooked
    for f in range(0, nb_flights): # simulate nb_flights flights
        revenue[f][tix_overbooked] = simulate_net_revenue(nb_tickets_sold, nb_seats, probability_show, revenue_per_seat, voucher_cost)
    
print(revenue)

plt.boxplot(revenue)
plt.show() 

type(revenue)
revenue.shape
