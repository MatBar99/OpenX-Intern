import argparse
from datetime import datetime
from datetime import timedelta
import re 
import numpy as np
import collections
import os
import warnings 


'''
This program capture all dates stored in one file by using regex.
Next, it finds time slot based on three ideas explained in comments.
The last step is about finding common time slot. It can be done by
finding reapated starting points and by finding which person finish its
break at the latest.

'''


def convert_all_day(date):
    date_end = date + timedelta(hours=23,minutes=59,seconds=59)

    return [date, date_end]

def obtain_date_from_file(path):
    with open(path, 'r') as file:
        dates = []
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            matches = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)

            for match in matches:
                date = datetime.strptime(match,"%Y-%m-%d %H:%M:%S")
                dates.append(date)

            matches = re.findall(r'\d{4}-\d{2}-\d{2}$', line)

            for match in matches:
                date = datetime.strptime(match,"%Y-%m-%d")
                dates.extend(convert_all_day(date))
    dates.sort()
    return dates

def find_slots_one_person(reference_date, time_in_minutes, calendar_dates):
    all_slots = []
    #checking if there is a time slot before first break
    diff_start = np.timedelta64(calendar_dates[0] - reference_date,'m')
    diff_start_minutes = diff_start.astype(int)
    if diff_start_minutes > time_in_minutes:
        slot_start = reference_date + timedelta(seconds=1)
        all_slots.append(slot_start)
        
    #if there are more breaks, there is possibility to find a time slot between them
    if len(calendar_dates) > 2 and len(calendar_dates) % 2 == 0:
        starting_points = calendar_dates[1::2]
        ending_points = calendar_dates[2::2]
        for s_point,e_point in zip(starting_points, ending_points):
            diff = np.timedelta64(e_point-s_point,'m')
            diff_minutes = diff.astype(int)
            if(diff_minutes) > 30:
                slot_start = s_point + timedelta(seconds=1)
                all_slots.append(slot_start)

    #there is always time slot after the last break
    slot_start = calendar_dates[-1] + timedelta(seconds=1)

    all_slots.append(slot_start)
    return all_slots

def find_files(path):
    filepaths = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            filepaths.append(os.path.join(path, file))
    return filepaths
     
def find_final_slots(path, time_in_minutes, min_people, reference_date):
    slots = []
    last_break_slots = []

    filepaths = find_files(path)

    if len(filepaths) < min_people:
        warnings.warn("There are not that many calendars!")
        warnings.warn("The slots will be found for all people.")
        min_people = len(filepaths)

    for i in range(min_people):
        date = obtain_date_from_file(filepaths[i])
        one_slot = find_slots_one_person(reference_date, time_in_minutes, date)
        slots.extend(one_slot)
        last_break_slots.append(one_slot[-1])
    
    repeated_slots = [item for item, count in collections.Counter(slots).items() if count > 1]
    common_last_slot = [max(last_break_slots)]
    

    return repeated_slots + common_last_slot

def show_dates(slots):
    for slot in slots:
        print(slot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--calendars',
                        default='in', type=str)
    parser.add_argument('-d', '--duration-in-minutes',
                        default=30, type=int)
    parser.add_argument('-m', '--minimum-people',
                        default=2, type=int)
    parser.add_argument('-t', '--reference-date',
                        default=datetime(year=2022,month=7,day=1,hour=9))

    args = parser.parse_args()
    slots = find_final_slots(args.calendars, args.duration_in_minutes,
                             args.minimum_people, args.reference_date)
    show_dates(slots)
