from pylab import *
import numpy as np

# Defining all the parameters mentioned in the question paper.

l = 0.5; c = 2.9979e8; mu0 = 4e-7*pi;Im = 1.0; a = 0.01
N=4; lam = l*4; f = c/lam; k = 2*pi/lam; dz = l/N

# Defining the locations of all known and unknown currents.

z = linspace(-l, l, 2 * N + 1)
print((z).round(2))

# Defining an array containing the locations of all unknown currents.

u = delete(z, [0, N, 2 * N])
print((u).round(2))

# Defining a function which computes and returns a matrix to be used in solving the Ampere's Law

def M(N, a):
    M = (1 / (2 * pi * a)) * identity(2 * N - 2)
    return M
print((M(N, a)).round(2))

#Creating vectors Rz and Ru

Rz = zeros([2*N+1,2*N+1])
Ru = zeros([2*N-2,2*N-2])
i =0;j=0

# Defining matrix Rz which contains the distances between all the known and unknown current locations

while i<2*N+1:
    while j<2*N+1:
        Rz[i][j] = sqrt(a**2 + (z[i]-z[j])**2)
        j+=1    
    i+=1
    j=0
i = 0;j=0
print(Rz.round(2))

# Defining matrix Ru whcih contains only the distances between unknown current locations.

while i<2*N-2:
    while j<2*N-2:
        Ru[i][j] = sqrt(a**2 + (u[i]-u[j])**2)
        j+=1    
    i+=1
    j=0
print(Ru.round(2))

#Defining vectors P_B and and P
 
P_B = zeros(2*N +1,dtype="complex_")
P = zeros([2*N-2,2*N-2],dtype="complex_")
i = 0
while i<2*N +1:
    P_B[i] = ((mu0/(4*pi))*(complex(cos(k*Rz[i][N]),-sin(k*Rz[i][N])))*dz)/Rz[i][N]
    i +=1
P_B1 = P_B
P_B = delete(P_B,N)
P_B = P_B[1:-1]
print((P_B * 1e8).round(2))

i=0;j=0
while i<2*N-2:
    while j<2*N-2:
        P[i][j] = ((mu0/(4*pi))*(complex(cos(k*Ru[i][j]),-sin(k*Ru[i][j])))*dz)/Ru[i][j]
        j+=1    
    i+=1
    j=0
print((P * 1e8).round(2))

# Computing the matrices P and Pb using the vector potential to current relation.

j = 1j
RN = delete(Rz[N], [0, N, 2 * N])
print(RN.round(2))

# Computing the matrices Q and Qb  from the magntic field to current relation.

Q = -(a / mu0) * P * ((-k * j / Ru) + (-1 / Ru ** 2))
print((Q).round(2))

Qb = -(a / mu0) * P_B * ((-k * j / RN) + (-1 / RN ** 2))
print((Qb).round(2))

# Obtaining the currents at unknown location by solving the matrix equation.

J = inv(M(N, a) - Q) @ Qb * Im
print((J).round(2))

# Defining array containing current at all locations.

I = concatenate(([0], J[: N - 1], [Im], J[N - 1 :], [0]))
print((I).round(2))

# Sinusoidal distribution assumption of current.

Ia = concatenate((Im * sin(k * (l - z[:N])), Im * sin(k * (l + z[N:]))))
print((Ia).round(2))

figure()
plot(z, abs(I), lw=2, label="Calculated value ")
plot(z, abs(Ia), lw=2, label="Sinusoidal approximation")
xlabel(r"$z$")
ylabel(r"$I$")
title("Calculated value of current")
legend(loc="upper right")
grid()

show()

