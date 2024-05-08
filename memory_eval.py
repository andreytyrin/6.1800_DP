import numpy as np
import matplotlib.pyplot as plt

avg_num_trips = 10_000  # average number of trips per day
C = 5000  # number of bikes
num_active_hours = 4  # number of active hours per day
avg_trip_time = 30  # average trip time in minutes
num_users = 50_000

fraction_w_cameras = 0.1
fps = 30
emergency_recording_time = 15  # in minutes
frame_size = 1.5  # in MB
acc_rate = 45  # in MB/s
cellular_rate = 25  # in MB/s
station2ccf_rate = 1024  # in MB/s

def calc_non_video_memory():
    users_db_entry_size = 320 / 8  # in bytes
    bikes_db_entry_size = 640 / 8  # in bytes

    routes_db_amt_per_day = (
        60 * avg_trip_time /10 * 2 * 32 / 8 * avg_num_trips / 1024 ** 2
    )  # in MB

    transactions_db_amt_per_day = 32 * 10 / 8 * avg_num_trips / 1024 ** 2  # in MB
    return {
        "users_db_entry_size": users_db_entry_size,
        "bikes_db_entry_size": bikes_db_entry_size,
        "routes_db_amt_per_day": routes_db_amt_per_day,
        "transactions_db_amt_per_day": transactions_db_amt_per_day,
    }


def calc_video_info():
    num_videos_recorded = avg_num_trips * fraction_w_cameras
    avg_video_size = avg_trip_time * 60 * fps * frame_size / 1024  # in MB
    emergency_video_size = emergency_recording_time * 60 * fps * frame_size / 1024 # in GB
    worst_case_video_size = avg_video_size + emergency_video_size
    emergency_cut_size = 3 * 60 * fps / 3 * frame_size / 1024  # in GB

    single_video_info = {
        "avg_video_size": avg_video_size,
        "emergency_video_size": emergency_video_size,
        "worst_case_video_size": worst_case_video_size,
        "emergency_cut_size": emergency_cut_size,
    }

    # wc stands for worst case
    absolutely_wc_size = worst_case_video_size * avg_num_trips / 1024  # in GB
    wc_size = worst_case_video_size * num_videos_recorded / 1024  # in GB
    avg_size = avg_video_size * num_videos_recorded / 1024  # in GB

    total_size_info = {
        "absolutely_wc_size": absolutely_wc_size,
        "wc_size": wc_size,
        "avg_size": avg_size,
    }
    
    ### time analysis ###
    wc_cellular_full = emergency_video_size / (cellular_rate / 1024)  # in seconds
    cellular_cut = emergency_cut_size / (cellular_rate / 1024)  # in seconds
    station2ccf_wc = wc_size / (station2ccf_rate / 1024)  # in seconds
    station2ccf_avg = avg_size / (station2ccf_rate / 1024)  # in seconds
    time_info = {
        "wc_cellular_full": wc_cellular_full,
        "cellular_cut": cellular_cut,
        "station2ccf_wc": station2ccf_wc,
        "station2ccf_avg": station2ccf_avg,
    }
    
    return single_video_info, total_size_info, time_info

def plot_non_video_memory(non_video_info):
    # Single video labels and sizes
    plt.rcParams["axes.labelsize"] = 18
    plt.rcParams["axes.titlesize"] = 18
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16
    plt.rcParams["legend.fontsize"] = 16 
    
    labels = ["Users", "Bikes",
              "Routes",
              "Transactions"]
    sizes = [non_video_info["users_db_entry_size"] * num_users / 1024 ** 2,
             non_video_info["bikes_db_entry_size"] * C / 1024 ** 2,
             non_video_info["routes_db_amt_per_day"],
             non_video_info["transactions_db_amt_per_day"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 10))
    # STATIC DB
    ax1.bar(labels[:2], sizes[:2], color='darkgreen', alpha=0.7)
    ax1.set_ylabel("Memory (MB)")
    ax1.set_title("Table Sizes")
    ax1.tick_params(axis='x', labelsize=16)
    ax1.tick_params(axis='y', labelsize=16)
    
    # DYNAMIC DB
    ax2.bar(labels[2:], sizes[2:], color='darkgreen', alpha=0.7)
    ax2.set_ylabel("Memory (MB)")
    ax2.set_title("Daily Amounts Written to DB")
    ax2.tick_params(axis='x', labelsize=16)
    ax2.tick_params(axis='y', labelsize=16)
    
    fig.tight_layout()
    plt.savefig("non_video_memory.png", dpi=300)
    


def plot_video_memory(single_video_info, total_size_info, time_info):
    # Single video labels and sizes
    plt.rcParams["axes.labelsize"] = 18
    plt.rcParams["axes.titlesize"] = 18
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16
    plt.rcParams["legend.fontsize"] = 16
    
    
    labels_single = ["Average Case", "Emergency Case",
                     "Worst Case", "Emergency Cut"]
    sizes_single = [single_video_info["avg_video_size"],
                    single_video_info["emergency_video_size"],
                    single_video_info["worst_case_video_size"],
                    single_video_info["emergency_cut_size"]]

    # Total size labels and sizes
    labels_total = ["Worst Case", "Average Case"]
    sizes_total = [total_size_info["absolutely_wc_size"],
                   total_size_info["wc_size"],]
    emergency_cut_size = single_video_info["emergency_cut_size"]
    
    labels_time = ["Emergence Cut$\\to$CCF", "Station$\\to$CCF"]
    sizes_time = [time_info["cellular_cut"], time_info["station2ccf_wc"]]
    

    # Create subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 10))

    # Plot single video sizes
    zipped = zip(labels_single, sizes_single)
    sorted_zipped = sorted(zipped, key=lambda x: x[1], reverse=True)
    labels_single, sizes_single = zip(*sorted_zipped)
    
    ax1.bar(labels_single, sizes_single, color='gray', alpha=0.7)
    ax1.axhline(y=emergency_cut_size, color="red", linestyle="--", linewidth=2, label="Emergency Cut Size")
    
    yticks = ax1.get_yticks()
    if emergency_cut_size not in yticks:
        yticks = np.append(yticks, emergency_cut_size)
        ax1.set_yticks(yticks[1:])

    ax1.set_ylabel("Memory (GB)")
    ax1.set_title("Single Video Memory Sizes")
    # ax1.grid(True)
    ax1.tick_params(axis='x', rotation=30, labelsize=16)
    ax1.tick_params(axis='y', labelsize=16)
    ax1.legend()

    # Plot total sizes
    ax2.bar(labels_total, sizes_total, color='gray', alpha=0.7)
    ax2.set_ylabel("Memory (GB)")
    ax2.set_title("Daily Amount of Video Data")
    # ax2.grid(True)
    ax2.tick_params(axis='x', rotation=30, labelsize=16)
    ax2.tick_params(axis='y', labelsize=16)

    
    ax3.bar(labels_time, sizes_time, color='gray', alpha=0.7)
    ax3.set_ylabel("Time (seconds)")
    ax3.set_title("Video Transfer Times")
    # ax3.grid(True)
    ax3.tick_params(axis='x', rotation=30, labelsize=16)
    ax3.tick_params(axis='y', labelsize=16)
    
    # Adjust layout and save
    fig.tight_layout()

    plt.savefig("video_memory.png", dpi=300)
    
    

if __name__ == "__main__":
    non_video_info = calc_non_video_memory()
    single_video_info, total_video_info, time_info = calc_video_info()

    plot_non_video_memory(non_video_info)
    plot_video_memory(single_video_info, total_video_info, time_info)

    print(non_video_info)
    print(single_video_info)
    print(total_video_info)
    print(time_info)
