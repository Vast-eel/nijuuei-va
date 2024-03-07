import os
import sys
import struct
import unicodedata

def byte_invert(array):
    for i in range(0, len(array)):
        array[i] = ~array[i] + 256


class KagePhraseData:
    file_name = ""
    file_size = 0

    phrases = []
    offsets = []
    
    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.file_size = os.path.getsize(file_name)
        if (mode == 0):
            self.file = open(self.file_name, mode="rb")
            self.output = open(self.file_name + ".txt", mode="w", encoding="shift_jis")
        elif (mode == 1):
            self.file = open(self.file_name + ".txt", mode="r", encoding="shift_jis")
            self.output = open(self.file_name, mode="w+b")

    def decrypt_string(self, name_length):
        last_pos = self.file.tell()
        name_string = bytearray(self.file.read(name_length))
        byte_invert(name_string)
        if len(name_string) % 2 != 0:
            last_pos -= 1
        self.file.seek(last_pos)
        return name_string.decode("shift_jis")

    def encrypt_string(self, s):
        name_string = bytearray(s, "shift_jis")
        byte_invert(name_string)
        return name_string
        
    def read_commands(self):
        self.file.seek(4, 0)
        index = 0
        phrase_count = struct.unpack('<I', self.file.read(4))[0]
        while index < phrase_count:
            self.offsets.append(struct.unpack('<I', self.file.read(4))[0])
            index += 1
            
        index = 0
        while self.file.tell() != self.file_size:
            for i in self.offsets:
                if self.file.tell() == i:
                    self.phrases.append([])
                    length = struct.unpack('<H', self.file.read(2))[0]
                    string = self.decrypt_string(length)
                    self.phrases[index].append(string)
                    self.file.seek(length, 1)
                    
                    length = struct.unpack('<H', self.file.read(2))[0]
                    string = self.decrypt_string(length)
                    self.phrases[index].append(string)                    
                    
                    index += 1              
                          
            self.file.seek(2, 1) 
            
    def script_decompile(self):
        self.file.seek(4, 0)
        
        for i in range(len(self.phrases)):
            self.output.write('#' + str(i) + '\n')
            self.output.write(self.phrases[i][0] + '\n' + self.phrases[i][1] + '\n\n')
            
        self.file.close()
        self.output.close()
            
    def script_compile(self):
        lines = self.file.read().split('\n\n')
        lines = [line for line in lines if line]
        
        index = 0
        counter = 0
        while index < len(lines):
            plaintext = lines[index].split('\n', 2)
            if '#' in plaintext[0]:
                self.phrases.append([])
                counter = int(plaintext[0][1:])
                self.phrases[counter].append(plaintext[1])
                self.phrases[counter].append(plaintext[2])    
                
            index += 1 
        
        self.output.write(b"KPD1")
        self.output.write(struct.pack('<I', counter + 1))
        header_length = counter * 4 + 12
        self.output.write(struct.pack('<I', header_length))
        for i in range(counter):
            self.output.write(struct.pack('<I', 0))
        for i in self.phrases:
            for x in range(len(i)):
                if x == 0:
                    self.offsets.append(self.output.tell())
                    
                calc_length = 0
                normal_width_characters = 0
                
                for c in i[x]:
                    status = unicodedata.east_asian_width(c)
                    if status == 'Na':
                        calc_length += 1
                        normal_width_characters += 1
                    elif status == 'N':
                        calc_length += 1
                    else:
                        calc_length += 2
                        
                self.output.write(struct.pack('<H', calc_length))
                self.output.write(self.encrypt_string(i[x]))
        self.output.seek(8, 0)
        for i in self.offsets:
            self.output.write(struct.pack('<I', i))

infile = input("File (leave blank for Nijyuei.kpd): ") or "Nijyuei.kpd"
mode = int(input("Mode (0 - export, 1 - import): "))

kpd = KagePhraseData(infile, mode)
if (mode == 0):
    kpd.read_commands()
    kpd.script_decompile()
else:
    kpd.script_compile()