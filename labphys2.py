from math import sqrt, tan, pi, atan
from mpmath import csc
import sys

t_beta = [ 12.71, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.160, 2.145, 2.131,
           2.120, 2.110, 2.101, 2.093, 2.086, 2.080, 2.074 ]

t_beta_inf = 1.960


def error_calculation(l_values, device_err, el=False):
    if not el:
        device_err /= 2
    n = len(l_values)

    t_beta_n = t_beta[ n - 2 ]

    avg = sum(l_values) / n

    t = sum([ (i - avg) ** 2 for i in l_values ])

    std_err = sqrt(t / (n ** 2 - n))

    rnd_err = std_err * t_beta_n

    msr_err = device_err * t_beta_inf / 3

    abs_err = sqrt(rnd_err ** 2 + msr_err ** 2)

    rel_err = abs_err / avg
    return f"avg:{avg}\n sx:{std_err}\n rnd_err:{rnd_err}\n device_err:{device_err}\n msr_err:{msr_err}\n abs_err:{abs_err}\n rel_err:{round(rel_err * 100, 4)}%\n "


U = [ 108, 120, 160, 186, 134, 170, 232, 118, 130 ]
I = list(map(lambda x: x / 1000, [ 40, 44, 59, 69, 49, 62, 86, 41, 46 ]))

f = 50.2
R_coil = 861
delta_f = 0.3
delta_I = 0.5/1000
delta_U = 0.5
delta_R = 0.1
I_exp=[]
with open("lab.docx", "w") as file:
    for i, j in enumerate(U):
        tmp = j / I[ i ]
        L = tmp / (2 * pi * 50.2)
        delta_Lu = delta_U / (2 * pi * f * I[ i ])
        delta_Li = -(j * delta_I) / (2 * pi * f * I[ i ] * I[ i ])
        delta_Lf = -(j * delta_f) / (2 * pi * f * f * I[ i ])
        delta_L = sqrt(delta_Lf ** 2 + delta_Li ** 2 + delta_Lu ** 2)

        rel_err = delta_L / L
        Xl = 2 * pi * f * L
        fi = atan(Xl / R_coil)
        I_exp.append(j / sqrt(Xl ** 2 + R_coil ** 2))
        file.write(f"L{i+1}={round(L,4)}+-{round(delta_L,4)} Henry, epsilon={round(rel_err*100,4)}%, ")
        file.write(f"fi{i + 1}={round(fi,4)}\n\n")
    for i,j in enumerate(I):
        file.write(f"Experimental I{i+1}={round(I_exp[i]*1000,4)} mA; Measured I{i+1}={round(j*1000,4)} mA; difference{round(abs(I_exp[i]-j)*1000,4)} mA\n\n")

