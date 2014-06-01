'''
Created on 16.04.2014

@author: martin
'''
from numpy import *
from uncertainties import ufloat
from uncertainties.umath import *
import matplotlib.pyplot as plt


def make_LaTeX_table(data,header, flip= 'false', onedim = 'false'):
    output = '\\begin{table}\n\\centering\n\\begin{tabular}{'
    #Get dimensions
    if(onedim == 'true'):
        if(flip == 'false'):
        
            data = array([[i] for i in data])
        
        else:
            data = array([data])
    
    row_cnt, col_cnt = data.shape
    header_cnt = len(header)
    
    if(header_cnt == col_cnt and flip== 'false'):
        #Make Format
        
        for i in range(col_cnt):
            output += 'S'
        output += '}\n\\toprule\n{'+ header[0]
        for i in range (1,col_cnt):
            output += '} &{ ' + header[i]
        output += ' }\\\\\n\\midrule\n'
        for i in data:
            if(isinstance(i[0],(int,float,int32))):
                output += str( i[0] )
            else:
                output += ' ${:L}$ '.format(i[0])
            for j in range(1,col_cnt):
                if(isinstance(i[j],(int,float,int32))):
                    output += ' & ' + str( i[j])
                else:
                    output += ' & ' + str( i[j]).replace('/','')
                
            output += '\\\\\n'
        output += '\\bottomrule\n\\end{tabular}\n\\label{}\n\\caption{}\n\\end{table}\n'
                            
        return output

    else:
        return 'ERROR'



    
def err(data):
    mean = data.mean()
    N = len(data)
    err = 0
    for i in data:
        err += (i - mean)**2
    err = sqrt(err/((N-1)*N))
    return ufloat(mean,err)


def lin_reg(x,y):
    N = len(x)
    sumx = x.sum()
    sumy = y.sum()
    sumxx = (x*x).sum()
    sumxy = (x*y).sum()
    m = (sumxy - sumx*sumy/N)/(sumxx- sumx**2/N)
    b = sumy/N - m*sumx/N
    
    sy = sqrt(((y - m*x - b)**2).sum()/(N-1))
    m_err = sy *sqrt(N/(N*sumxx - sumx**2))
    b_err= m_err * sqrt(sumxx/N)
    return ufloat(m,m_err), ufloat(b,b_err)
    
    
# Auswertung Teil A
# Messwerte einlesen
t, n, u, i = loadtxt("dataA.txt", unpack=True)
# Relevante Werte berechnen
sigman = n**(0.5)
sigmaI = sigman/t
I = n/t
sigmaIrel = sigmaI/I

# Erster Plot
plt.xlim(290,710)
plt.ylim(-1,62)
plt.xlabel('Zaehlrohrspannung U[V]')
plt.ylabel('Impulsrate I [1/s]')
plt.errorbar(u,I,yerr=sigmaI,xerr=None,fmt=None,ecolor='red')
plt.plot(u,I,'.')
plt.show()
plt.savefig("plot1.png")
plt.close()

# Zweiter Plot (Regressionsgerade)
u2=u[2:] 
I2=I[2:]
sigmaI2=sigmaI[2:]
m,b = lin_reg(u2,I2)

plt.xlim(300,710)
plt.xlabel('Zaehlrohrspannung U[V]')
plt.ylabel('Impulsrate I [1/s]')
plt.errorbar(u2,I2,yerr=sigmaI2,xerr=None,fmt=None,ecolor='red')
plt.plot(u2,I2,'.')
plt.plot(x,x*m.n+b.n)
plt.show()
plt.savefig("plot2.png")
plt.close()

# Berechnung des Anstiegs
deltaU=700-340
print "Aufgabenteil A:"
print "delta U:"
print deltaU
Iunten=m*340+b
print "I340:"
print I340
Ioben=m*700+b
print "I700:"
print I700
mPro=(((Ioben/Iunten)-1)*100)/(deltaU/100)
print "m in Prozent/100V"
print mPro


#plt.plot(x,x*m.n+b.n)






"""  

laengenD=array([laengeZA,laengeZB,laengeZC])
zeitenD=array([tdZA,tdZB,tdZC])
m3, b3 = lin_reg(laengenD,zeitenD)
print "m und b aus linearer Regression der 2 MHz Sonde: m=%s, b=%s" % (m3,b3)
plt.plot([laengeZA,laengeZB,laengeZC],[tdZA,tdZB,tdZC],'x')

x=linspace(0,0.25)

plt.plot(x,x*m3.n+b3.n) ## Hier musst du als erstes Argument nocheinmal 'x' angeben !!!!! 


plt.xlabel("Zylinderlaenge [m]")
plt.ylabel("Laufzeit [10^(-6)sec]")
plt.xlim(0, 0.25)
plt.ylim(0, 0.0001)
plt.savefig("Fig3.png")
plt.close() # Hiermit wird die Zeichung nach dem speichern resettet

"""

