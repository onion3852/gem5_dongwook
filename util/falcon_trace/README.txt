# The ASCII trace format uses one line per request on the format cmd,
# addr, size, tick. For example:
# r,128,64,4000
# w,232123,64,500000
# This trace reads 64 bytes from decimal address 128 at tick 4000,
# then writes 64 bytes to address 232123 at tick 500000.
