import subprocess

import src.app_info

app_ver = src.app_info.APP_VERSION.split(".")
filevers = (int(app_ver[0]), int(app_ver[1]), 0, 0)

win_verinfo = f"""VSVersionInfo(ffi=FixedFileInfo(filevers={filevers},prodvers={filevers},mask=0x3f,flags=0x0,OS=0x4,fileType=0x1,subtype=0x0,date=(0,0)),kids=[StringFileInfo([StringTable('040904b0',[StringStruct('FileVersion','{src.app_info.APP_VERSION}'),StringStruct('ProductVersion','{src.app_info.APP_VERSION}'),StringStruct('ProductName','{src.app_info.APP_NAME}')])])])"""

with open("file_version_info.txt", "w") as f:
    f.write(win_verinfo)

with open("Info.plist.template", "r") as f:
    plist_content = f.read()

plist_content = plist_content.replace("{{APP_VERSION}}", src.app_info.APP_VERSION)
plist_content = plist_content.replace("{{APP_COPYRIGHT}}", src.app_info.APP_COPYRIGHT)
plist_content = plist_content.replace("{{APP_NAME}}", src.app_info.APP_NAME)

with open("Info.plist", "w") as f:
    f.write(plist_content)

subprocess.run(["pyinstaller", "main.spec"])
