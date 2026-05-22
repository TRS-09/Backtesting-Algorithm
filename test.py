import matplotlib.pyplot as plt

xvalues = [1000]
for i in range(0,10):
    xvalues.append(xvalues[i]*(1.05))

plt.plot(xvalues)
plt.show()