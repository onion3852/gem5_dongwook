#!/bin/bash

UTIL_PATH=/home/gem5/util

$UTIL_PATH/encode_packet_trace.py test-trace_dma0.ascii test-trace_dma0.trc
$UTIL_PATH/encode_packet_trace.py test-trace_dma1.ascii test-trace_dma1.trc
$UTIL_PATH/encode_packet_trace.py test-trace_dma2.ascii test-trace_dma2.trc
$UTIL_PATH/encode_packet_trace.py test-trace_dma3.ascii test-trace_dma3.trc
