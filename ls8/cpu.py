"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0]*8
        self.ram = [0]*256
        self.HLT = 0b1
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        

    def load(self, location):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        code = open(location, 'r')
        lines = code.readlines()
        program = []

        for line in lines:
            if line[0] == '1' or line[0] == '0':
                program.append(int(line[:8], 2))
        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        address = 0
        
        HLT = False

        while not HLT:
            IR = self.ram_read(address)
            operand_a = self.ram_read(address + 1)
            operand_b = self.ram_read(address + 2)
            #LDI
            if IR == self.LDI:
                self.reg[operand_a] = operand_b
                address += 3
            #PRN
            elif IR == self.PRN:
                print(int(self.reg[operand_a]))
                address += 2
            #HLT
            elif IR == self.HLT:
                HLT = True
    
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value