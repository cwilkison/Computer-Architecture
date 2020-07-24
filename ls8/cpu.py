"""CPU functionality."""

import sys
LDI = 0b10000010 
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.sp = 7


    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        cleaned = []
        # print(filename)
        for line in filename:
            # print(line)
            line1 = line.strip()
            if not line1.startswith('#') and line1.strip():
                line2 = line1.split('#', 1)[0]
                # print(line2)
                cleaned.append(int(line2, 2))
                # print(line2)

        for instruction in cleaned:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ldi(self, register, value):
        self.reg[register] = value

    def prn(self, index):
        print(self.reg[index])

    def hlt(self):
        sys.exit(0)

    def push(self, operand_a, operand_b):
        self.sp -= 1
        self.ram_write(self.sp, self.reg[operand_a])
        self.pc += 2
    
    def pop(self, operand_a, operand_b):
        self.reg[operand_a] = self.ram_read(self.sp)
        self.sp += 1
        self.pc += 2

    def call(self, operand_a):
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.pc + 2
        self.pc = self.reg[operand_a]

    def ret(self):
        self.pc = self.ram[self.reg[7]]
        self.reg[7] += 1

    def run(self):
        """Run the CPU."""
        # number of operands = inst value & 0b11000000 >> 6
        # inst length = number of operands + 1
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        


        running = True
        # self.trace()
        while running is True:
            inst = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            
            if inst == LDI:
                # self.reg[operand_a] = operand_b
                self.ldi(operand_a, operand_b)
                self.pc += 3
            
            elif inst == PRN:
                self.prn(operand_a)
                self.pc += 2
            
            elif inst == HLT:
                self.hlt()
                self.pc += 1
                running = False

            elif inst == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif inst == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            
            elif inst == PUSH:
                self.push(operand_a, operand_b)

            elif inst == POP:
                self.pop(operand_a, operand_b)
            
            elif inst == CALL:
                self.call(operand_a)
            
            elif inst == RET:
                self.ret()
                
            else:
                print("unknown instruction")
                print(bin(inst))
                running = False