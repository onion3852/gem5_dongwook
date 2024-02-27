# Trace generation
#
# 1. set the number of traces
# 2. set the write ratio (%)

# Tick gap between each trace will be
# given as a random value from 30 to 39
TICK_GAP_BASE = 30

START_ADDRESS = 2147483648  # 0x80000000
ADDRESS_GAP = 64  # 0x40

import random


def generate_trace():
    print("\n### Sequential Trace Generator ###")
    print("Enter the number of traces to generate.")
    print("(each trace is devided into 16 sub-traces)")
    n = int(input(": "))

    # 'write' command is put uniformly.
    # ex) if number of trace is 100 and write ratio is 5%,
    #     20th, 40th, 60th, 80th, and 100th traces are write command
    write_ratio = float(input("\nEnter the ratio of 'write' command(%): "))

    # gap between write command (order)
    if write_ratio == 0:
        write_command = -1
    else:
        write_command_gap = int(n / (n * (write_ratio / 100)))
        # first write command order
        write_command = write_command_gap - 1

    # command's Tick
    tick = 0

    # trace will be generated in 'my_trace.txt'
    with open("my_trace.txt", "w") as file:
        # total number of trace is n
        for i in range(n):
            address = hex(START_ADDRESS + (ADDRESS_GAP * i))

            # if it's write command
            if i == write_command:
                trace = "w," + address[2:] + ",64," + str(tick)
                file.write(trace + "\n")

                # set the index of next write command
                write_command += write_command_gap
                # set the next command's Tick
                tick = tick + (TICK_GAP_BASE + random.randint(0, 9))
                continue

            # if it's read command
            trace = "r," + address[2:] + ",64," + str(tick)
            file.write(trace + "\n")
            # set the next command's Tick
            tick = tick + (TICK_GAP_BASE + random.randint(0, 9))


########################################################################################
generate_trace()
