from math import *
import paho.mqtt.client as mqtt
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
# define characteristics of the system
points = 10
d = 1
L = [d, d]


def publish(angles):
    msg = str(angles)
    # msg = "(100,10)"
    print(msg)
    client.publish(topic, msg)
    time.sleep(.4)
    print("published: %s successfully." % msg)


def solve(x, y):
    theta_avg = (atan2(y, x) * 360 / 2 / pi)
    r = sqrt(x**2 + y**2)
    # print(x, y)
    # print(theta_avg)
    # print(r)
    cosB = (L[0] ** 2 + L[1] ** 2 - r ** 2) / (2 * L[0] * L[1])
    beta = atan2(sqrt(1 - cosB ** 2), cosB) * 360 / 2 / pi
    theta_2 = 180 - beta

    theta_1 = (2 * theta_avg - theta_2) / 2
    angles = (theta_1, theta_2)

    # print(angles)
    x_1 = L[0] * cos(theta_1 * 2 * pi / 360)
    y_1 = L[0] * sin(theta_1 * 2 * pi / 360)
    plt.plot([0, x_1], [0, y_1], color='red')  # Add a red line

    x_2 = L[1] * cos((theta_1 + theta_2) * 2 * pi / 360) + x_1
    y_2 = L[1] * sin((theta_1 + theta_2) * 2 * pi / 360) + y_1
    plt.plot([x_1, x_2], [y_1, y_2], color='red')  # Add a red line
    return angles


list_of_positions = [(d + d/2 * cos(i * 2 * pi / 360), d/2 * sin(i * 2 * pi / 360)) for i in range(0, 360, int(360/points))]
x, y = zip(*list_of_positions)

fig, ax = plt.subplots()
ax.scatter(x, y, vmin=0, vmax=100)

ax.set(xlim=(0, d * 2), ylim=(-d, d))

broker_address = "67.253.32.232"
topic = "ME035"

client = mqtt.Client("THE SCRAMBLER")
client.connect(broker_address)
# while True: # definitely not my light spamming code...
#     for i in range(10):
#         client.publish("light", str(i))
#         time.sleep(.1)

for p in list_of_positions:
    angles = solve(p[0], p[1])
    publish(angles)
plt.show()

client.disconnect()
