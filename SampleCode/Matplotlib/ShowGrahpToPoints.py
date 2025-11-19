import sys
evnPath = r"C:\Users\mihar\Documents\BlenderAddon\.venv\Lib\site-packages"
sys.path.append(evnPath)

import bpy
import os

import numpy as np
import matplotlib.pyplot as plt

dt = 1/240

#解析を行いたいオブジェクト
obj = bpy.context.active_object
obj2 = bpy.data.objects["RANK"]

#可視化するデータ
data = []
data2 = []

#解析したいフレーム範囲
scene = bpy.context.scene
start = scene.frame_start
end = scene.frame_end
len = end - start

#データの形成
for f in range(start, end):
    bpy.context.scene.frame_set(f)
    loc = obj.location
    loc2 = obj2.location
    data.append(loc.z)
    data2.append(loc2.z)
    #print(f"フレーム {frame}: 位置 = ({loc.x:.3f}, {loc.y:.3f}, {loc.z:.3f})")
        

#ShowGrahp
t = np.arange(0, float(len)*dt, dt)
plt.plot(t,data)
plt.plot(t,data2)
plt.xlabel("time t [s]")
plt.ylabel("velocity v [m/s]")
plt.title("PointMove")
plt.savefig(r"C:\Users\mihar\Downloads\Grahp")
plt.close()


#Blender内で使用されているすべての画像を再読み込み
for img in bpy.data.images:
    if img.source == 'FILE':  #外部ファイルから読み込まれているものだけ
        img.reload()