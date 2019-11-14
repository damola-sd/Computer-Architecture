"""CPU functionality."""

import sys
import os

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 244

    def ram_read(self, mem) :
        return self.ram[mem]

    def ram_write(self, mem, value):
        self.ram[mem] = value

        
    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        examples_dir = os.path.join(os.path.dirname(__file__), "examples/")
        file_path = os.path.join(examples_dir, file_name)

        try:
            with open(file_path) as f:
                for line in f:
                    num = line.split("#", 1)[0]
                    # print(num)

                    if num.strip() != "":
                       self.ram_write(address, int(num, 2))
                       address += 1 

        except FileNotFoundError:
            print(f"{file_name} not found")
            sys.exit(2)

        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        """Run the CPU."""
        IR = self.ram[self.pc]
        PRN = 0b01000111
        LDI = 0b10000010
        HLT = 0b00000001
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101
        CALL = 0b01010000
        RET = 0b00010001

        running = True

        while running:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                # print("Entered LDI Else If")
                self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
                self.pc += 3
            elif IR == PRN:
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2
            elif IR == HLT:
                running = False
            elif IR == MUL: 
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2
            elif IR == PUSH:
                #Decrement the Special Pointer
                # self.reg[self.sp] -= 1
                # val = self.reg[self.ram[self.pc + 1]]
                # self.ram[self.reg[self.sp]] = val
                # self.pc += 2
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
            
                # Decrement the SP.
                self.reg[self.sp] -= 1
                # Copy the value in the given register to the address pointed to by SP.
                self.ram[self.reg[self.sp]] = val
                self.pc += 2

            elif IR == POP:
                # value = self.ram[self.reg[self.sp]]
                # reg = self.ram[self.pc + 1]
                # self.reg[self.ram[self.pc + 1]] = value
                # #Increment the Special Pointer
                # self.reg[self.sp] += 1
                # self.pc += 2
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[self.sp]]
                # Copy the value from the address pointed to by SP to the given register.
                self.reg[reg] = val
                # Increment SP.
                self.reg[self.sp] += 1
                self.pc += 2 


            elif IR == CALL:
                # print("Entered the Call ElIF")
                #Decrement the Special Pointer
                self.reg[self.sp] -= 1
                
                self.ram[self.reg[self.sp]] = self.pc + 2
                register_num = self.ram[self.pc + 1]
                subroutine = self.reg[register_num]
                self.pc = subroutine
            
            elif IR == RET:
                #Increment the Special Pointer
                print('RET')
                return_addr = self.ram[self.reg[self.sp]]
                self.pc = return_addr

                self.reg[self.sp] += 1

            else:
                print(f"Unknown Instruction")
                sys.exit(1)
                


