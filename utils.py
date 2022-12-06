import re
import pandas as pd
def open_file(file):
    with open(file) as f:
        program = [line[: -1] for line in f]
    return program


def add_hex(num1, num2):
    return hex(int(num1, 16) + int(num2, 16))[2: ].upper()

def get_prog_dimension(head_record):
    start = head_record[9: 13]
    length = head_record[15: ]
    return start, add_hex(start, length)

def get_memory_dimension(start, length):
    memory_start = start[: 3] + str(0)
    memory_end = length[: 2] + hex(int(length[3], 16) + 1)[2: ].upper() + str(0)
    return memory_start, memory_end

def get_memory_addresses(memory_start, memory_end):
    memory_addresses = []
    while(int(memory_start, 16) <= int(memory_end, 16)):
        memory_addresses.append(memory_start)
        memory_start = add_hex(memory_start, '10')
    return memory_addresses

def get_text_records(program):
    text_records = []
    for line in program:
        if line[0] == 'T':
            text_records.append(text_record(line))
    return text_records

def text_record(text_record):
    start = text_record[3: 7]
    values = re.findall('..?', text_record[9: ])
    return {
        'Start': start,
        'Values': values
    }
def empty_memory_graph():
    return pd.DataFrame(columns = ['Memory_Address', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'])

def memory_allocation(text_records, memory_graph, starting_address):
    for record in text_records:
        record['Start'] = add_hex(record['Start'], starting_address)
        
        start = record['Start'][:-1] + '0'
        column = record['Start'][-1]
        values = record['Values']
        index = memory_graph[memory_graph.Memory_Address == start].index

        for value in values:
            memory_graph.loc[index, column] = value
            column = add_hex(column, '1')

            if column == '10':
                index += 1
                column = '0'
    return memory_graph