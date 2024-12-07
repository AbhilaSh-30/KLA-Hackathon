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
    for i in range(len(machines_dict)):
        machines_id.append(machines_dict[i]['machine_id'])
        steps_id.append(machines_dict[i]['step_id'])
        cooldown_time.append(machines_dict[i]['cooldown_time'])
        for j in range(len(machines_dict[i]['initial_parameters'])):
            init_param.append(machines_dict[i]['initial_parameters'][f'P{j+1}'])
        for k in range(len(machines_dict[i]['fluctuation'])):
            fluctuation.append(machines_dict[i]['fluctuation'][f'P{j+1}'])
        number_of_wafer.append(machines_dict[i]['n'])
    return machines_id,steps_id,cooldown_time,init_param,fluctuation,number_of_wafer

def wafer_parser(json_data):
    wafers_dict = json_data['wafers']
    wafer_type = []
    processing_time = []
    quantity = []
    for i in range(len(wafers_dict)):
        wafer_type.append(wafers_dict[i]['type'])
        # for j in range(len(wafers_dict[i]['processing_times'])):
        #     processing_time.append(wafers_dict[i]['processing_times'][f'S{j+1}'])
        processing_time.append(wafers_dict[i]['processing_times'])
        quantity.append(wafers_dict[i]['quantity'])
    return wafer_type,processing_time,quantity

def process_schedules(processing_time,quantity,init_param,fluctuation,rangemax,number_of_wafer,cooldown_time):
    start_time_m1 = 0
    start_time_m2 = 0
    s1_time = processing_time[0]['S1']
    s2_time = processing_time[1]['S2']
    m1_init = init_param[0]
    m2_init = init_param[1]
    m1_fluc = fluctuation[0]
    m2_fluc = fluctuation[1]
    m1_n = number_of_wafer[0]
    m2_n = number_of_wafer[1]
    m1_cool = cooldown_time[0]
    m2_cool = cooldown_time[1]
    P1 = []
    P2 = []
    sch = []
    schedules = {}
    length = int(quantity[0])
    for i in range(1,int(quantity[0])+1):
        if(m1_init<=rangemax[0] or m2_init<=rangemax[1]):
            if(m1_init<=rangemax[0]):
                end_time_m1 = start_time_m1 + s1_time
                P1.append({"wafer_id":f"W1-{i}","step":"S1","machine":"M1","start_time":start_time_m1,"end_time":end_time_m1})
                if(i%2 == 0):
                    m1_init += m1_fluc
                
            if(m2_init<=rangemax[1]):
                end_time_m2 = start_time_m2 + s2_time
                P2.append({"wafer_id":f"W2-{i}","step":"S2","machine":"M2","start_time":start_time_m2,"end_time":end_time_m2})
                m2_init += m2_fluc
            start_time_m2 = start_time_m1 = max(end_time_m2,end_time_m1)
            
            if(m1_init>=rangemax[0]):
                start_time_m1 += m1_cool
                m1_init = init_param[0]

            if(m2_init>=rangemax[1]):
                start_time_m2 += m2_cool
                m2_init = init_param[1]  

    for i in range(len(P1)):
        sch.append(P1[i])
        sch.append(P2[i])
    schedules = {"schedule" : sch}
    return schedules

def main():
    file_path = "C:/Users/csuser/Desktop/Milestones/Input/Input/Milestone3a.json"
    json_data = read_file(file_path)
    rangemin,rangemax,dependency = steps_parser(json_data)
    machines_id,steps_id,cooldown_time,init_param,fluctuation,number_of_wafer = machines_parser(json_data)
    wafer_type,processing_time,quantity = wafer_parser(json_data)
    schedules = process_schedules(processing_time,quantity,init_param,fluctuation,rangemax,number_of_wafer,cooldown_time)
    with open('output3a.json','w') as file:
        json.dump(schedules,file)

main()