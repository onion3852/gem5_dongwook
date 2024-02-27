#!/bin/bash

GEM5_PATH=/home/gem5/build/ARM
CONFIG_PATH=/home/gem5/configs/example
GEM5_RUN_PATH=/home/gem5/run_script

$GEM5_PATH/gem5.opt \
	--outdir $GEM5_RUN_PATH/output_ruby_pytrafficgen \
	$CONFIG_PATH/ruby_pytrafficgen.py \
	--network=garnet \
	--topology FalconBusArch \
	--num-cpus 2 \
	--num-dmas 4 \
	--num-dirs 4 \
	--traffic_mode_cpu trace \
	--traffic_mode_dma trace \
	--trace_duration 500000000 \
	--mem-type DDR5_4400_4x8 \
	--sys-clock "900MHz" \
	--ruby-clock "600MHz" \
	| tee run_ruby_pytrafficgen.log

## options
	#--debug-flags=RubyQueue \
	#--debug-flags=RubyCache \
	#--debug-flags=MemCtrl \
	#--debug-flags=Ruby \
	#--debug-flags=RubyHitMiss \
	#--debug-flags=PacketQueue \
	#--debug-flags=TrafficGen \
	#--debug-flags=RubyNetwork \
	#--topology CrossbarGarnet \
	#--traffic_mode trace \
	#--traffic_mode linear \
	#--mem-channels 2 \
	#--trace_duration 4130000000 \
	#--tgen-cfg-file "./configs/example/dongwook_tgen.cfg" \
