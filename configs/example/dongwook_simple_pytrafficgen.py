import m5
from m5.objects import *
from m5.defines import buildEnv
from m5.util import addToPath
import os, argparse, sys

addToPath("../")
addToPath("../..")

from common import Options

# Get paths we might need.  It's expected this file is in m5/configs/example.
config_path = os.path.dirname(os.path.abspath(__file__))
config_root = os.path.dirname(config_path)


parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
Options.addNoISAOptions(parser)

# PyTrafficGen argument
parser.add_argument(
    "--traffic_mode",
    type=str,
    help="pattern of generated addresses, linear or random.",
)
parser.add_argument(
    "--traffic_mode_cpu",
    type=str,
    help="pattern of generated addresses, linear or random or trace.",
)
parser.add_argument(
    "--traffic_mode_dma",
    type=str,
    help="pattern of generated addresses, linear or random or trace.",
)
parser.add_argument(
    "--trace_duration",
    type=int,
    help="duration of this state before transitioning.",
)
parser.add_argument(
    "--rd_prct",
    type=int,
    default=50,
    help="pattern of generated addresses, linear or random.",
)

parser.add_argument(
    "--maxloads", metavar="N", default=0, help="Stop after N loads"
)
parser.add_argument(
    "--progress",
    type=int,
    default=1000,
    metavar="NLOADS",
    help="Progress message interval ",
)
parser.add_argument("--num-dmas", type=int, default=0, help="# of dma testers")
parser.add_argument(
    "--functional",
    type=int,
    default=0,
    help="percentage of accesses that should be functional",
)
parser.add_argument(
    "--suppress-func-errors",
    action="store_true",
    help="suppress panic when functional accesses fail",
)

args = parser.parse_args()

## argument print for debug
print("dongwook debug] args.num_cpus: ", args.num_cpus)
print("dongwook debug] args.num_dmas: ", args.num_dmas)
print("dongwook debug] args.num_dirs: ", args.num_dirs)

#args.l1d_size = "32kB"
#args.l1i_size = "32kB"
args.icache_size = "32kB"
args.dcache_size = "32kB"
#args.l1d_assoc = 4
#args.l1i_assoc = 4
args.icache_assoc = 4
args.dcache_assoc = 4
#args.l2_size = "128kB"
args.l2cache_size = "128kB"
#args.l2_assoc = 4
args.l2cache_assoc = 4
#args.l3_size = "2MB"
args.l3cache_size = '2MB'
#args.l3_assoc = 2
args.l3cache_assoc = 16

block_size = 64

if args.num_cpus > block_size:
    print(
        "Error: Number of testers %d limited to %d because of false sharing"
        % (args.num_cpus, block_size)
    )
    sys.exit(1)

cpus = PyTrafficGen()


system = System(
    cpu=cpus,
    clk_domain=SrcClockDomain(clock=args.sys_clock),
    mem_ranges=[
        AddrRange(start=0x80000000, size="2GB"),
        AddrRange(start=0x880000000, size="30GB"),
        AddrRange(start=0x8800000000, size="480GB"),
    ],
)

print("dongwook debug] len(system.mem_ranges): ", len(system.mem_ranges))

system.mmap_using_noreserve = True


if args.num_dmas > 0:
    dmas = [PyTrafficGen() for i in range(args.num_dmas)]
    system.dma_devices = dmas

    # comm_monitor for dmas
    comm_monitor_dmas = [CommMonitor() for i in range(args.num_dmas)]
    system.comm_monitor_dma_devices = comm_monitor_dmas
else:
    dmas = []
    comm_monitor_dmas = []

dma_ports = []
for (i, dma) in enumerate(dmas):
    # dma_ports.append(dma.test)
    # dma_ports.append(dma.port)
    dma.port = comm_monitor_dmas[i].cpu_side_port
    dma_ports.append(comm_monitor_dmas[i].mem_side_port)

print("dongwook debug] args: ", args)

import math
from common.CacheConfig import *
from common.Caches import *
from common import MemConfig
#from src.mem.DRAMInterface import DRAMInterface

# L1 bus
system.cpu.l1bus = L1XBar()
# L2 bus
system.cpu.l2bus = L2XBar()

# L1 cache
system.cpu.icache = L1_ICache()
system.cpu.dcache = L1_DCache()
system.cpu.port = system.cpu.l1bus.cpu_side_ports
system.cpu.icache.cpu_side = system.cpu.l1bus.mem_side_ports
system.cpu.dcache.cpu_side = system.cpu.l1bus.mem_side_ports
system.cpu.icache.mem_side = system.cpu.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.cpu.l2bus.cpu_side_ports
# L2 cache 
system.cpu.l2cache = L2Cache()
system.cpu.l2cache.cpu_side = system.cpu.l2bus.mem_side_ports

# L3 bus
system.l3bus = L3XBar()
system.cpu.l2cache.mem_side = system.l3bus.cpu_side_ports

# L3 cache
system.l3cache = L3Cache()

# connect L3 cache has L3 bus
system.l3cache.cpu_side = system.l3bus.mem_side_ports

# membus
system.membus = SystemXBar()

# connect L3 cache and membus
system.l3cache.mem_side = system.membus.cpu_side_ports

## L3 cache has two mem_side_ports
# l3cache_mem_side = []
# membus_cpu_side = []
# for i in range(2):
#     l3cache_mem_side.append()
#     membus_cpu_side.append()
# system.cpu.l3cache.mem_side = l3cache_mem_side
# system.membus.cpu_side_ports = membus_cpu_side

# connect comm_monitor_dmas to membus
for i in range(args.num_dmas):
    comm_monitor_dmas[i].mem_side_port = system.membus.cpu_side_ports

## comm_monitor for drams
#if args.num_dirs > 0:
#    comm_monitor_mems = [CommMonitor() for i in range(args.num_dirs)]
#    system.comm_monitor_mem_devices = comm_monitor_mems
#else:
#    comm_monitor_mems = []
#for i in range (args.num_dirs):
#    comm_monitor_mems[i].cpu_side_port = system.membus.mem_side_ports

# dongwook start
##if args.numa_high_bit:
##    dir_bits = int(math.log(args.num_dirs, 2))
##    intlv_size = 2 ** (args.numa_high_bit - dir_bits + 1)
##else:
##    intlv_size = args.cacheline_size

intlv_size = block_size # 64
xor_low_bit = 20 # options from falcon_garnet.ver
crossbars = []
mem_ctrls = []
index = 0
for i in range (args.num_dirs):
        crossbar = None
        if len(system.mem_ranges) > 1:
            crossbar = IOXBar(width=32)  # 32B = 256b
            crossbars.append(crossbar)
            crossbars[i].cpu_side_ports = system.membus.mem_side_ports

        dir_ranges = []
        for r in system.mem_ranges:
            mem_type = ObjectList.mem_list.get(args.mem_type)
            dram_intf = MemConfig.create_mem_intf(  # configs/common/MemConfig.py
                mem_type,
                r,  # 0x8000_0000 ~ 2GB, 0x8_8000_0000 ~ 30GB, 0x88_0000_0000 ~ 480GB
                index,  # 0 ~ (number of dir_cntrl-1)
                int(math.log(args.num_dirs, 2)),
                intlv_size,
                xor_low_bit,
            )
            if issubclass(mem_type, DRAMInterface):
                mem_ctrl = m5.objects.MemCtrl(dram=dram_intf)
            else:
                mem_ctrl = dram_intf

            #if args.access_backing_store:
            #   dram_intf.kvm_map = False

            mem_ctrls.append(mem_ctrl)
            dir_ranges.append(dram_intf.range)

            if crossbar != None:
                mem_ctrl.port = crossbar.mem_side_ports

            # Enable low-power DRAM states if option is set
            if issubclass(mem_type, DRAMInterface):
                mem_ctrl.dram.enable_dram_powerdown = (
                    args.enable_dram_powerdown
                )

        index += 1

system.mem_ctrls = mem_ctrls

if len(crossbars) > 0:
    system.crossbars = crossbars

# dongwook end

#drams = []
#for i in range (args.num_dirs):
#    drams.append(DDR5_4400_4x8())
#
#mem_ctrls = []
#for i in range (args.num_dirs):
#    for j in range(len(system.mem_ranges)):
#        mem_ctrls.append(MemCtrl())
#        mem_ctrls[i*len(system.mem_ranges) + j].dram = DDR5_4400_4x8()
#        print("dongwook debug] mem_ctrls: ", i*len(system.mem_ranges) + j)
#        print("dongwook debug] dram: ", drams[i])
#        mem_ctrls[i*len(system.mem_ranges) + j].dram.range = system.mem_ranges[j]
#        #mem_ctrls[i*3 + j].dram[i].range = system.mem_ranges[j]
#        mem_ctrls[i*len(system.mem_ranges) + j].port = system.membus.mem_side_ports
#        #system.mem_ctrl0 = MemCtrl()
#        #system.mem_ctrl1 = MemCtrl()
#        #system.mem_ctrl0.dram = DDR5_4400_4x8()
#        #system.mem_ctrl1.dram = DDR5_4400_4x8()
#        #system.mem_ctrl0.dram.range = system.mem_ranges[0]
#        #system.mem_ctrl1.dram.range = system.mem_ranges[1]
#        #system.mem_ctrl0.port = system.membus.mem_side_ports
#        #system.mem_ctrl1.port = system.membus.mem_side_ports
#print("dongwook debug] drams: ", drams)
#system.mem_ctrls = mem_ctrls

# Create a top-level voltage domain and clock domain
system.voltage_domain = VoltageDomain(voltage=args.sys_voltage)
system.clk_domain = SrcClockDomain(
    clock=args.sys_clock, voltage_domain=system.voltage_domain
)

## Create a seperate clock domain for memory controller
#for i in range(args.num_dirs):
#    if len(system.mem_ranges) > 1:
#        for j in range(len(system.mem_ranges)):
#            # print("middk_debug] i+j", len(system.mem_ranges)*i+j)
#            system.mem_ctrls[
#                len(system.mem_ranges) * i + j
#            ].clk_domain = SrcClockDomain(
#                clock="600MHz", voltage_domain=system.voltage_domain
#            )
#    else:
#        system.mem_ctrls[i].clk_domain = SrcClockDomain(
#            clock="600MHz", voltage_domain=system.voltage_domain
#        )
# Create a seperate clock domain for dma devices
for i in range(args.num_dmas):
    system.dma_devices[i].clk_domain = SrcClockDomain(
        clock="1GHz", voltage_domain=system.voltage_domain
    )


## PyTrafficGen create functions
def createRandomTraffic(tgen):
    yield tgen.createRandom(
        1000000000,  # duration
        80000000,  # start_addr
        AddrRange("2GB").end,  # end_addr
        64,  # block_size
        1000,  # min_period
        1000,  # max_period
        args.rd_prct,  # read_percent
        0,
    )  # data_limit
    yield tgen.createExit(0)


def createLinearTraffic(tgen):
    yield tgen.createLinear(
        1000000000,  # duration
        80000000,  # start_addr
        AddrRange("2GB").end,  # end_addr
        64,  # block_size
        1000,  # min_period
        1000,  # max_period
        args.rd_prct,  # read_percent
        0,
    )  # data_limit
    yield tgen.createExit(0)


def createTraceTraffic(tgen):
    yield tgen.createTrace(
        args.trace_duration,  # duration
        "/home/gem5/util/falcon_trace/test-trace.trc",  # trace_file
        0,
    )  # addr_offset
    yield tgen.createExit(0)


def createTraceTraffic_dma0(tgen):
    yield tgen.createTrace(
        args.trace_duration,  # duration
        "/home/gem5/util/falcon_trace/test-trace_dma0.trc",  # trace_file
        0,
    )  # addr_offset
    yield tgen.createExit(0)


def createTraceTraffic_dma1(tgen):
    yield tgen.createTrace(
        args.trace_duration,  # duration
        "/home/gem5/util/falcon_trace/test-trace_dma1.trc",  # trace_file
        0,
    )  # addr_offset
    yield tgen.createExit(0)


def createTraceTraffic_dma2(tgen):
    yield tgen.createTrace(
        args.trace_duration,  # duration
        "/home/gem5/util/falcon_trace/test-trace_dma2.trc",  # trace_file
        0,
    )  # addr_offset
    yield tgen.createExit(0)


def createTraceTraffic_dma3(tgen):
    yield tgen.createTrace(
        args.trace_duration,  # duration
        "/home/gem5/util/falcon_trace/test-trace_dma3.trc",  # trace_file
        0,
    )  # addr_offset
    yield tgen.createExit(0)


# -----------------------
# run simulation
# -----------------------

root = Root(full_system=False, system=system)
root.system.mem_mode = "timing"

# Not much point in this being higher than the L1 latency
m5.ticks.setGlobalFrequency("1ps")
# m5.ticks.setGlobalFrequency("1ns")

# instantiate configuration
m5.instantiate()

if args.traffic_mode_cpu == "linear":
    for i in range(args.num_cpus):
        root.system.cpu[i].start(createLinearTraffic(root.system.cpu[i]))
elif args.traffic_mode_cpu == "random":
    for i in range(args.num_cpus):
        root.system.cpu[i].start(createRandomTraffic(root.system.cpu[i]))
elif args.traffic_mode_cpu == "trace":
    for i in range(args.num_cpus):
        root.system.cpu[i].start(createTraceTraffic(root.system.cpu[i]))
else:
    print("Wrong CPU traffic type! Exiting!")
    exit()

if args.traffic_mode_dma == "linear":
    for i in range(args.num_dmas):
        root.system.dma_devices[i].start(
            createLinearTraffic(root.system.dma_devices[i])
        )
elif args.traffic_mode_dma == "random":
    for i in range(args.num_dmas):
        root.system.dma_devices[i].start(
            createRandomTraffic(root.system.dma_devices[i])
        )
elif args.traffic_mode_dma == "trace":
    root.system.dma_devices[0].start(
        createTraceTraffic_dma0(root.system.dma_devices[0])
    )
    root.system.dma_devices[1].start(
        createTraceTraffic_dma1(root.system.dma_devices[1])
    )
    root.system.dma_devices[2].start(
        createTraceTraffic_dma2(root.system.dma_devices[2])
    )
    root.system.dma_devices[3].start(
        createTraceTraffic_dma3(root.system.dma_devices[3])
    )
else:
    print("Wrong DMA traffic type! Exiting!")
    exit()

# simulate until program terminates
exit_event = m5.simulate(args.abs_max_tick)

print("Exiting @ tick", m5.curTick(), "because", exit_event.getCause())
