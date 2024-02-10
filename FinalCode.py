import re
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# a dictionary for convert binary numbers to hex
binary_to_hex_dict = {
    '0000': '0',
    '0001': '1',
    '0010': '2',
    '0011': '3',
    '0100': '4',
    '0101': '5',
    '0110': '6',
    '0111': '7',
    '1000': '8',
    '1001': '9',
    '1010': 'A',
    '1011': 'B',
    '1100': 'C',
    '1101': 'D',
    '1110': 'E',
    '1111': 'F'
}
# a dictionary for 32-bit registers and opcodes
registers_32bit = {
    'eax': "000",
    'ebx': "011",
    'ecx': '001',
    'edx': '010',
    'esi': '110',
    'edi': '111',
    'esp': '100',
    'ebp': '101'
}
# a dictionary for 16-bit registers and opcodes
registers_16bit = {
    'ax': "000",
    'bx': "011",
    'cx': '001',
    'dx': '010',
    'si': '110',
    'di': '111',
    'sp': '100',
    'bp': '101'
}
# a dictionary for 8-bit registers and opcodes
registers_8bit = {
    'al': '000',
    'bl': '011',
    'cl': '001',
    'dl': '010',
    'ah': '100',
    'bh': '111',
    'ch': '101',
    'dh': '110'
}
# a dictionary for 32-bit memory and opcodes
registers_32bit_MOD00 = {
     '[eax]': "000",
     '[ebx]': "011",
     '[ecx]': '001',
     '[edx]': '010',
     '[esi]': '110',
     '[edi]': '111',
     '[esp]': '100',
     '[ebp]': '101'
}
# a dictionary for instructions opcodes
instructionOpcode = {
    'ADD': '000000',
    'SUB': '001010',
    'AND': '001000',
    'OR': '000010',
    'XOR': '001100',
    'PUSH': '01010',
    'POP': '01011',
    'INC': '01000',
    'DEC': '01001'
}
# these comment are for 16-bit and 8-bit memory that are not in project
# registers_16bit_MOD00 = {
#      '[ax]': "000",
#      '[bx]': "011",
#      '[cx]': '001',
#      '[dx]': '010',
#      '[si]': '110',
#      '[di]': '111',
#      '[sp]': '100',
#      '[bp]': '101'
# }
# registers_8bit_MOD00 = {
#     '[al]': '000',
#     '[bl]': '011',
#     '[cl]': '001',
#     '[dl]': '010',
#     '[ah]': '100',
#     '[bh]': '111',
#     '[ch]': '101',
#     '[dh]': '110'
# }


printArray = []

counter = 0


# a function to convert the binary of assemble code into hex(32-bit and 8-bit)
def binary_to_hex(number):
    global counter

    hex_value = (
        binary_to_hex_dict[number[0][0:4]] +
        binary_to_hex_dict[number[0][4:8]] +
        binary_to_hex_dict[number[0][8:12]] +
        binary_to_hex_dict[number[0][12:16]]
    )
    printArray.append(["0x"+f"{counter:015d}: {hex_value}"])
    counter += 2


# a function to convert the binary of assemble code into hex(16-bit)
def binary_to_hex_16bit(number):
    global counter

    hex_value = '66' + (
        binary_to_hex_dict[number[0][0:4]] +
        binary_to_hex_dict[number[0][4:8]] +
        binary_to_hex_dict[number[0][8:12]] +
        binary_to_hex_dict[number[0][12:16]]
    )
    printArray.append(["0x"+f"{counter:015d}: {hex_value}"])
    counter += 3


# a function to convert the binary of assemble code into hex for one operand instructions(32_bit)
def binary_to_hex_one_operand(number):
    global counter

    hex_value = (
        binary_to_hex_dict[number[0][0:4]] +
        binary_to_hex_dict[number[0][4:8]]
    )
    printArray.append(["0x"+f"{counter:015d}: {hex_value}"])
    counter += 1


# a function to convert the binary of assemble ode into hex for one operand instructions(16_bit)
def binary_to_hex_16_bit_one_operand(number):
    global counter

    hex_value = '66' + (
        binary_to_hex_dict[number[0][0:4]] +
        binary_to_hex_dict[number[0][4:8]]
    )
    printArray.append(["0x"+f"{counter:015d}: {hex_value}"])
    counter += 2


# a function to convert the binary of assemble code into hex for one operand instructions(8_bit)
def binary_to_hex_8_bit_one_operand(number):
    global counter

    hex_value = ("FE"+
        binary_to_hex_dict[number[0][0:4]] +
        binary_to_hex_dict[number[0][4:8]]
    )
    printArray.append(["0x"+f"{counter:015d}: {hex_value}"])
    counter += 2


number = []  # a list for save the binary code of assembly code


# create 16 complement of the address of jump if it is negative
def complement16(num):
    hexnum = [*num]
    for i in range(len(hexnum)):
        hexnum[i] = hex(15 - int(hexnum[i], 16))[2:]
    temp = "".join(hexnum)
    if len(hexnum) < 2:
        temp = "f" + temp
    return hex((int(temp, 16)) + 1)[2:]


# process function to build the binary number
def main_process(instruction, first_arg, second_arg):
    if first_arg in registers_32bit and second_arg in registers_32bit:
        number.append(instructionOpcode[instruction.upper()]+'01' + '11' + registers_32bit[second_arg]+registers_32bit[first_arg])
        binary_to_hex(number)
    elif first_arg in registers_16bit and second_arg in registers_16bit:
        number.append(instructionOpcode[instruction.upper()]+'01' + '11' + registers_16bit[second_arg]+registers_16bit[first_arg])
        binary_to_hex_16bit(number)
    elif first_arg in registers_8bit and second_arg in registers_8bit:
        number.append(instructionOpcode[instruction.upper()] + '00' + '11' + registers_8bit[second_arg] + registers_8bit[first_arg])
        binary_to_hex(number)
    elif first_arg in registers_32bit_MOD00 and second_arg in registers_32bit:
        number.append(instructionOpcode[instruction.upper()] + '01' + '00' + registers_32bit[second_arg] + registers_32bit_MOD00[first_arg])
        binary_to_hex(number)
    elif first_arg in registers_32bit_MOD00 and second_arg in registers_16bit:
        number.append(instructionOpcode[instruction.upper()] + '01' + '00' + registers_16bit[second_arg] + registers_32bit_MOD00[first_arg])
        binary_to_hex_16bit(number)
    elif first_arg in registers_32bit_MOD00 and second_arg in registers_8bit:
        number.append(instructionOpcode[instruction.upper()] + '00' + '00' + registers_8bit[second_arg] + registers_32bit_MOD00[first_arg])
        binary_to_hex(number)
    elif first_arg in registers_32bit and second_arg in registers_32bit_MOD00:
        number.append(instructionOpcode[instruction.upper()] + '11' + '00' + registers_32bit[first_arg] + registers_32bit_MOD00[second_arg])
        binary_to_hex(number)
    elif first_arg in registers_16bit and second_arg in registers_32bit_MOD00:
        number.append(instructionOpcode[instruction.upper()] + '11' + '00' + registers_16bit[first_arg] + registers_32bit_MOD00[second_arg])
        binary_to_hex_16bit(number)
    elif first_arg in registers_8bit and second_arg in registers_32bit_MOD00:
        number.append(instructionOpcode[instruction.upper()] + '10' + '00' + registers_8bit[first_arg] + registers_32bit_MOD00[second_arg])
        binary_to_hex(number)
    elif first_arg in registers_32bit:
        number.append(instructionOpcode[instruction.upper()] + registers_32bit[first_arg])
        binary_to_hex_one_operand(number)
    elif first_arg in registers_16bit:
        number.append(instructionOpcode[instruction.upper()] + registers_16bit[first_arg])
        binary_to_hex_16_bit_one_operand(number)
    elif first_arg in registers_8bit:
        if instruction.upper() == "INC":
            number.append("11000" + registers_8bit[first_arg])
        elif instruction.upper() == "DEC":
            number.append("11001" + registers_8bit[first_arg])
        binary_to_hex_8_bit_one_operand(number)
    elif instruction.upper() == "JMP":
        global counter
        printArray.append([])
        jmp_dict[first_arg] = counter
        counter += 2
    elif instruction.upper() == "PUSH" and ((int(first_arg)) >= -129) or (int(first_arg) <= 128):
        if int(first_arg) > 0:
            hex_value = hex(int(first_arg))[2:]

        else:
            hex_value = str(complement16(hex(int(first_arg))[3:]))
        temp = ""
        for i in range(len(hex_value) - 2, -1, -2):
            temp += hex_value[i] + hex_value[i + 1] + " "
        printArray.append(["0x" + f"{counter:015d}: 6a{temp}"])
        counter += 2


# read the text file and call the main process here
def assemble_code_from_text(code):
    global counter, printArray, label_dict, jmp_dict

    # Reset global variables
    counter = 0
    printArray = []
    label_dict = {}
    jmp_dict = {}

    # Split each line into components (operation, operand1, operand2)
    lines = code.split('\n')

    # check that if is that line is label or not
    def is_label(line):
        return re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:$', line)

    # add the label into labels dictionary with its offset
    def handle_label(line):
        global counter
        label = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:$', line).group(1)
        label_dict[label] = counter

    # iterate the file line by line for instructions
    for line in lines:
        if line != '':
            if is_label(line):
                printArray.append(["0x" + f"{counter:015d}: {line} NOTHING"])
                handle_label(line)
            else:
                components = re.split(r'\s|,\s*', line)
                instructions = components[0].upper()
                first_arg = components[1] if len(components) > 1 else None
                second_arg = components[2] if len(components) > 2 else None

                main_process(instructions, first_arg, second_arg)

    # fix the print array for jumps
    def JmpHandle():
        temp = []
        index = 0
        for j in jmp_dict:
            for i in label_dict:
                if j == i:
                    temp.append(label_dict[i] - (jmp_dict[j] + 2))

            for i in range(len(printArray)):
                if not printArray[i]:
                    if temp[index] >= 0:
                        printArray[i] = ["0x" + f"{jmp_dict[j]:015d}: EB0{temp[index]}"]
                    else:
                        temp[index] = str(complement16(hex(int(temp[index]))[3:])).upper()
                        printArray[i] = ["0x" + f"{jmp_dict[j]:015d}: EB{temp[index]}"]
                    index += 1
                    break

    JmpHandle()

    return printArray


# loading the file
def load_file_data():
    file_path = filedialog.askopenfilename(title="Select Assembly File", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            file_data = file.read()
        file_data_text.delete(1.0, tk.END)
        file_data_text.insert(tk.END, file_data)


def assemble_loaded_file():
    file_data = file_data_text.get(1.0, tk.END)
    if file_data.strip():
        try:
            assembled_code = assemble_code_from_text(file_data)
            assembled_code_text.delete(1.0, tk.END)
            for line in assembled_code:
                assembled_code_text.insert(tk.END, line[0] + '\n')
        except Exception as e:
            assembled_code_text.delete(1.0, tk.END)
            assembled_code_text.insert(tk.END, f"Error: {str(e)}")
    else:
        assembled_code_text.delete(1.0, tk.END)
        assembled_code_text.insert(tk.END, "No data to assemble.")


# Create the main GUI window
root = tk.Tk()
root.title("Assembly Code Assembler")
root.iconbitmap("codingbrowser_102152.ico")  # Replace "icon.ico" with your icon file
root.configure(bg='#282c34')  # Set the window background color

custom_font = ("Comic Sans MS", 12)

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#61dafb", foreground="#282c34", font=custom_font)  # Stylish button style

# Create and configure widgets
load_button = ttk.Button(root, text="Load File", command=load_file_data, style="TButton")
load_button.grid(row=0, column=0, pady=10, padx=10)

# Create a light gray frame as a border for the load window
load_frame = tk.Frame(root, bg='#e0e0e0', bd=3)  # Add a border width of 3
load_frame.grid(row=1, column=0, padx=10, pady=10)

file_data_text = tk.Text(load_frame, height=20, width=40, bg='#e0e0e0', fg='#282c34', insertbackground='#282c34', font=custom_font)
file_data_text.pack(padx=10, pady=10)

assemble_button = ttk.Button(root, text="Assemble", command=assemble_loaded_file, style="TButton")
assemble_button.grid(row=0, column=1, pady=10, padx=10)

# Create a light gray frame as a border for the assemble window
assemble_frame = tk.Frame(root, bg='#e0e0e0', bd=3)  # Add a border width of 3
assemble_frame.grid(row=1, column=1, padx=10, pady=10)

assembled_code_text = tk.Text(assemble_frame, height=20, width=40, bg='#e0e0e0', fg='#282c34', insertbackground='#282c34', font=custom_font)
assembled_code_text.pack(padx=10, pady=10)

# Run the main event loop
root.mainloop()

