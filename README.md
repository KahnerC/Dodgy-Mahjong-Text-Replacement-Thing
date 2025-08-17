# Dodgy-Mahjong-Text-Replacement-Thing
An imperfect text replacement for *The Mahjong of Haruhi-chan Suzumiya (涼宮ハルヒちゃんの雀麻 / Suzumiya Haruhi-chan no Mahjong)* on PSP

Haruhi Mahjong is a game  
You may play it on your Playstation Portable  
If you open it with 7-Zip, you will find large quantities of text hanging exposed  
You may replace it with your own text, but it will look silly  
The letters will be too wide  
And there will not be enough of them to say the things you want to say  
If you know the mind of the Playstation Portable,  
You may make the letters narrower  
If you do not know the mind of the Playstation Portable,  
There is this thing  
  
This thing looks at your translated script  
It breaks your letters into two-letter chunks  
And maps them to characters of the Japanese font  
So you get more letters per letter  
Great value  
  
It finds which chunks you need, and which chunks you do not  
Anne of Green Gables needs 1071 chunks  
Moby Dick needs 1757 chunks  
You have 2092 chunks available  
  
  
Relies on hacktools by Illidanz (https://github.com/Illidanz/hacktools) and Pygame  
Pygame might stop working in November, but you can find something to fill its part (it's used here to generate the many required 18x18 and (probably unnecessary 12x12) pictures of two-character chunks for the new font)  
You'll want to extract the font config data for FONT2.PGF (and maybe FONT1.PGF), and change all of the widths, heights and other values to something reasonable for a full-size square. A short script for that is included.  
  
Before running the thing, you will need:  
-A folder for the individual font images. "glyphdump/font2" by default here. You probably want to comment out the bit for Font 1 for now.  
-A font config file for Font 2, called "fontconfig2.txt" by default. Generated as described above, ideally with its dimensions standardised.  
-A folder containing all of the files with accessible text to be translated ("input files" by default, with three subfolders "mail", "misc" and "vnscripts", with .hsd files sorted within)  
-A folder to receive the output files ("copyfiles" by default)  
-One translated script (you can use the *dump_all_text* function to rip the Japanese text in a shape that the rest of the script can interpret)  
  
It should then generate a bunch of files in the "copyfiles" folder, which can be pasted in the relevant folder of the extracted iso. You can repack it if you want.  
  
Other notes:  
-Sprites mostly live in PICTURE.BIN. You can look around by swapping the pointer addresses at the start of the file around. The first row in your hex editor is loosely the title screen.  
-A sample machine-translated script is included. I accidentally translated some encoded dummy text instead of the source for the intro. I use "MARK" instead of a more intuitive name for the *dump_all_text* function to shore it up against getting lost in machine translation, so it starts off all very Lynchian. It covers the first ~50 pages of the story and everything else that's hanging exposed.  
-The main menu and nameplates looks to use sprites for theur text. The other menu text and in-mahjong talk isn't hanging exposed in the *.hsd* files, so this script will just mangle them.  
-Commas, paragraph marks and newlines all have meaning to the interpreter, so I started assigning characters at the start of the Japanese alphabet (~210 deep) in case there were others.  
-The line-by-line decoder function doesn't work, on account of fixing some off-by-one nonsense elsewhere.  
-Each VN script file has a matching *_sc.hsd* file, which I assume sets up some cues relating to the scene. The main files are mostly fancy *.csv*s, using the line-by-line format of:  
0,0,0,0,3,0,7,0,360,272,100,2,0,麻雀ブームが来るわっ！  
From twiddling, the rough meaning of these is:  
(ordering?),(sprite slot),(nameplate),(character sprite set),(specific character sprite),0,7,0,(x position),(y position),(sprite transparency),2,(voice line),(text)
