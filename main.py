import parse
import numpy as np
import matplotlib.pyplot as plt

fname = input("Input Filename: ")
title = input("The title name: ")
type = input("Bq?: ")
time = float(input("How long are you staying inside a year?: "))
if(type == "y"):
    cov = 1
else:
    cov = 37
f = open(fname, 'r')
lines = f.read().splitlines()
epp = 0.027 * 1.17 * (10 ** -17) * 6.242 * (10 ** 12) * 3600

total_energy = 0
total_yef = 0
weigh_f = 0.12
mass = 1.0
max = 0.0
min = 10000.0
Energy = []
yef = []
for i in range(len(lines)-6):
    Energy.append(float(parse.parsetext(lines[i+6])[2]) * cov)
    yef.append(parse.getefdose(float(parse.parsetext(lines[i+6])[2]), time))
    if Energy[i] > max:
        max = Energy[i]
    if Energy[i] < min:
        min = Energy[i]
    total_energy += Energy[i]
    total_yef += yef[i]

avg = total_energy / len(Energy)
avg_ef = total_yef / len(yef)
variance = sum((x - avg) ** 2 for x in Energy) / len(Energy)
var_ef = sum((x - avg_ef) ** 2 for x in yef) / len(yef)
# Trend line for energy
std_dev = np.sqrt(variance)
x = np.arange(len(Energy))
coefficients = np.polyfit(x, Energy, 1)
linear_fit = np.poly1d(coefficients)

# Trend line for effective dose
std_dev_ef = np.sqrt(var_ef)
x_yef = np.arange(len(yef))
coef_ef = np.polyfit(x, yef, 1)
linfit_ef = np.poly1d(coef_ef)

avg_ef = parse.getefdose(avg, time)
max_ef = parse.getefdose(max, time)
min_ef = parse.getefdose(min, time)
print(avg)
plt.rcParams['font.family'] ='Nanum Gothic'
plt.rcParams['axes.unicode_minus'] =False
fig, ax1 = plt.subplots()
ax1.plot(Energy)
ax1.plot(x, linear_fit(x), label='Linear Fit', linestyle='--', color='red')
ax2 = ax1.twinx()
ax1.text(0.01, 0.5, 'Bq/m³', verticalalignment='center', horizontalalignment='left', 
        transform=ax1.transAxes, fontsize=12)
ax1.text(0.99, 0.5, 'pCi', verticalalignment='center', horizontalalignment='right', 
        transform=ax1.transAxes, fontsize=12)
ax1.text(0.5, -0.1, 'Time(in Hours)', verticalalignment='center', horizontalalignment='center', 
        transform=ax1.transAxes, fontsize=12)
ax2.set_ylim(ax1.get_ylim()[0] / 37, ax1.get_ylim()[1] / 37)

efdose = avg * time * avg * 0.4 * (8 * (10 ** -9))
print(f"The yearly effective dose is: {efdose} mSv/year")
plt.text(0, 1, f"최고값: {max}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left')
plt.text(0, 0.95, f"최소값: {min}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left')
plt.text(0, 0.90, f"평균: {avg}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left')
plt.title(f"{title}의 라돈농도")
plt.grid()
plt.show()
# Make a new graph with yearly effective dose calculated with each radon data
plt.plot(yef)
plt.plot(x_yef, linfit_ef(x_yef), label="Trend lines", linestyle='--', color='red')
plt.title(f"{title}의 연간유효선량")
plt.xlabel("Time(In hours)")
plt.ylabel("Yearly effective dose(mSv/yr)")
plt.text(0, 1, f"최고값: {max_ef}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left')
plt.text(0, 0.95, f"최소값: {min_ef}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left')
plt.text(0, 0.90, f"평균: {avg_ef}", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='left')
plt.grid()
plt.show()
f.close()