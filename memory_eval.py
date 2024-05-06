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
    emergency_cut_size = 2 * 60 * fps * frame_size / 1024  # in GB

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



if __name__ == "__main__":
    non_video_info = calc_non_video_memory()
    single_video_info, total_video_info, time_info = calc_video_info()
    print(non_video_info)
    print(single_video_info)
    print(total_video_info)
    print(time_info)