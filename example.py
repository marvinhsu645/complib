# convert a netlist to a tripartite graph
def netlist2trigraph(netlist):
    pass

# convert a tripartite graph to a bipartite graph
def tri2bigraph(graph):
    pass

# get Parts in a netlist
def get_comps(netlist):
    pass

# get Parts info in the component library
def get_info_from_complib(part):
    pass

# get patches from the info
def get_patches(info):
    pass

# subgraph isomorphism
def patch_detection(graph, patch):
    pass

def merge_blocks():
    pass

def hide_patches():
    pass

mpu9250_patch="(export (version D) \
                    (components \
                        (comp (ref #PWR1) \
                            (value GND) \
                            (libsource (lib power) (part GND)) \
                            (sheetpath (names /top/9252463163646315502) (tstamps /top/9252463163646315502))) \
                        (comp (ref #PWR2) \
                            (value VCC) \
                            (libsource (lib power) (part VCC)) \
                            (sheetpath (names /top/5533475186907887364) (tstamps /top/5533475186907887364))) \
                        (comp (ref C1) \
                            (value 0.1muF) \
                            (libsource (lib Device) (part C)) \
                            (sheetpath (names /top/15864663021404307731) (tstamps /top/15864663021404307731))) \
                        (comp (ref C2) \
                            (value 0.1muF) \
                            (libsource (lib Device) (part C)) \
                            (sheetpath (names /top/4757838341044565466) (tstamps /top/4757838341044565466))) \
                        (comp (ref C3) \
                            (value 10nF) \
                            (libsource (lib Device) (part C)) \
                            (sheetpath (names /top/2814596574783560753) (tstamps /top/2814596574783560753))) \
                        (comp (ref U1) \
                            (value MPU-9250) \
                            (libsource (lib MPU-9250) (part MPU-9250)) \
                            (sheetpath (names /top/14013186969592232737) (tstamps /top/14013186969592232737)))) \
                    (nets \
                        (net (code 1) (name N$1) \
                            (node (ref #PWR1) (pin 1)) \
                            (node (ref C1) (pin 2)) \
                            (node (ref C2) (pin 2)) \
                            (node (ref C3) (pin 2)) \
                            (node (ref U1) (pin 18)) \
                            (node (ref U1) (pin 20))) \
                        (net (code 2) (name N$2) \
                            (node (ref #PWR2) (pin 1)) \
                            (node (ref C2) (pin 1)) \
                            (node (ref U1) (pin 13))) \
                        (net (code 3) (name N$3) \
                            (node (ref #PWR2) (pin 1)) \
                            (node (ref U1) (pin 1))) \
                        (net (code 4) (name N$4) \
                            (node (ref C1) (pin 1)) \
                            (node (ref U1) (pin 10))) \
                        (net (code 5) (name N$5) \
                            (node (ref #PWR2) (pin 1)) \
                            (node (ref C3) (pin 1)) \
                            (node (ref U1) (pin 8)))) \
                )"

# # vertices
# blocks = {"PWR1", "PWR2", "C1", "C2", "C3", "U1"}
# pinblocks = {"U1_1", "U1_2", "U1_3", "U1_4", "U1_5", "U1_6", "U1_7", "U1_8", "U1_9", "U1_10", "U1_11", "U1_12", "U1_13", "U1_14", "U1_15", "U1_16", "U1_17", "U1_18", "U1_19", "U1_20", "U1_21", "U1_22", "U1_23", "U1_24", "U1_25",
#              "C1_1", "C1_2", "C2_1", "C2_2", "C3_1", "C3_2", "PWR1_1", "PWR2_1"}
# nets = {"N1", "N2", "N3", "N4", "N5"}

# ------------------------------------------- #

## Schematic to Block Diagram

mpu9250_netlist = "..."     # input

T_mpu9250 = netlist2trigraph(mpu9250_netlist)   # get tripartite graph
T_mpu9250 = {("U1", "U1_1"), ("U1", "U1_2"), ("U1", "U1_3"), ("U1", "U1_4"), ("U1", "U1_5"), ("U1", "U1_6"), ("U1", "U1_7"), ("U1", "U1_8"), ("U1", "U1_9"), ("U1", "U1_10"), ("U1", "U1_11"), ("U1", "U1_12"), ("U1", "U1_13"), ("U1", "U1_14"), ("U1", "U1_15"), ("U1", "U1_16"), ("U1", "U1_17"), ("U1", "U1_18"), ("U1", "U1_19"), ("U1", "U1_20"), ("U1", "U1_21"), ("U1", "U1_22"), ("U1", "U1_23"), ("U1", "U1_24"), ("U1", "U1_25"),
             ("C1", "C1_1"), ("C1", "C1_2"),
             ("C2", "C2_1"), ("C2", "C2_2"),
             ("C3", "C3_1"), ("C3", "C3_2"),
             ("PWR1", "PWR1_1"), ("PWR1", "PWR2_1"), # b-p
             ("N1", "U1_18"), ("N1", "U1_20"), ("N1", "PWR1_1"), ("N1", "C1_2"), ("N1", "C2_2"), ("N1", "C3_2"), # p-n
             ("N2", "PWR2_1"), ("N2", "C2_1"), ("N2", "U1_13"),
             ("N3", "PWR2_1"), ("N3", "U1_1"),
             ("N4", "C1_1"), ("N4", "U1_10"),
             ("N5", "PWR2_1"), ("N5", "C3_1"), ("N5", "U1_8")}

B_mpu9250 = tri2bigraph(T_mpu9250)              # get bipartite graph
B_mpu9250 = {("N1", "U1"), ("N1", "PWR1"), ("N1", "C1"), ("N1", "C2"), ("N1", "C3"), 
             ("N2", "PWR2"), ("N2", "C2"), ("N2", "U1"),
             ("N3", "PWR2"), ("N3", "U1"),
             ("N4", "C1"), ("N4", "U1"), 
             ("N5", "PWR2"), ("N5", "C3"), ("N5", "U1")}

netlist_comps = get_comps(mpu9250_netlist)
# ["PWR1", "PWR2", "C1", "C2", "C3", "U1"]

netlist_comps_info = get_info_from_complib(netlist_comps)
# {"U1": {name='MPU-9250', tagset={'IMU', 'Accelerometer'}...}

netlist_patches = get_patches(netlist_comps_info)
# B_patch = [{("N1", "U1"), ("N1", "C1")}, {...}, {...}]

matched_patches = patch_detection(B_mpu9250, netlist_patches)

if matched_patches != None:
    merge_blocks()

T_mpu9250 = hide_patches()

## Unrefinement