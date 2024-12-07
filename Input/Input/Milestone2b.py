import json

def read_file(file_path):
    with open(file_path,'r') as file:
        data = json.load(file)
    return data

def steps_parser(json_data):
    steps_dict = json_data['steps']
    rangemin = []
    rangemax = []
    dependency = []
    for i in range(len(steps_dict[0]['parameters']['P1'])):
        min = steps_dict[i]['parameters']['P1'][0]
        max = steps_dict[i]['parameters']['P1'][1]
        rangemin.append(min)
        rangemax.append(max)
        depend = steps_dict[i]['dependency']
        if(depend == None): depend = 0
        dependency.append(depend)
    return rangemin,rangemax,dependency

def machines_parser(json_data):
    machines_dict = json_data['machines']
    machines_id = []
    steps_id = []
    cooldown_time = []
    init_param = []
    fluctuation = []
    number_of_wafer = []
    machines = []
    for i in range(len(machines_dict)):
        machines_id.append(machines_dict[i]['machine_id'])
        steps_id.append(machines_dict[i]['step_id'])
        cooldown_time.append(machines_dict[i]['cooldown_time'])
        init_param.append(machines_dict[i]['initial_parameters'])
        fluctuation.append(machines_dict[i]['fluctuation'])
        number_of_wafer.append(machines_dict[i]['n'])
    return machines_id,steps_id,cooldown_time,init_param,fluctuation,number_of_wafer

def wafer_parser(json_data):
    wafers_dict = json_data['wafers']
    wafer_type = []
    time = []
    processing_time = []
    quantity = []
    for i in range(len(wafers_dict)):
        wafer_type.append(wafers_dict[i]['type'])
        for j in range(len(wafers_dict[i]['processing_times'])):
            time.append(wafers_dict[i]['processing_times'][f'S{j+1}'])    
        processing_time.append(time)
        time = []
        # processing_time.append([wafers_dict[i]['processing_times']])
        quantity.append(wafers_dict[i]['quantity'])
    return wafer_type,processing_time,quantity

def process_schedules(processing_time,quantity):
    start_time_m1 = 0
    start_time_m2 = 0
    start_time_m3 = 0
    start_time_m4 = 0
    w1_s1_time = processing_time[0][0]
    w1_s2_time = processing_time[0][1]
    w2_s1_time = processing_time[1][0]
    w2_s2_time = processing_time[1][1]
    P1 = []
    P2 = []
    P3 = []
    P4 = []
    sch = []
    schedules = {}
    w1_quan = int(quantity[0])
    w2_quan = int(quantity[1])
    max_len = max(w1_quan,w2_quan)
    for i in range(1,max_len+1):
        if(i%2 != 0):
            if(i<=w1_quan):
                end_time_m1 = start_time_m1 + w1_s1_time
                P1.append({"wafer_id":f"W1-{i}","step":"S1","machine":"M1","start_time":start_time_m1,"end_time":end_time_m1})
            end_time_m2 = start_time_m2 + w2_s1_time
            P2.append({"wafer_id":f"W2-{i}","step":"S1","machine":"M2","start_time":start_time_m2,"end_time":end_time_m2})
            end_time_m3 = start_time_m3 + w2_s2_time
            P3.append({"wafer_id":f"W2-{i+1}","step":"S2","machine":"M3","start_time":start_time_m3,"end_time":end_time_m3})
            if(i <= w1_quan):
                end_time_m4 = start_time_m4 + w1_s2_time
                P4.append({"wafer_id":f"W1-{i+1}","step":"S2","machine":"M4","start_time":start_time_m4,"end_time":end_time_m4})
        if(i%2 == 0):
            if(i<=w1_quan):
                end_time_m1 = start_time_m1 + w1_s1_time
                P1.append({"wafer_id":f"W1-{i}","step":"S1","machine":"M1","start_time":start_time_m1,"end_time":end_time_m1})
            end_time_m2 = start_time_m2 + w2_s1_time
            P2.append({"wafer_id":f"W2-{i}","step":"S1","machine":"M2","start_time":start_time_m2,"end_time":end_time_m2})
            end_time_m3 = start_time_m3 + w2_s2_time
            P3.append({"wafer_id":f"W2-{i-1}","step":"S2","machine":"M3","start_time":start_time_m3,"end_time":end_time_m3})
            if(i<=w1_quan):
                end_time_m4 = start_time_m4 + w1_s2_time
                P4.append({"wafer_id":f"W1-{i-1}","step":"S2","machine":"M4","start_time":start_time_m4,"end_time":end_time_m4})
        start_time_m4 = start_time_m3 = start_time_m2 = start_time_m1 = max(end_time_m4,end_time_m3,end_time_m1,end_time_m2)
    for i in range(max_len):
        if(i<=w1_quan-1):
            sch.append(P1[i])
        sch.append(P2[i])
        sch.append(P3[i])
        if(i<=w1_quan-1):
            sch.append(P4[i])
    print(sch)
    schedules = {"schedule" : sch}
    return schedules

def main():
    file_path = "C:/Users/csuser/Desktop/Milestones/Input/Input/Milestone2b.json"
    json_data = read_file(file_path)
    rangemin,rangemax,dependency = steps_parser(json_data)
    machines_id,steps_id,cooldown_time,init_param,fluctuation,number_of_wafer = machines_parser(json_data)
    wafer_type,processing_time,quantity = wafer_parser(json_data)
    schedules = process_schedules(processing_time,quantity)

    with open('output2b.json','w') as file:
        json.dump(schedules,file)

main()