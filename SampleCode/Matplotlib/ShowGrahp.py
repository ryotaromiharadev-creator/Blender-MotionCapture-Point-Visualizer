import sys
#仮想環境のパス 自分のものに書き換えてください
evnPath = r"C:\Users\mihar\Documents\BlenderAddon\.venv\Lib\site-packages"
sys.path.append(evnPath)

import bpy
import os

import matplotlib.pyplot as plt

dt = 1/240

obj = bpy.context.active_object

if obj.animation_data and obj.animation_data.action:
    action = obj.animation_data.action
    keyframes = sorted({int(kp.co.x) for fcurve in action.fcurves for kp in fcurve.keyframe_points})


    data = []
    for frame in keyframes:
        bpy.context.scene.frame_set(frame)
        loc = obj.location
        data.append(loc.z)
        #print(f"フレーム {frame}: 位置 = ({loc.x:.3f}, {loc.y:.3f}, {loc.z:.3f})")
        

#ShowGrahp
plt.plot(np.arange(0, float(len(keyframes)*dt), dt),data)
plt.xlabel("time t [s]")
plt.ylabel("velocity v [m/s]")
plt.title("PointMove")
#画像の保存先 自分のものに書き換えてください
plt.savefig(r"C:\Users\mihar\Downloads\Grahp")
plt.close()


#Blender内で使用されているすべての画像を再読み込み
for img in bpy.data.images:
    if img.source == 'FILE':  #外部ファイルから読み込まれているものだけ
        img.reload()