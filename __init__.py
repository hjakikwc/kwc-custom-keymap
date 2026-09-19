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

import bpy
from bpy.props import *
from bpy.types import AddonPreferences
import rna_keymap_ui


class KWC_KEYMAP_AddonPreferences(AddonPreferences):
	bl_idname = __package__

	tab_addon_menu : EnumProperty(name="tab", description="", items=[('KEYMAP',"Keymap","","EVENT_A",0),('LINK', "Link", "","URL",1)],default='KEYMAP')

	def draw(self, context):
		layout = self.layout

		row = layout.row(align=True)
		row.prop(self, "tab_addon_menu",expand=True)


		if self.tab_addon_menu=="KEYMAP":
			box = layout.box()
			col = box.column()
			col.label(text="Keymap List:")

			kc = context.window_manager.keyconfigs.user
			old_km_name = ""

			for km, kmi in addon_keymaps:
				km = km.active()
				if km.name != old_km_name:
					col.label(text=km.name, icon="DOT")
					old_km_name = km.name
				col.context_pointer_set("keymap", km)
				rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
				col.separator()


		if self.tab_addon_menu=="LINK":
			row = layout.row()
			row.label(text="Link:")
			row.operator( "wm.url_open", text="Booth").url = "https://kwc.booth.pm/"

classes = (KWC_KEYMAP_AddonPreferences,)

addon_keymaps = []
def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	kc = bpy.context.window_manager.keyconfigs.addon
	if not kc:
		return

	#3D View
	km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")

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

	#Object Mode
	km = kc.keymaps.new(name="Object Mode", space_type="EMPTY")
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
	kmi = km.keymap_items.new("object.mode_set",type= 'THREE',value="PRESS")
	addon_keymaps.append((km, kmi))
	kmi.properties.mode = 'POSE'

	#Pose
	km = kc.keymaps.new(name="Pose", space_type="EMPTY")
	#オブジェクトモード
	kmi = km.keymap_items.new("object.mode_set",type= 'TAB',value="PRESS")
	addon_keymaps.append((km, kmi))
	kmi.properties.mode = 'OBJECT'

	#オブジェクトモード
	kmi = km.keymap_items.new("object.mode_set",type= 'FOUR',value="PRESS")
	addon_keymaps.append((km, kmi))
	kmi.properties.mode = 'OBJECT'


	#2D View
	km = kc.keymaps.new(name="View2D", space_type="EMPTY")

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

	#オブジェクトモード
	kmi = km.keymap_items.new("object.mode_set",type= 'FOUR',value="PRESS")
	addon_keymaps.append((km, kmi))
	kmi.properties.mode = 'OBJECT'

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


def unregister():
	for km, kmi in addon_keymaps:
		try:
			km.keymap_items.remove(kmi)
		except RuntimeError:
			pass
	addon_keymaps.clear()

	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == '__main__':
	register()
