bl_info = {
    "name": "CSV To Animation",
    "author": "Mihara",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "Add > Mesh",
    "description": "CSVデータをモーションキャプチャーで表示します",
    "category": "Generater",
}

import sys
import os
sys.path.append(os.path.dirname(__file__))

import bpy
import process_csv
import re

def GenerateMotionPoint(path):
    label,datas = process_csv.read_motion_csv_in_groups(path)

    #将来的にパラメータとして出したい
    scale = 1
    skip = 1

    #CSVを基にアニメーションをつける
    #オブジェクト群をコレクションにまとめる
    new_collection = bpy.data.collections.new("DataPoint")

    for i,data in enumerate(datas):
        #アニメーションをつけるオブジェクト
        bpy.ops.mesh.primitive_uv_sphere_add(radius=25)
        obj = bpy.context.active_object
        #AddCollection
        new_collection.objects.link(obj)
        #ReName
        name = label[i*3]
        name =  re.sub(r"^.*:(.*)_X$", r"\1", name)
        obj.name = name
        
        for j,OneData in enumerate(data):
            x = OneData[0] / scale
            y = OneData[1] / scale
            z = OneData[2] / scale
            obj.location = (x, y, z)
            obj.keyframe_insert(data_path="location", frame=int(j/skip))


# 実際に行いたい処理
def process_file(filepath):
    GenerateMotionPoint(filepath)


# ファイル選択オペレーター
class OBJECT_OT_select_file(bpy.types.Operator):
    bl_idname = "object.select_file"
    bl_label = "MotionData.csvをアニメーションに書き出す"
    bl_description = "モーションキャプチャデータを点群で表示します"

    # File Selector用のプロパティ
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    # ファイル選択ダイアログを開く
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    # 「OK」が押された後に実行される
    def execute(self, context):
        process_file(self.filepath)
        return {'FINISHED'}


# 「ファイル -> インポート」メニューにボタンを追加
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_select_file.bl_idname, icon='FILE_FOLDER')


def register():
    bpy.utils.register_class(OBJECT_OT_select_file)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_select_file)


if __name__ == "__main__":
    register()
