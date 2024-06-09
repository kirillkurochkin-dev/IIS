import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
import tkinter as tk
from tkinter import filedialog
from datetime import timedelta
import os

# Function to read data from a file
def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = np.array([list(map(lambda x: float(x.replace(',', '.')), line.split())) for line in lines])
    return data

# Functi    on to choose a file
def choose_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    return file_path

# Choose files
print("Choose file ib.txt")
ib_file_path = choose_file()
print("Choose file ub.txt")
ub_file_path = choose_file()

# Read data
ib = read_data(ib_file_path)
ub = read_data(ub_file_path)

# Ensure the arrays have the same size
assert ib.shape == ub.shape, "Data from ib.txt and ub.txt must be the same size"

# Assume a sampling frequency of 1000 Hz
fs = 1000
num_samples = ib.shape[1]

# Calculate the duration of the experiment
duration_seconds = num_samples / fs
duration = timedelta(seconds=duration_seconds)

# Print the duration of the experiment in HH:MM:SS format
print(f"Experiment duration: {str(duration)}")

# Instantaneous power
p = ub * ib

# RMS voltage and current
U_rms = np.sqrt(np.mean(ub**2, axis=1))
I_rms = np.sqrt(np.mean(ib**2, axis=1))

# Active power
P = np.mean(p, axis=1)

# Apparent power
S = U_rms * I_rms

# Reactive power
Q = np.sqrt(S**2 - P**2)

# Print results
print(f"RMS voltage (U_rms): {U_rms}")
print(f"RMS current (I_rms): {I_rms}")
print(f"Active power (P): {P}")
print(f"Apparent power (S): {S}")
print(f"Reactive power (Q): {Q}")

# Time in seconds
t = np.arange(ib.shape[1]) / fs

# Function to plot signals u(t) and i(t)
def plot_signals():
    plt.figure(figsize=(10, 6))
    plt.plot(t, ub[0], label='u(t)')
    plt.plot(t, ib[0], label='i(t)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.title('Signals u(t) and i(t)')
    plt.grid(True)
    plt.show()

# Function to plot frequency spectrum and save to file
def plot_spectrum_and_save():
    # Calculate FFT for the first cycle (assuming 50 Hz main harmonic, 20 ms period)
    cycle_length = int(fs / 50)
    u_cycle = ub[0, :cycle_length]
    i_cycle = ib[0, :cycle_length]
    
    u_fft = fft(u_cycle)
    i_fft = fft(i_cycle)
    
    frequencies = np.fft.fftfreq(len(u_fft), 1/fs)
    
    # Create spectrum file path
    spectrum_file_path = os.path.join(os.path.dirname(ib_file_path), 'spectrum.txt')
    
    # Check if the spectrum file already exists
    if not os.path.isfile(spectrum_file_path):
        # Save spectrum to file
        with open(spectrum_file_path, 'w') as f:
            f.write('Frequency(Hz)\tU(f)\tI(f)\n')
            for freq, u_val, i_val in zip(frequencies[:len(frequencies)//2], np.abs(u_fft)[:len(u_fft)//2], np.abs(i_fft)[:len(i_fft)//2]):
                f.write(f"{freq}\t{u_val}\t{i_val}\n")
        print(f"Spectrum saved to {spectrum_file_path}")
    else:
        print(f"Spectrum file already exists: {spectrum_file_path}")
    
    # Plot the spectrum
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies[:len(frequencies)//2], np.abs(u_fft)[:len(u_fft)//2], label='U(f)')
    plt.plot(frequencies[:len(frequencies)//2], np.abs(i_fft)[:len(i_fft)//2], label='I(f)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.title('Frequency Spectrum')
    plt.grid(True)
    plt.show()

# Function to plot instantaneous power p(t)
def plot_instantaneous_power():
    plt.figure(figsize=(10, 6))
    plt.plot(t, p[0], label='p(t)')
    plt.xlabel('Time (s)')
    plt.ylabel('Power')
    plt.legend()
    plt.title('Instantaneous Power p(t)')
    plt.grid(True)
    plt.show()

# Function to plot active, reactive, and apparent power over time
def plot_power_over_time():
    plt.figure(figsize=(10, 6))
    plt.plot(P, label='Active Power P(t)')
    plt.plot(Q, label='Reactive Power Q(t)')
    plt.plot(S, label='Apparent Power S(t)')
    plt.xlabel('Sample Index')
    plt.ylabel('Power')
    plt.legend()
    plt.title('Power over time')
    plt.grid(True)
    plt.show()

# Command-line interface for choosing which plots to display
def main():
    while True:
        print("\nChoose the plot to display:")
        print("1. Signals u(t) and i(t)")
        print("2. Frequency Spectrum (and save to file)")
        print("3. Instantaneous Power p(t)")
        print("4. Active, Reactive, and Apparent Power over time")
        print("5. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == '1':
            plot_signals()
        elif choice == '2':
            plot_spectrum_and_save()
        elif choice == '3':
            plot_instantaneous_power()
        elif choice == '4':
            plot_power_over_time()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()