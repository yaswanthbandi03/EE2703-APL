import numpy as np
import scipy.signal as sp                                             # Scipy.signal module contains the functions helps us in solving the LTI sytems   
from pylab import *                                                   # Such as bilateral and inverse fourier transform , convolution , impulse response 

# Question_1
# Finding the reponse for sinusoidal exponential decaying forced input for the spring equation with its natural frequency as 1.5rad/sec 

F1 = sp.lti([1,0.5],[1,1,2.5])                                        # Defining the laplace transform of input
X1 = sp.lti([1,0.5],[1,1,4.75,2.25,5.625])                            # Defining the laplace transform of the output
                                                                      
t,x1 = sp.impulse(X1,None,linspace(0,50,501))                         # Finding the time domain output by applying inverse laplace using sp.impulse
                                             
figure(0)                                                             # plotting the output response
plot(t,x1) 
xlabel(r'$t$')
ylabel(r'$x(t)$')
title(r' $x(t)$ vs $t$ for decay rate 0.5/sec - Question_1')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "-") 


# Question_2
# Recuding the Decay constant of the input

F2 = sp.lti([1,0.05],[1,0.1,2.2525])                                  # Defining the laplace transform of new input
X2 = sp.lti([1,0.05],[1,0.1,4.5025,0.225,5.068125])

t,x2 = sp.impulse(X2,None,linspace(0,50,501))                         # Finding the time domain output by applying inverse laplace using sp.impulse

figure(1)                                                             # plotting the output response
plot(t,x2)
xlabel(r'$t$')
ylabel(r'$x(t)$')
title(r' $x(t)$ vs $t$ for decay rate 0.05/sec - Question_2')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "-") 


# Question_3

H = sp.lti([1],[1,0,2.25])                                            # Defining the System transfer function   
dec = linspace(1.4,1.6,5)                                             # Set of cosine frequencies 

figure(2)                           
for i in dec:
    p = i*i + 0.0025
    F = sp.lti([1,0.05],[1,0.1,p])                                    # Defining the input laplace transform 
    t,f = sp.impulse(F,None,linspace(0,50,501))                       # Finding the input time domain equation
    t,y,svec = sp.lsim(H,f,t)                                         # Finding the Output by convolving the impulse response with the input using sp.lsim
    plot(t,y,label = 'freq = '+str(i)+' ')                            # plotting all responses in single plot with labels


xlabel(r'$t$')
ylabel(r'$y(t)$')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "-") 
title(r'Responses for different frequency inputs - Question_3')
legend()    
   
#Question 4
# We are given two set of equations, we have to solve those equations in s domain and convert it into time domain
#function x in laplace domain
X4 = sp.lti([1,0,2],[1,0,3,0])
#function of y in laplace domain
Y4 = sp.lti([2],[1,0,3,0])
#In time domain
t4,x4 = sp.impulse(X4,None,linspace(0,20,500))
t4,y4 = sp.impulse(Y4,None,linspace(0,20,500))
#plot
figure(3)
plot(t4,x4,label='x(t)')
plot(t4,y4,label='y(t)')
title("x(t) and y(t)")
xlabel(r'$t\rightarrow$')
ylabel(r'$functions\rightarrow$')
legend(loc = 'upper right')
plt.grid(True)

# Question_5
# TWO Port RLC network

R = 100                                                               # Default values for R,L,C
L = 10**(-6)
C = 10**(-6)

H5 = sp.lti([1],[L*C,R*C,1])                                          # Defining the system transfer function

w,S,phi = H5.bode()                                                   # Findiing the magnitude and phase response of the system transfer function using the system.bode()

figure(4)                                                             # plotting the magnitude response on the semilogx plot
plt.semilogx(w,S)
xlabel(r'$w$')
ylabel(r'$|H(s)|$')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "-") 
title(r'Magnitude_Response - Question_5')

figure(5)                                                             # plotting the phase response on the semilogx plot
plt.semilogx(w,phi)
xlabel(r'$w$')
ylabel(r'Phase$(H(s))$')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "-") 
title(r'Phase_Response - Question_5')

    
# Question_6
# Response for sinusoidal input of RLC network 
# It acts as an Low-Pass filter 

H5 = sp.lti([1],[L*C,R*C,1])                                          # System transfer function for RLC network 


t2 = linspace(0,0.01,(10**5+1))                                       # Time for 0<t<10 milli seconds
vi = np.cos(1000*t2)-np.cos((10**6)*t2)                               # Input to the system 
t2,vo,svec = sp.lsim(H5,vi,t2)                                        # Finding the output for 0<t<10ms 

t3 = linspace(0,0.00003,1001)                                         # Time for 0<t<30 micro seconds
vi1 = np.cos(1000*t3)-np.cos((10**6)*t3)
t3,vo1,svec = sp.lsim(H5,vi1,t3)                                      # Finding the output for 0<t<30us

figure(6)                                                             # plotting output and observing the steady state response
plot(t2,vo)
xlabel(r'$t$')
ylabel(r'V_output')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "-") 
title(r'steady state Output of network - Question_6')

figure(7)                                                             # plotting output and observing the steady state response 
plot(t3,vo1)
xlabel(r'$t$')
ylabel(r'V_output')
plt.grid(True, color = "grey", linewidth = "1.4", linestyle = "-") 
title(r'Output of network for T<30usec:Transient_response - Question_6')
show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

