#coding=shift-jis
import os
import re

# the last remnant of the first voice patch attempt
# put .bin files from the dc version into the BIN folder and run get_voices
# extracts voice number (index in afs file) and corresponding line

# match_voices is for adding the above to decompiled pc files
# ksd_tool 0 -> match_voices -> ksd_tool 2

def get_voices():
    voiceRE = re.compile(b'\xC9(?P<voice>.{2}\x00\x00)(.{,9}?)\xCD(?P<next>.{2})', flags=re.DOTALL)
    dialogueRE = re.compile(b'(\x81\x75)(?P<dialogue>.*)(\x81\x76)', flags=re.DOTALL)
    inPath = os.path.join(os.getcwd(), "Dreamcast/BIN")
    outPath = os.path.join(os.getcwd(), "Dreamcast")

    for file in os.listdir(outPath):
        os.remove(os.path.join(outPath, file))
        
    for file in os.listdir(inPath):
        if file.endswith(".BIN"):
            with (
            open(os.path.join(inPath, file), "rb") as tak,
            open(os.path.join(outPath, file[4:7] + ".txt"), "a", encoding="shift_jis") as output
            ):

                for i in re.finditer(voiceRE, tak.read()):
                    voNum = int.from_bytes(i.group('voice'), "little")   
                    length = int.from_bytes(i.group('next'), "little") - tak.seek(i.end())  
                    try:
                        line = tak.read(length)
                        #comment out the next line to get the nametag
                        #line = re.search(dialogueRE, line).group(0)
                        line = line.replace(b'\x81\x63\x81\x63', b'\x81\x45\x81\x45\x81\x45')
                        line = line.replace(b'#43', b'<0,')
                        line = line.replace(b'#53', b'>')
                        line = line.decode("shift_jis")  
                        output.write(str(voNum).zfill(4) + '\n')
                        output.write(line + '\n')  
                    except ValueError:
                        pass                   

                    
    for file in os.listdir(outPath):
        if file.startswith("000") or file.startswith("1"):
            os.remove(os.path.join(outPath, file))                

def match_voices():
    #dont_voice = ["name_set 双厳", "name_set 船頭", "name_set 十兵衛"]

    for file in os.listdir("Dreamcast"):
        if file.endswith(".txt"):
            vo_dict = {}
            with open(os.path.join("Dreamcast", file), "r", encoding="shift-jis") as voices:
                for i, line in enumerate(voices.readlines()):
                    if i % 2 == 0:
                        v = line.rstrip('\n').zfill(4)
                    else:
                        d = line.rstrip('\n').split()
                    if i > 0:
                        vo_dict[v] = d	# odd-numbered lines have voices, even-numbered lines have dialogue
            fName = file.strip(".txt") + ".ksd.txt"

            with (
                open(os.path.join("Ksd/Decompiled", fName), "r", encoding="shift-jis") as ksd,
                open(os.path.join("Ksd/Voiced", fName), "a", encoding="shift-jis") as output,
            ):
                txt_lines = ksd.read().split('\n')
                txt_lines = [line for line in txt_lines if line]
                name_tag = ''
                

                for index, line in enumerate(txt_lines):
                    if "name_set" in line: #and line not in dont_voice:
                        name_tag = line.split(' ')[-1]
                    for v, d in vo_dict.items():
                        try:
                            matches = d[1] in line and d[0] == name_tag
                        except IndexError:
                            matches = d[-1] in line
                        finally:
                            if matches:
                                ins = "sfx_set 2 " + "Vox\\" + v + ".wav"
                                output.write(ins + "\nsfx_play 2\n")
                                del vo_dict[v]
                                break                   
                    
                    output.write(line + '\n')
                    if d[-1] in line:
                        output.write("sfx_stop 2\n")  
                        
                    if line[:4] != txt_lines[index-1][:4]:
                        output.write('\n')                                   

                if len(vo_dict) > 0:
                    with (open(os.path.join("Ksd/Voiced/Rejects", fName), "w", encoding="shift-jis") as to_fix):            
                        for v, d in vo_dict.items():
                            to_fix.write(v + '\n' + '\t\t'.join(d) + '\n')    
match_voices()                        