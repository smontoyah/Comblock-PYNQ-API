import sys
from pynq import Overlay, comblock


def main():

    ov = Overlay("/testFiles/design_1.bit")
    CB_L = ov.comblock.AXIL
    CB_F = ov.comblock.AXIF

    # para evitar la escritura de CB_L y CB_F separamos las clases
    IN_REGS = CB_L.IN_REGS
    OUT_REGS = CB_L.OUT_REGS
    FIFO_IN = CB_L.FIFO_IN
    FIFO_OUT = CB_L.FIFO_OUT
    DRAM = CB_F.DRAM

    # Prueba de los Registros
    # =======================================================
    Regs_depth = IN_REGS.depth  if (IN_REGS.depth < OUT_REGS.depth) else OUT_REGS.depth

    print("Testing the Input and output Registers...")
    print("=====================================\n")

    for i in range(Regs_depth):
        print("Writing %d in the Output REG%d \n"%(i,i))
        OUT_REGS.writeReg(i, i)
        
    for i in range(Regs_depth):
        print("Reading the Input REG%d = %d \n"%(i,IN_REGS.readReg(i)))

    # Prueba de las memorias FIFO
    # =======================================================

    Fifo_depth = FIFO_IN.depth  if (FIFO_IN.depth < FIFO_OUT.depth) else FIFO_OUT.depth

    print("Testing the Input and output FIFO...")
    print("=====================================\n")

    print("Writing the numbers from 0 to %d in the Output FIFO \n"%(Fifo_depth-1))
    for i in range(Fifo_depth):
        FIFO_OUT.writeF(i)
        
    print("Checking the Input FIFO values...\n")
    error = 0
    for i in range(Fifo_depth):
        val = FIFO_IN.readF()
        if val != i:
            error = 1
            break
        else:
            continue

    print("ERROR: FIFO_IN %d = %d"%(i, val) if (error == 1) else "The values match") 

    # Prueba de la memoria RAM
    # =======================================================
    print("Testing the DRAM...")
    print("=====================================\n")

    print("Writing the numbers from 0 to %d in the RAM \n"%(DRAM.depth-1))
    DRAM.writeBulk(0, [i for i in range(DRAM.depth)])
        
    print("Checking the DRAM values...\n")
    error = 0
    for i in range(DRAM.depth):
        val = DRAM.readRam(i)
        if val != i:
            error = 1
            break
        else:
            continue

    print("ERROR: DRAM %d = %d\n"%(i, val) if (error == 1) else "The values match\n") 

    # Muestra de transaciones invalidas
    # ======================================================
    print( "Testing some invalid transactions messages...\n")
    print(IN_REGS.readReg(4)) # Se intenta leer el registro 4 de entrada
    print(IN_REGS.readReg(17)) # Se intenta leer el registro 17 de entrada


if __name__ == '__main__':
    main()