# Copyright (c) 2010 Advanced Micro Devices, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.params import *
from m5.objects import *

from topologies.BaseTopology import SimpleTopology


class FalconBusArch(SimpleTopology):
    description = "FalconBusArch"

    def makeTopology(self, options, network, IntLink, ExtLink, Router):

        # default values for link latency and router latency.
        # Can be over-ridden on a per link/router basis
        link_latency = options.link_latency  # used by simple and garnet
        router_latency = options.router_latency  # only used by garnet

        # middk

        controller_to_string = []

        for (i, n) in enumerate(self.nodes):
            print("middk_debug] ", n)
            controller_to_string.append(str(n))
            if "cpu0.l1i" in controller_to_string[i]:
                cpu0_l1i = n
            elif "cpu0.l1d" in controller_to_string[i]:
                cpu0_l1d = n
            elif "cpu0.l2" in controller_to_string[i]:
                cpu0_l2 = n
            elif "cpu1.l1i" in controller_to_string[i]:
                cpu1_l1i = n
            elif "cpu1.l1d" in controller_to_string[i]:
                cpu1_l1d = n
            elif "cpu1.l2" in controller_to_string[i]:
                cpu1_l2 = n
            elif "hnf" in controller_to_string[i]:
                hnf = n
            elif "dma_rni0" in controller_to_string[i]:
                dma0 = n
            elif "dma_rni1" in controller_to_string[i]:
                dma1 = n
            elif "dma_rni2" in controller_to_string[i]:
                dma2 = n
            elif "dma_rni3" in controller_to_string[i]:
                dma3 = n
            elif "snf0" in controller_to_string[i]:
                snf0 = n
            elif "snf1" in controller_to_string[i]:
                snf1 = n
            elif "snf2" in controller_to_string[i]:
                snf2 = n
            elif "snf3" in controller_to_string[i]:
                snf3 = n

        router_count = 0
        routers = []

        ## make routers for
        #
        # routers00 -> cpu0
        # routers01 -> cpu1
        # routers02 -> hnf
        # routers03 -> d5l
        # routers04 -> d5r
        # routers05 -> main bus
        # routers06 -> dma0
        # routers07 -> dma1
        # routers08 -> dma2
        # routers09 -> dma3
        ##

        for i in range(10):
            routers.append(
                Router(
                    router_id=router_count,
                    width=512,
                )
            )
            router_count += 1

        network.routers = routers

        # for (i, n) in enumerate(routers):
        #    print("middk_debug] ", n)

        # cpu
        cpu0 = [cpu0_l1i, cpu0_l1d, cpu0_l2]
        cpu1 = [cpu1_l1i, cpu1_l1d, cpu1_l2]
        l3 = [hnf]
        dmas = [dma0, dma1, dma2, dma3]
        d5l = [snf0, snf1]
        d5r = [snf2, snf3]

        link_count = 0

        ## External Link
        ext_links = []

        for (i, n) in enumerate(cpu0):
            ext_links.append(
                ExtLink(
                    link_id=link_count,  # Ext 0~2
                    ext_node=n,
                    int_node=routers[0],
                    latency=link_latency,
                    width=128,
                    ext_cdc=True,
                    int_cdc=False,
                    ext_serdes=False,
                    int_serdes=True,
                )
            )
            link_count += 1

        for (i, n) in enumerate(cpu1):
            ext_links.append(
                ExtLink(
                    link_id=link_count,  # Ext 3~5
                    ext_node=n,
                    int_node=routers[1],
                    latency=link_latency,
                    width=128,
                    ext_cdc=True,
                    int_cdc=False,
                    ext_serdes=False,
                    int_serdes=True,
                )
            )
            link_count += 1

        for (i, n) in enumerate(l3):
            ext_links.append(
                ExtLink(
                    link_id=link_count,  # Ext 6
                    ext_node=n,
                    int_node=routers[2],
                    latency=link_latency,
                    width=512,
                    ext_cdc=False,
                    int_cdc=False,
                    ext_serdes=False,
                    int_serdes=False,
                )
            )
            link_count += 1

        for (i, n) in enumerate(d5l):
            ext_links.append(
                ExtLink(
                    link_id=link_count,  # Ext 7~8
                    ext_node=n,
                    int_node=routers[3],
                    latency=link_latency,
                    width=256,
                    ext_cdc=False,
                    int_cdc=False,
                    ext_serdes=False,
                    int_serdes=True,
                )
            )
            link_count += 1

        for (i, n) in enumerate(d5r):
            ext_links.append(
                ExtLink(
                    link_id=link_count,  # Ext 9~10
                    ext_node=n,
                    int_node=routers[4],
                    latency=link_latency,
                    width=256,
                    ext_cdc=False,
                    int_cdc=False,
                    ext_serdes=False,
                    int_serdes=True,
                )
            )
            link_count += 1

        for (i, n) in enumerate(dmas):
            ext_links.append(
                ExtLink(
                    link_id=link_count,  # Ext 11~14
                    ext_node=n,
                    int_node=routers[6 + i],
                    latency=link_latency,
                    width=512,
                    ext_cdc=False,
                    int_cdc=True,
                    ext_serdes=False,
                    int_serdes=False,
                )
            )
            link_count += 1

        network.ext_links = ext_links

        ## Internal Link
        int_links = []

        int_links.append(
            IntLink(
                link_id=link_count,  # Int 0
                src_node=routers[0],
                dst_node=routers[2],
                latency=link_latency,
                src_cdc=False,
                dst_cdc=False,
                src_serdes=False,
                dst_serdes=False,
                width=512,
            )
        )
        link_count += 1

        int_links.append(
            IntLink(
                link_id=link_count,  # Int 1
                src_node=routers[2],
                dst_node=routers[0],
                latency=link_latency,
                src_cdc=False,
                dst_cdc=False,
                src_serdes=False,
                dst_serdes=False,
                width=512,
            )
        )
        link_count += 1

        int_links.append(
            IntLink(
                link_id=link_count,  # Int 2
                src_node=routers[1],
                dst_node=routers[2],
                latency=link_latency,
                src_cdc=False,
                dst_cdc=False,
                src_serdes=False,
                dst_serdes=False,
                width=512,
            )
        )
        link_count += 1

        int_links.append(
            IntLink(
                link_id=link_count,  # Int 3
                src_node=routers[2],
                dst_node=routers[1],
                latency=link_latency,
                src_cdc=False,
                dst_cdc=False,
                src_serdes=False,
                dst_serdes=False,
                width=512,
            )
        )
        link_count += 1

        int_links.append(
            IntLink(
                link_id=link_count,  # Int 4
                src_node=routers[2],
                dst_node=routers[3],
                latency=link_latency,
                src_cdc=False,
                dst_cdc=False,
                src_serdes=False,
                dst_serdes=False,
                width=512,
            )
        )
        link_count += 1

        int_links.append(
            IntLink(
                link_id=link_count,  # Int 5
                src_node=routers[3],
                dst_node=routers[2],
                latency=link_latency,
                src_cdc=False,
                dst_cdc=False,
                src_serdes=False,
                dst_serdes=False,
                width=512,
            )
        )
        link_count += 1

        int_links.append(
            IntLink(
                link_id=link_count,  # Int 6
                src_node=routers[2],
                dst_node=routers[4],
                latency=link_latency,
                src_cdc=False,
                dst_cdc=False,
                src_serdes=False,
                dst_serdes=False,
                width=512,
            )
        )
        link_count += 1

        int_links.append(
            IntLink(
                link_id=link_count,  # Int 7
                src_node=routers[4],
                dst_node=routers[2],
                latency=link_latency,
                src_cdc=False,
                dst_cdc=False,
                src_serdes=False,
                dst_serdes=False,
                width=512,
            )
        )
        link_count += 1

        int_links.append(
            IntLink(
                link_id=link_count,  # Int 8
                src_node=routers[2],
                dst_node=routers[5],
                latency=link_latency,
                src_cdc=False,
                dst_cdc=False,
                src_serdes=False,
                dst_serdes=False,
                width=512,
            )
        )
        link_count += 1

        int_links.append(
            IntLink(
                link_id=link_count,  # Int 9
                src_node=routers[5],
                dst_node=routers[2],
                latency=link_latency,
                src_cdc=False,
                dst_cdc=False,
                src_serdes=False,
                dst_serdes=False,
                width=512,
            )
        )
        link_count += 1

        for i in range(4):
            for j in range(3):
                int_links.append(
                    IntLink(
                        link_id=link_count,  # Int 10~12, 13~15, 16~18, 19~21
                        src_node=routers[6 + i],
                        dst_node=routers[3 + j],
                        latency=link_latency,
                        src_cdc=False,
                        dst_cdc=True,
                        src_serdes=False,
                        dst_serdes=False,
                        width=512,
                    )
                )
                link_count += 1

        for i in range(3):
            for j in range(4):
                int_links.append(
                    IntLink(
                        link_id=link_count,  # Int 22~25, 26~29, 30~33
                        src_node=routers[3 + i],
                        dst_node=routers[6 + j],
                        latency=link_latency,
                        src_cdc=False,
                        dst_cdc=True,
                        src_serdes=False,
                        dst_serdes=False,
                        width=512,
                    )
                )
                link_count += 1

        # dongwook start
        # int_links.append(
        #     IntLink(
        #         link_id=link_count, # Int 34 (6 to 2)
        #         src_node=routers[6],
        #         dst_node=routers[2],
        #         latency=link_latency,
        #         src_cdc=False,
        #         dst_cdc=True,
        #         src_serdes=False,
        #         dst_serdes=False,
        #         width=512
        #     )
        # )
        # int_links.append(
        #     IntLink(
        #         link_id=link_count, # Int 35 (2 to 6)
        #         src_node=routers[2],
        #         dst_node=routers[6],
        #         latency=link_latency,
        #         src_cdc=False,
        #         dst_cdc=True,
        #         src_serdes=False,
        #         dst_serdes=False,
        #         width=512
        #     )
        # )
        # dongwook end

        network.int_links = int_links
