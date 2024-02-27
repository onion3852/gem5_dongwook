#
# Trace generation
#
# 1. select trace type
#   - Sequential
#   - Sequential & Loop
# 2. set the number of traces
# 3. set the write ratio (%)


TICK = 1
START_ADDRESS = 2147483648  # 0x80000000
ADDRESS_GAP = 1024  # 0x400


def generate_address(sel, n, loop, write_tick_gap):
    with open("my_trace.txt", "w") as file:
        if sel == 1:
            # Sequential trace
            write_tick = write_tick_gap
            for i in range(n):
                address = hex(START_ADDRESS + ADDRESS_GAP * i)
                if i == write_tick:
                    trace = "w," + address + ",64," + str(TICK * i)
                    write_tick += write_tick_gap
                    file.write(trace + "\n")
                    continue
                trace = "r," + address + ",64," + str(TICK * i)
                file.write(trace + "\n")

        elif sel == 2:
            # Sequential & Loop trace
            write_tick = write_tick_gap
            for i in range(loop):
                for j in range(n):
                    address = hex(START_ADDRESS + ADDRESS_GAP * j)
                    if j + n * i == write_tick:
                        trace = "w," + address + ",64," + str(j + n * i)
                        write_tick += write_tick_gap
                        file.write(trace + "\n")
                        continue
                    trace = "r," + address + ",64," + str(j + n * i)
                    file.write(trace + "\n")


####################################################################
print("Select the trace type.")
print("1. Sequential")
print("2. Sequential & Loop")

sel = int(input("trace type: "))
if sel == 1:
    n = int(input("\nEnter the number of traces to generate: "))
    loop = 0
elif sel == 2:
    n = int(input("\nEnter the number of traces in each loop: "))
    loop = int(input("\nEnter the number of loop: "))

ratio = float(input("\nEnter the ratio of 'write' command(%): "))
write_tick_gap = int(n / (n * (ratio / 100)))

generate_address(sel, n, loop, write_tick_gap)
