#!/bin/bash

GEM5_PATH=/home/gem5/build/ARM
CONFIG_PATH=/home/gem5/configs/example
GEM5_RUN_PATH=/home/gem5/run_script

$GEM5_PATH/gem5.opt \
	--outdir $GEM5_RUN_PATH/test_output_ruby_pytrafficgen \
	$CONFIG_PATH/ruby_pytrafficgen.py \
	--network=garnet \
	--topology CrossbarGarnet \
	--num-cpus 1 \
	--num-dmas 1 \
	--traffic_mode trace \
	--mem-type DDR5_4400_4x8 \
	--num-dirs 1 \
	--sys-clock "900MHz" \
	--ruby-clock "1GHz" \

## options
	#--debug-flags=RubyNetwork \
	#--outdir $GEM5_RUN_PATH/output_ruby_pytrafficgen_test \
	#--debug-flags=TrafficGen \
	#--topology FalconBusArch \
	#--topology CrossbarGarnet \
	#--traffic_mode linear \
	#--mem-channels 2 \
	#--debug-flags=Ruby \
