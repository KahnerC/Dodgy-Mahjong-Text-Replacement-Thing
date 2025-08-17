import os
import shutil

def derive_required_glyphs(all_lines="filename.txt"):
    with open(all_lines,"r", encoding="utf-8") as f:
        sampletext = f.readlines()

    charnumber = 0
    glyphset = ["Â¶"]

    #raw_text = []

    for t_line_whole in sampletext:
        for t_line in t_line_whole.split("¶"):#Â¶
            t_line_s = t_line.strip()
            #raw_text.append(t_line_s)
            #thisone = False
            #if t_line_s == "SP gauge SP gauge MAX":
            #    print(t_line_s)
            #    thisone = True
            for t_char in (t_line_s+"  "):
                if not charnumber%2:
                    new_glyph = (" "+t_line_s+"  ")[charnumber-1:charnumber+1]
                    #if thisone:
                    #    print(new_glyph)
                    if new_glyph not in glyphset and t_char != "\n" and len(new_glyph) > 1:
                        glyphset.append(new_glyph)
                        #print(new_glyph)
                charnumber += 1
            charnumber = 0
        #print(t_line)
    #print(len(glyphset))
    #print(glyphset)
    #print(raw_text)
    return glyphset

def map_glyphs(font_dump="filename.txt", glyphset=[]):
    with open(font_dump,"r", encoding="utf-8") as f:
        c_info = f.readlines()

    glyphmap = {"Â¶":"¶"}

    count = 209
    for glyph in glyphset:
        #print(str(count) + " - " + c_info[count][0])
        glyphmap[glyph] = c_info[count][0]
        #glyphmap[c_info[count][0]] = glyph
        count += 1
    return glyphmap

def generate_glyph_images(glyphset=[], folder_out="glyphdump/glyph",font_no=2):
    import pygame
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    pygame.init()
    pygame.font.init()
    if font_no == 1:
        size = (12, 12)
    else:
        size = (18, 18)
    font = pygame.font.SysFont("Comic Sans MS", 70)
    screen = pygame.display.set_mode(size)

    count = 208

    for glyph in glyphset:
        text_surface = font.render(glyph, True, WHITE)
        ts_18 = pygame.transform.scale(text_surface, size)
        screen.blit(ts_18, ((size[0]-ts_18.get_width())/2,0))
        #pygame.display.flip()
        pygame.image.save(screen, folder_out+("0000"+str(count))[-4:]+".png")
        screen.fill(BLACK)
        count += 1
    pygame.quit()

def encode_line(input_line="", glyphmap={}):
    output_line = ""
    line_chunks = 0
    for input_line_part in input_line.split("Â¶"):#¶Â
        input_line_part_s = input_line_part.strip()
        if line_chunks > 0:
            output_line += "¶"
            #print(input_line)
            #print(input_line_part_s)
        encode_index = 0
        #print(input_line_part_s)
        while encode_index < len(input_line_part_s):
            #print(glyphmap.keys())
            #print((" "+str(input_line_part_s)+"  ")[encode_index:encode_index+3][-2:])
            output_line += glyphmap[(" "+str(input_line_part_s)+"  ")[encode_index:encode_index+3][-2:]]
            encode_index += 2
        line_chunks += 1
    return output_line

def slot_encoded_text(source_file="whatever.hsd", replacement_text="whatever_eng.txt", file_out="fileout.hsd", glyphmap={}):
    with open(source_file,"r", encoding="utf-16-be") as f:
        origin_file = f.readlines()
    with open(replacement_text,"r", encoding="utf-8") as f:
        translated_text = f.readlines()
    with open(file_out,"w", encoding="utf-16-be") as f:
        count = 0
        for line in origin_file:
            line_split = line.split(",",14)
            line_out = ""
            for i in range(13):
                line_out += line_split[i]+","           
            line_out += encode_line(translated_text[count], glyphmap)+"\n"
            f.write(line_out)
            count += 1

def decode_line(input_line="", glyphmap={}):#Got busted up by fixing an off-by-one error. Means the glyphmaps aren't correct, but they work somehow...
    inverted_glyphmap = {}
    for key, value in glyphmap.items():
        inverted_glyphmap[value] = key
    output_line = ""
    for char in input_line:
        output_line += inverted_glyphmap[char]
    return output_line

def unpack_scenario_file(input_file="whatever.hsd"):
    output_text = "MARK"+input_file.split("/")[-1][8:-4]+"\n"
    with open(input_file,"r", encoding="utf-16-be") as f:
        raw_script = f.readlines()
    for line in raw_script:
        output_text += line.split(",",14)[-1]
    return output_text

def unpack_mail_file(input_file="whatever.hsd"):
    output_text = "MARK"+input_file.split("MailDef")[-1][:2]+"\n"
    with open(input_file,"r", encoding="utf-16-be") as f:
        raw_script = f.readlines()
    for line in raw_script:
        output_text += line.split(",",2)[-1]
    return output_text

def unpack_misc_file(input_file="whatever.hsd"):
    output_text = "MARK"+input_file.split("Coll")[-1][1]+"\n"
    with open(input_file,"r", encoding="utf-16-be") as f:
        raw_script = f.readlines()
    for line in raw_script:
        output_text += line.split(",",4)[-1]
    return output_text

def dump_all_text(output_file="full_dump.txt"):
    with open(output_file,"w", encoding="utf-16-be") as file_out:

        for file in os.listdir("input files/vnscripts"):
            if file[-4:] == ".hsd":
                file_out.write(unpack_scenario_file("vnscripts/"+file))

        for file in os.listdir("input files/mail"):
            if file[-4:] == ".hsd":
                file_out.write(unpack_mail_file("mail/"+file))

        for file in os.listdir("input files/misc"):
            if file[-4:] == ".hsd":
                file_out.write(unpack_misc_file("misc/"+file))

def splay_input_files(output_location="output files/"):
    for file in os.listdir("input files/vnscripts"):
        if file[-4:] == ".hsd":
            shutil.copyfile("input files/vnscripts/"+file,output_location+file)

    for file in os.listdir("input files/mail"):
        if file[-4:] == ".hsd":
            shutil.copyfile("input files/mail/"+file,output_location+file)

    for file in os.listdir("input files/misc"):
        if file[-4:] == ".hsd":
            shutil.copyfile("input files/misc/"+file,output_location+file)

def interpret_mark(markline="01_01_01", folder_out="copyfiles/"):
    #print(markline)
    if markline == "C":
        file_out = "CollScenarioName.hsd"
        filetype = "misc"
    if markline == "V":
        file_out = "CollVoiceList.hsd"
        filetype = "misc"
    if len(markline) == 2:
        mail_names = ["none","haruhi","kyon","yuki","mikuru","koizumi","turuya","arakawa","mori","imouto","acyakura","taniguti","comp","kunikida","syousitu"]
        file_out = "MailDef"+markline+mail_names[int(markline)]+".hsd"
        filetype = "mail"
    if len(markline) == 3:
        file_out = "Prologue"+markline+".hsd"
        filetype = "vnscript"
    if len(markline) > 3:
        file_out = "Scenario" + markline + ".hsd"
        filetype = "vnscript"
    return [folder_out+file_out, filetype]

def replace_line_text(glyphmap,line_raw="x,y,jptexthere",line_en="entexthere",filetype="vnscript"):
    #print("lost?")
    #print(glyphmap)
    if filetype == "vnscript":
        chunks = 14
    elif filetype == "mail":
        chunks = 2
    else:
        chunks = 4
    output_chunks = line_raw.split(",",chunks)[:-1]
    output_line = ""
    for chunk in output_chunks:
        output_line += chunk+","
    #print("what's happening here?")
    #print(line_raw)
    #print(line_en)
    output_line += encode_line(line_en, glyphmap)
    return output_line
    
def apply_translated_text(output_location="output files/",tl_input="whatever.txt",glm={}):
    line_count = 0
    with open(tl_input,"r") as f_in:
        tl_text_raw = f_in.readlines()
    for line in tl_text_raw:
        line_s = line.strip()
        #print(line_s)
        if line_s[:4] == "MARK":
            file_out_info = interpret_mark(line_s[4:], output_location)
            #print(line_s + " - " + file_out_info[0])
            with open(file_out_info[0],"r",encoding="utf-16-be") as f_existing:
                ex_text = f_existing.readlines()
                #print(len(ex_text))
                #print(line_s)
            if line_count > 2:
                f_out.close()
            f_out = open(file_out_info[0],"w",encoding="utf-16-be")
            #print(file_out_info[0])
            line_count = 0
        else:
            #print(glm.keys())
            f_out.write(replace_line_text(glm,ex_text[line_count],line_s,file_out_info[1])+"\n")
            line_count += 1

gls = derive_required_glyphs("available_tl.txt")
print(len(gls))
glm = map_glyphs("font2config.txt", gls)
generate_glyph_images(gls, "glyphdump/font1/glyph",1)
generate_glyph_images(gls, "glyphdump/font2/glyph",2)

from hacktools import psp
psp.repackPGFData("FONT1.PGF","copyfiles/FONT1.PGF","font1configout.txt","glyphdump/font1/glyph")
psp.repackPGFData("FONT2.PGF","copyfiles/FONT2.PGF","font2configout.txt","glyphdump/font2/glyph")

splay_input_files("copyfiles/")
apply_translated_text("copyfiles/","available_tl.txt", glm)

