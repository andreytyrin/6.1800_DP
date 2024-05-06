import numpy as np
import math
from scipy.stats import norm
import matplotlib.pyplot as plt

avg_num_trips = 10_000  # average number of trips per day
C = 5000  # number of bikes
num_active_hours = 4  # number of active hours per day
avg_trip_time = 30  # average trip time in minutes


def compute_rates(num_active_hours=8, num_trips=10000, avg_trip_time=30, C=5000):
    interarrival_time = 60 * num_active_hours / num_trips

    lambda_rate = 1 / interarrival_time  # number of users looking for a bike per minute
    mu_rate = 1 / avg_trip_time  # bikes availability per minute
    return lambda_rate, mu_rate, lambda_rate / (mu_rate * C)


def prob_more_than_t(t, rho):
    return np.exp(-1 / rho * (t + 0.01))


def plot_prob_vs_num_trips():
    plt.rcParams["axes.labelsize"] = 18
    plt.rcParams["axes.titlesize"] = 18
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16

    num_trips = np.arange(1, 1_000_000, 100)
    wait_times = np.arange(1, 10.5, 0.1)
    probs = np.zeros((len(wait_times), len(num_trips)))

    for i, wait_time in enumerate(wait_times):
        for j, n in enumerate(num_trips):
            probs[i, j] = prob_more_than_t(wait_time, compute_rates(num_trips=n)[2])

    fig, ax = plt.subplots(figsize=(10, 8))
    c = ax.imshow(
        probs,
        aspect="auto",
        interpolation="nearest",
        cmap="Greens",
        origin="lower",
        extent=[num_trips[0], num_trips[-1], wait_times[0], wait_times[-1]],
    )

    ax.set_xlabel("Number of trips per day")
    ax.set_ylabel("Wait Time Threshold (min)")
    # ax.set_title("Probability Heatmap of Waiting More Than Threshold Time")
    cbar = fig.colorbar(c, ax=ax, label="Probability")
    ax.grid(False)
    fig.tight_layout()
    fig.savefig("prob_heatmap.png", dpi=300)


def hist_rho_factor_vs_num_trips():
    plt.rcParams["axes.labelsize"] = 18
    plt.rcParams["axes.titlesize"] = 18
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16
    plt.rcParams["legend.fontsize"] = 16

    num_trips = np.arange(100, 100_000, 5000)
    rho_factors = [compute_rates(num_trips=n)[2] for n in num_trips]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axhline(y=1, color="red", linestyle="--", linewidth=2, label="$\\rho$ = 1")

    ax.bar(num_trips, rho_factors, color="gray", width=3000)
    ax.set_xlabel("Daily number of trips")
    # ax.set_ylabel("Rho factor")
    ax.set_ylabel("$\\rho$")
    fig.tight_layout()
    ax.legend()

    fig.savefig("rho_hist.png", dpi=300)
    
def plot_combined():
    # Set common configurations
    plt.rcParams["axes.labelsize"] = 18
    plt.rcParams["axes.titlesize"] = 18
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16
    plt.rcParams["legend.fontsize"] = 16

    # Data for heatmap
    num_trips_heatmap = np.arange(1, 1_000_000, 100)
    wait_times = np.arange(1, 10.5, 0.1)
    probs = np.zeros((len(wait_times), len(num_trips_heatmap)))
    for i, wait_time in enumerate(wait_times):
        for j, n in enumerate(num_trips_heatmap):
            probs[i, j] = prob_more_than_t(wait_time, compute_rates(num_trips=n)[2])

    # Data for bar plot
    num_trips_bar = np.arange(100, 100_000, 5000)
    rho_factors = [compute_rates(num_trips=n)[2] for n in num_trips_bar]

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Plot heatmap
    c = ax1.imshow(
        probs,
        aspect="auto",
        interpolation="nearest",
        cmap="Greens",
        origin="lower",
        extent=[num_trips_heatmap[0], num_trips_heatmap[-1], wait_times[0], wait_times[-1]],
    )
    ax1.set_xlabel("Number of trips per day")
    ax1.set_ylabel("$t$, Wait Time Threshold (min)")
    # ax1.set_title("Probability Heatmap of Waiting More Than Threshold Time")
    cbar = fig.colorbar(c, ax=ax1, label="$P$(waiting > $t$ min)")
    ax1.grid(False)

    # Plot bar plot
    ax2.axhline(y=1, color="red", linestyle="--", linewidth=2, label="$\\rho$ = 1")
    ax2.bar(num_trips_bar, rho_factors, color="gray", width=3000)
    ax2.set_xlabel("Daily number of trips")
    ax2.set_ylabel("$\\rho$")
    ax2.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7)
    ax2.legend()

    # Layout adjustments and save
    fig.tight_layout()
    fig.savefig("combined_plot.png", dpi=300)



if __name__ == "__main__":
    lambda_rate, mu_rate, rho = compute_rates(
        num_active_hours, avg_num_trips, avg_trip_time, C
    )
    print(f"lambda = {lambda_rate}, mu = {mu_rate}, rho = {rho}")
    print(f"Probability of waiting more than 1 minute: {prob_more_than_t(1, rho)}")
    # plot_prob_vs_num_trips()
    # hist_rho_factor_vs_num_trips()
    plot_combined()
