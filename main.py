# -------------------------------- Imports ----------------------------------
import numpy as np                      # Autor: Adam Skóbel
import matplotlib.pyplot as plt         # Kierunek: Teleinformatyka
import math
from scipy import signal


# -------------------------------- Input Variables --------------------------
x1 = np.array([0, 1, 0, 1])                     # Dane użytkownika U1
x2 = np.array([1, 0, 0, 0])                     # Dane użytkownika U2
###
a1 = 0.75                                       # Waga mocy dla użytkownika U1
a2 = 0.25                                       # Waga mocy dla użytkownika U2
s1_t = math.sqrt(a1)                            # Współczynnik skalowania s1(t)
s2_t = math.sqrt(a2)                            # Współczynnik skalowania s2(t)
### a1 i a2 mają sumować się do 1 (REGUłA)


# -------------------------------- Other Variables --------------------------
N = 4                                           # Długość ciągu znaków dla danych x1 oraz x2
X_axis = []                                     # Tablica argumentów osi X dla każdego wykresu
x1_extended = []                                # Tablica rozszerzona dla argumentów tabeli x1
x2_extended = []                                # Tablica rozszerzona dla argumentów tabeli x2
x1_scaled = []                                  # Tablica dla wstępnie przeskalowanych argumentów tablicy x1_extended
x2_scaled = []                                  # Tablica dla wstępnie przeskalowanych argumentów tablicy x2_extended
s_scaled = []                                   # Tablica dla argumentów sygnału wchodzącego do kanału
s1_decoded = []                                 # Tablica będąca kontenerem na dane zdekodowane sygnału s1
s2_decoded = []                                 # Tablica będąca kontenerem na dane zdekodowane sygnału s2


# -------------------------------- Functions --------------------------------
# ========================== ENCODING ==========================
def bpsk_modulation():                          # Modulacja BPSK
    if (len(x1) or len(x2)) == 0:
        print("Array x1 or x2 is empty!")
    else:
        for i in range(N):
            x1[i] = x1[i] * 2 - 1
            x2[i] = x2[i] * 2 - 1
        print(f'BPSK modulation for user U1:  {x1}')
        print(f'BPSK modulation for user U2:  {x2}')
    print("\n")


# def generated_square_sign():                  # Testowy sygnał prostokątny
#     t = np.linspace(0, N, 200, endpoint=True)
#     plt.plot(t, signal.square(np.pi * t))
#     plt.show()


def arrays_extenction():                        # Generacja rozszerzonych tablic
    j = 0
    for i in range(N):
        X_axis.append(i)
        X_axis.append(i + 1)
        x1_extended.append(x1[j])
        x1_extended.append(x1[j])
        x2_extended.append(x2[j])
        x2_extended.append(x2[j])
        j += 1
    print(f'Extended X_axis: {X_axis}')
    print(f'Extended table x1_extended: {x1_extended} for table: x1')
    print(f'Extended table x2_extended: {x2_extended} for table: x2\n')


def plot():                                     # Generacja wykresów podstawowych
    fig, axs = plt.subplots(2)
    fig.suptitle('Plot of basic signals x1 (red) and x2 (blue)')
    fig.supxlabel('time (modulation cycles number)')
    fig.supylabel('Amplitude')
    axs[0].plot(X_axis, x1_extended, label="Signal x1 (user U1)", color='r')
    axs[0].grid(axis="x", linestyle=":", lw=1, color="black")
    axs[0].legend(loc='best')
    axs[1].plot(X_axis, x2_extended, label="Signal x2 (user U2)", color='b')
    axs[1].grid(axis="x", linestyle=":", lw=1, color="black")
    axs[1].legend(loc='best')
    plt.show()


def signal_scaling():                           # Skalowanie + konwersja na float
    for i in range(2 * N):
        x1_scaled.append(x1_extended[i] * (s1_t / 1.0))
        x2_scaled.append(x2_extended[i] * (s2_t / 1.0))
    for j in range(2 * N):
        s_scaled.append(x1_scaled[j] + x2_scaled[j])
    print(f'Early scaled x1_extended: {x1_scaled}')
    print(f'Early scaled x2_extended: {x2_scaled}\n')
    print(f'Scaled s_scaled table: {s_scaled}\n')


def plot_early_scaled():                         # Generacja wykresów po wykonaniu wczesnego skalowania
    fig, axs = plt.subplots(2)
    fig.suptitle('Plot of early scaled signals x1 (red) and x2 (blue)')
    fig.supxlabel('time (modulation cycles number)')
    fig.supylabel('Amplitude')
    axs[0].plot(X_axis, x1_scaled, label="Signal x1 (user U1)", color='r')
    axs[0].grid(axis="x", linestyle=":", lw=1, color="black")
    axs[0].legend(loc='best')
    axs[1].plot(X_axis, x2_scaled, label="Signal x2 (user U2)", color='b')
    axs[1].grid()
    axs[1].legend(loc='best')
    plt.show()


def plot_scaled_both_signals():                 # Generacja wykresu wspólnego sygnałów przeskalowanych
    plt.plot(X_axis, x1_scaled, label="Signal x1 (user U1)", color='r')
    plt.plot(X_axis, x2_scaled, label="Signal x2 (user U2)", color='b')
    plt.xlim(0, N)
    plt.ylim(-1, 1)
    plt.axhline(0, color='black')
    plt.title('Both scaled signals compared with each other')
    plt.xlabel('time (modulation cycles number)')
    plt.ylabel('Amplitude')
    plt.legend(loc='best')
    plt.grid(axis="x", linestyle=":", lw=1, color="black")
    plt.show()


def plot_scaled():                               # Generacja wykresu sygnału zmodulowanego metodą superpozycji
    plt.figure(1)
    plt.title('Scaled signal')
    plt.xlabel('time (modulation cycles number)')
    plt.ylabel('Amplitude')
    plt.plot(X_axis, s_scaled, label="Signal in canal", color='r')
    plt.grid(axis="x", linestyle=":", lw=1, color="black")
    plt.xlim(0, N)
    plt.legend(loc='best')
    plt.axhline(0, color='black')
    plt.show()


# ========================== DECODING ==========================
def binary_first_decoding():
    for i in range(2*N):
        if (s_scaled[i] > 0):
            s1_decoded.append(1)
        if (s_scaled[i] <= 0):
            s1_decoded.append(0)
    print(f'Binary early decoded most powerful signal table is: {s1_decoded}\n')


def plot_first_signal_decoded():                 # Generacja wykresu najsilniejszego sygnału zdemodulowanego
    plt.figure(1)
    plt.title('Strongest demodulated signal')
    plt.xlabel('time (modulation cycles number)')
    plt.ylabel('Amplitude')
    plt.plot(X_axis, s1_decoded, 'r')
    plt.grid(axis="x", linestyle=":", lw=1, color="black")
    plt.xlim(0, N)
    plt.ylim(-0.25, 1.25)
    plt.show()


def binary_decoding_2nd_signal(function_1, function_2):
    holder = 0
    signal = 0
    if (a1 > a2):
        holder = 'a2'
        signal = 's2'
        for i in range(2 * N):
            s2_decoded.append(s_scaled[i] - (math.sqrt(a1) * function_1[i]))
    if (a2 > a1):
        holder = 'a1'
        signal = 's1'
        for i in range(2 * N):
            s2_decoded.append(s_scaled[i] - (math.sqrt(a2) * function_2[i]))
    print(f'2nd signal {signal} is weaker and his table of early decoded values is: {s2_decoded}\n')


def plot_2nd_signal_decoding():                 # Generowanie wykresu sygnału słabszego
    plt.figure(1)
    plt.title('Residual signal')
    plt.xlabel('time (modulation cycles number)')
    plt.ylabel('Amplitude')
    plt.plot(X_axis, s2_decoded, 'r')
    plt.axhline(0, color='black')
    plt.ylim(-1.5, 1.5)
    plt.xlim(0, N)
    plt.grid(axis="x", linestyle=":", lw=1, color="black")
    plt.show()


def final_decoding():
    for i in range(2*N):
        if (s2_decoded[i] > 0):
            s2_decoded[i] = 1
        if (s2_decoded[i] <= 0):
            s2_decoded[i] = 0
    print(f'Binary decoded 2nd signal table is: {s2_decoded}\n')


def plot_final():                               # Generowanie ostatecznej postaci słabszego sygnału zdemodulowanego
    plt.figure(1)
    plt.title('Binary decoded residual signal')
    plt.xlabel('time (modulation cycles number)')
    plt.ylabel('Amplitude')
    plt.plot(X_axis, s2_decoded, 'r')
    plt.ylim(-1.5, 1.5)
    plt.ylim(-0.25, 1.25)
    plt.xlim(0, N)
    plt.grid(axis="x", linestyle=":", lw=1, color="black")
    plt.show()


# -------------------------------- Main Body --------------------------------
print(f'\nTitle of the exercise: NOMA - non orthogonal multiple access\n')
print(f'Basic table for user U1: {x1}')
print(f'Basic table for user U2: {x2}\n')
bpsk_modulation()

arrays_extenction()
# plot()                                       # Etap 1 - generacja wykresów po modulacji BPSK

signal_scaling()
# plot_early_scaled()
# plot_scaled_both_signals()
# plot_scaled()                                # Etap 2 - Sygnał wprowadzany do kanału (zakodowany metodą superpozycji)

binary_first_decoding()
# plot_first_signal_decoded()

binary_decoding_2nd_signal(x1_extended, x2_extended)
# plot_2nd_signal_decoding()
final_decoding()
# plot_final()                                 # Etap 3 - Binarne dekodowanie BPSK
