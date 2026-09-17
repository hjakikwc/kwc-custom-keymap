# KWC Custom Keymap (C)2024 Hayano
# 
# ##### BEGIN GPL LICENSE BLOCK #####
# 
# This program is free software: 
# you can redistribute it and/or modify it under the terms of 
# the GNU General Public License as published by the Free Software Foundation, 
# either version 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with this program. 
# If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENCE BLOCK #####

bl_info = {
	"name": "KWC Custom Keymap",
	"author": "hjaki",
	"version" : (1, 0, 8),
	"blender" : (3, 6, 8),
	"description": "Custom key maps",
	"warning": "",
	"category": "UI",
}

#公開用のinfo。↑のinfoは消す
# 
# bl_info = {
# 	"name": "KWC Custom Keymap",
# 	"author": "Hayano",
# 	"version" : (1, 0, 1),
# 	"blender" : (3, 6, 8),
# 	"description": "Custom key maps",
# 	"warning": "",
# 	"category": "UI",
# }
# 
# 公開用のinfoここまで


import bpy
from bpy.props import *
from bpy.types import AddonPreferences
import rna_keymap_ui

class KWC_KEYMAP_AddonPreferences(AddonPreferences):
	bl_idname = __name__

	tab_addon_menu : EnumProperty(name="tab", description="", items=[('KEYMAP',"Keymap","","EVENT_A",0),('LINK', "Link", "","URL",1)],default='KEYMAP')

	def draw(self, context):
		layout = self.layout
		
		row = layout.row(align=True)
		row.prop(self, "tab_addon_menu",expand=True)


		if self.tab_addon_menu=="KEYMAP":
			box = layout.box()
			col = box.column()
			col.label(text="Keymap List:")

			wm = bpy.context.window_manager
			kc = wm.keyconfigs.user
			old_km_name = ""
			old_id_l = []

			for km_add, kmi_add in addon_keymaps:
				for km_con in kc.keymaps:
					if km_add.name == km_con.name:
						km = km_con
						break

				for kmi_con in km.keymap_items:
					if kmi_add.idname == kmi_con.idname:

						if not kmi_con.id in old_id_l:
							kmi = kmi_con
							old_id_l.append(kmi_con.id)
							break

				try:
					if not km.name == old_km_name:
						col.label(text=str(km.name),icon="DOT")
					col.context_pointer_set("keymap", km)
					rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
					col.separator()
					old_km_name = km.name
				except: pass


		if self.tab_addon_menu=="LINK":
			row = layout.row()
			row.label(text="Link:")
			row.operator( "wm.url_open", text="Booth").url = "https://kwc.booth.pm/items/5506923"

classes = (KWC_KEYMAP_AddonPreferences,)	

addon_keymaps = []
def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon

	#3D View
	km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
	if kc:

		#ビューを回転
		kmi = km.keymap_items.new("view3d.rotate",type= 'LEFTMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#視点の移動
		kmi = km.keymap_items.new("view3d.move",type= 'MIDDLEMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#ビューをズーム
		kmi = km.keymap_items.new("view3d.zoom",type= 'RIGHTMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#移動モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'W',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.move"

		#回転モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'E',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.rotate"

		#スケールモード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'R',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.scale"

		#ボックス選択モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'B',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.select_box"

		#サークル選択モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'C',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.select_circle"

		#頂点モード
		kmi = km.keymap_items.new("object.mode_set_with_submode",type= 'ONE',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.mode = 'EDIT'
		kmi.properties.mesh_select_mode = {'VERT'}

		#辺モード
		kmi = km.keymap_items.new("object.mode_set_with_submode",type= 'TWO',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.mode = 'EDIT'
		kmi.properties.mesh_select_mode = {'EDGE'}

		#面モード
		kmi = km.keymap_items.new("object.mode_set_with_submode",type= 'THREE',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.mode = 'EDIT'
		kmi.properties.mesh_select_mode = {'FACE'}

		#ポーズモード
		kmi = km.keymap_items.new("object.mode_set_with_submode",type= 'THREE',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.mode = 'POSE'
		kmi.properties.mesh_select_mode = {'VERT'}

		#オブジェクトモード
		kmi = km.keymap_items.new("object.mode_set_with_submode",type= 'FOUR',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.mode = 'OBJECT'

		#オブジェクトモード
		km = wm.keyconfigs.addon.keymaps.new('Pose')
		kmi = km.keymap_items.new("object.mode_set_with_submode",type= 'TAB',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.mode = 'OBJECT'


	#2D View
	km = kc.keymaps.new(name="View2D", space_type="EMPTY")
	if kc:
	
		#視点の移動
		kmi = km.keymap_items.new("view2d.pan",type= 'LEFTMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#視点の移動
		kmi = km.keymap_items.new("view2d.pan",type= 'MIDDLEMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#2Dビューズーム
		kmi = km.keymap_items.new("view2d.zoom",type= 'RIGHTMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

	#2D View Button List 
	km = kc.keymaps.new(name="View2D Buttons List", space_type="EMPTY")
	if kc:
		#視点の移動
		kmi = km.keymap_items.new("view2d.pan",type= 'LEFTMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#視点の移動
		kmi = km.keymap_items.new("view2d.pan",type= 'MIDDLEMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#2Dビューズーム
		kmi = km.keymap_items.new("view2d.zoom",type= 'RIGHTMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

	#Image
	km = kc.keymaps.new(name="Image", space_type="IMAGE_EDITOR")
	if kc:
		#視点の移動
		kmi = km.keymap_items.new("image.view_pan",type= 'LEFTMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#視点の移動
		kmi = km.keymap_items.new("image.view_pan",type= 'MIDDLEMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#2Dビューズーム
		kmi = km.keymap_items.new("image.view_zoom",type= 'RIGHTMOUSE',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#移動モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'W',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.move"

		#回転モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'E',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.rotate"

		#スケールモード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'R',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.scale"

		#ボックス選択モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'B',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.select_box"

		#サークル選択モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'C',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.select_circle"
	
	#UV
	km = kc.keymaps.new(name="UV Editor", space_type="EMPTY")
	if kc:
		#移動モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'W',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.move"

		#回転モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'E',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.rotate"

		#スケールモード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'R',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.scale"

		#ボックス選択モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'B',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.select_box"

		#サークル選択モード
		kmi = km.keymap_items.new("wm.tool_set_by_id",type= 'C',value="PRESS")
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "builtin.select_circle"

		#ループ選択
		kmi = km.keymap_items.new("uv.select_loop",type= 'LEFTMOUSE',value="DOUBLE_CLICK")
		addon_keymaps.append((km, kmi))

		#ループ選択
		kmi = km.keymap_items.new("uv.select_loop",type= 'LEFTMOUSE',value="DOUBLE_CLICK",shift=True)
		addon_keymaps.append((km, kmi))
		kmi.properties.extend = True

		#エッジリング選択
		kmi = km.keymap_items.new("uv.select_edge_ring",type= 'LEFTMOUSE',value="DOUBLE_CLICK",ctrl=True)
		addon_keymaps.append((km, kmi))

		#エッジリング選択（追加）
		kmi = km.keymap_items.new("uv.select_edge_ring",type= 'LEFTMOUSE',value="DOUBLE_CLICK",ctrl=True,shift=True)
		addon_keymaps.append((km, kmi))
		kmi.properties.extend = True


	#Mesh
	km = kc.keymaps.new(name="Mesh", space_type="EMPTY")
	if kc:
		#ループ選択
		kmi = km.keymap_items.new("mesh.loop_select",type= 'LEFTMOUSE',value="DOUBLE_CLICK")
		addon_keymaps.append((km, kmi))

		#ループ選択（追加）
		kmi = km.keymap_items.new("mesh.loop_select",type= 'LEFTMOUSE',value="DOUBLE_CLICK",shift=True)
		addon_keymaps.append((km, kmi))
		kmi.properties.extend = True

		#ループ選択（解除）
		kmi = km.keymap_items.new("mesh.loop_select",type= 'LEFTMOUSE',value="DOUBLE_CLICK",shift=True,alt=True)
		addon_keymaps.append((km, kmi))
		kmi.properties.deselect = True
		
		#エッジリング選択
		kmi = km.keymap_items.new("mesh.edgering_select",type= 'LEFTMOUSE',value="DOUBLE_CLICK",ctrl=True)
		addon_keymaps.append((km, kmi))

		#エッジリング選択（追加）
		kmi = km.keymap_items.new("mesh.edgering_select",type= 'LEFTMOUSE',value="DOUBLE_CLICK",ctrl=True,shift=True)
		addon_keymaps.append((km, kmi))
		kmi.properties.extend = True

		#エッジリング選択（解除）
		kmi = km.keymap_items.new("mesh.edgering_select",type= 'LEFTMOUSE',value="DOUBLE_CLICK",ctrl=True,shift=True,alt=True)
		addon_keymaps.append((km, kmi))
		kmi.properties.deselect = True

		#細分化
		kmi = km.keymap_items.new("mesh.subdivide",type='D',value="PRESS",ctrl=True)
		addon_keymaps.append((km, kmi))


#公開時ここから下を削除
		#Merge Tool(アドオン：Merge Tool)
		kmi = km.keymap_items.new("wm.tool_set_by_id",type='W',value="PRESS",ctrl=True)
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "edit_mesh.merge_tool"

		#Super Smart Create(アドオン：Maxivz Tools)
		kmi = km.keymap_items.new("mesh.super_smart_create",type='C',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))

		#Edge Weight(アドオン：rmkit)
		kmi = km.keymap_items.new("wm.call_menu_pie",type='E',value="PRESS",shift=True)
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "VIEW3D_MT_PIE_setedgeweight_crease"

		#Move To Furthest(アドオン：rmkit)
		kmi = km.keymap_items.new("wm.call_menu_pie",type='A',value="PRESS",alt=True)
		addon_keymaps.append((km, kmi))
		kmi.properties.name = "VIEW3D_MT_PIE_movetofurthest"

	#Transform Modal Map
	# km = kc.keymaps.new(name="Transform Modal Map", space_type="EMPTY")
	# if kc:
		
		#モーダルマップじゃないと言われて適用できない

		# #プロポーショナルの影響を増加
		# kmi = km.keymap_items.new_modal(propvalue='PROPORTIONAL_SIZE_UP',type='RIGHT_BRACKET',value="PRESS",repeat=True)
		# addon_keymaps.append((km, kmi))

		# #プロポーショナルの影響を減少
		# kmi = km.keymap_items.new_modal(propvalue='Decrease Proportional influence',type='LEFT_BRACKET',value="PRESS",repeat=True)
		# addon_keymaps.append((km, kmi))

#公開時削除ここまで

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

	try:
		bpy.app.translations.unregister(__name__)
	except: pass

	for (km, kmi) in addon_keymaps:
		km.keymap_items.remove(kmi)
	addon_keymaps.clear()
	

if __name__ == '__main__':
	register()
