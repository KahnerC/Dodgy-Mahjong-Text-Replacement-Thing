with open("font2config.txt","r",encoding="utf-8") as f:
    fontconfig = f.readlines()
    fontconfig_out = ""
    for line in fontconfig:
        fontconfig_out += line.split("={")[0]+'={"width": 18, "height": 18, "left": 1, "top": 16, "dimension": {"x": 17.1875, "y": 16.59375}, "bearingx": {"x": 1.046875, "y": 0.0}, "bearingy": {"x": 15.25, "y": 0.0}, "advance": {"x": 18.0, "y": 0.0}}\n'

with open("font2configout.txt","w",encoding="utf-8") as f:
    f.write(fontconfig_out)
