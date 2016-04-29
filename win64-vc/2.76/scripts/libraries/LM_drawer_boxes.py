"""
Microvellum 
Drawer Boxes
Stores the logic and insert defs for all exterior components for cabinets and closets.
Doors, Drawers, Hampers
"""

import bpy
import fd

HIDDEN_FOLDER_NAME = "_HIDDEN"
PART_WITH_NO_EDGEBANDING = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Cut Parts","Part with No Edgebanding")
PART_WITH_FRONT_EDGEBANDING = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Cut Parts","Part with Front Edgebanding")
DRAWER_BOX = (HIDDEN_FOLDER_NAME,"Cabinet Assemblies","Drawer Boxes","Wood Drawer Box")

DRAWER_BOX_MATERIAL = ("Plastics","White Melamine")

#---------SPEC GROUP POINTERS

class Material_Pointers():
    
    Drawer_Box_Surface = fd.Material_Pointer(DRAWER_BOX_MATERIAL)

class Cutpart_Pointers():
    
    Drawer_Box_Parts = fd.Cutpart_Pointer(thickness=fd.inches(.5),
                                          core="Concealed_Surface",
                                          top="Drawer_Box_Surface",
                                          bottom="Drawer_Box_Surface")
    
    Drawer_Box_Bottom = fd.Cutpart_Pointer(thickness=fd.inches(.25),
                                           core="Concealed_Surface",
                                           top="Drawer_Box_Surface",
                                           bottom="Drawer_Box_Surface")

class Wood_Drawer_Box(fd.Library_Assembly):
    
    type_assembly = "NONE"
    mirror_y = False
    
    def draw(self):
        self.create_assembly()
        
        self.add_tab(name='Drawer Box Options',tab_type='VISIBLE')
        self.add_prompt(name="Hide",prompt_type='CHECKBOX',value=False,tab_index=0)
        self.add_prompt(name="Drawer Side Thickness",prompt_type='DISTANCE',value=fd.inches(.5),tab_index=0)
        self.add_prompt(name="Front Back Thickness",prompt_type='DISTANCE',value=fd.inches(.5),tab_index=0)
        self.add_prompt(name="Drawer Bottom Thickness",prompt_type='DISTANCE',value=fd.inches(.25),tab_index=0)
        self.add_prompt(name="Bottom Dado Depth",prompt_type='DISTANCE',value=fd.inches(.25),tab_index=0)
        self.add_prompt(name="Bottom Z Location",prompt_type='DISTANCE',value=fd.inches(.5),tab_index=0)
        self.add_prompt(name="Drawer Slide Quantity",prompt_type='QUANTITY',value=1,tab_index=0)
        
        Drawer_Width = self.get_var('dim_x','Drawer_Width')
        Drawer_Depth = self.get_var('dim_y','Drawer_Depth')
        Drawer_Height = self.get_var('dim_z','Drawer_Height')
        Drawer_Side_Thickness = self.get_var('Drawer Side Thickness')
        Front_Back_Thickness = self.get_var('Front Back Thickness')
        Drawer_Bottom_Thickness = self.get_var('Drawer Bottom Thickness')
        Bottom_Dado_Depth = self.get_var('Bottom Dado Depth')
        Bottom_Z_Location = self.get_var('Bottom Z Location')
        Hide = self.get_var('Hide')
        
        left_side = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        left_side.set_name("Left Drawer Side")
        left_side.x_loc(value = 0)
        left_side.y_loc(value = 0)
        left_side.z_loc(value = 0)
        left_side.x_rot(value = 90)
        left_side.y_rot(value = 0)
        left_side.z_rot(value = 90)
        left_side.x_dim('Drawer_Depth',[Drawer_Depth])
        left_side.y_dim('Drawer_Height',[Drawer_Height])
        left_side.z_dim('Drawer_Side_Thickness',[Drawer_Side_Thickness])
        left_side.cutpart("CBD_Drawer_Part")
        left_side.edgebanding('Drawer_Box_Parts',l1 = True)
        left_side.prompt('Hide','Hide',[Hide])

        right_side = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        right_side.set_name("Right Drawer Side")
        right_side.x_loc('Drawer_Width',[Drawer_Width])
        right_side.y_loc(value = 0)
        right_side.z_loc(value = 0)
        right_side.x_rot(value = 90)
        right_side.y_rot(value = 0)
        right_side.z_rot(value = 90)
        right_side.x_dim('Drawer_Depth',[Drawer_Depth])
        right_side.y_dim('Drawer_Height',[Drawer_Height])
        right_side.z_dim('-Drawer_Side_Thickness',[Drawer_Side_Thickness])
        right_side.cutpart("CBD_Drawer_Part")
        right_side.edgebanding('Drawer_Box_Parts',l1 = True)
        right_side.prompt('Hide','Hide',[Hide])

        front = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        front.set_name("Sub Front")
        front.x_loc('Drawer_Side_Thickness',[Drawer_Side_Thickness])
        front.y_loc(value = 0)
        front.z_loc(value = 0)
        front.x_rot(value = 90)
        front.y_rot(value = 0)
        front.z_rot(value = 0)
        front.x_dim('Drawer_Width-(Drawer_Side_Thickness*2)',[Drawer_Width,Drawer_Side_Thickness])
        front.y_dim('Drawer_Height',[Drawer_Height])
        front.z_dim('-Front_Back_Thickness',[Front_Back_Thickness])
        front.cutpart("CBD_Drawer_Part")
        front.edgebanding('Drawer_Box_Parts',l1 = True)
        front.prompt('Hide','Hide',[Hide])

        back = self.add_assembly(PART_WITH_FRONT_EDGEBANDING)
        back.set_name("Drawer Back")
        back.x_loc('Drawer_Side_Thickness',[Drawer_Side_Thickness])
        back.y_loc('Drawer_Depth',[Drawer_Depth])
        back.z_loc(value = 0)
        back.x_rot(value = 90)
        back.y_rot(value = 0)
        back.z_rot(value = 0)
        back.x_dim('Drawer_Width-(Drawer_Side_Thickness*2)',[Drawer_Width,Drawer_Side_Thickness])
        back.y_dim('Drawer_Height',[Drawer_Height])
        back.z_dim('Front_Back_Thickness',[Front_Back_Thickness])
        back.cutpart("CBD_Drawer_Part")
        back.edgebanding('Drawer_Box_Bottom',l1 = True)
        back.prompt('Hide','Hide',[Hide])

        bottom = self.add_assembly(PART_WITH_NO_EDGEBANDING)
        bottom.set_name("Drawer Back")
        bottom.x_loc('Drawer_Width-Drawer_Side_Thickness+Bottom_Dado_Depth',[Drawer_Width,Drawer_Side_Thickness,Bottom_Dado_Depth])
        bottom.y_loc('Front_Back_Thickness-Bottom_Dado_Depth',[Front_Back_Thickness,Bottom_Dado_Depth])
        bottom.z_loc('Bottom_Z_Location',[Bottom_Z_Location])
        bottom.x_rot(value = 0)
        bottom.y_rot(value = 0)
        bottom.z_rot(value = 90)
        bottom.x_dim('Drawer_Depth-(Drawer_Side_Thickness*2)+(Bottom_Dado_Depth*2)',[Drawer_Depth,Drawer_Side_Thickness,Bottom_Dado_Depth])
        bottom.y_dim('Drawer_Width-(Front_Back_Thickness*2)+(Bottom_Dado_Depth*2)',[Drawer_Width,Front_Back_Thickness,Bottom_Dado_Depth])
        bottom.z_dim('Drawer_Bottom_Thickness',[Drawer_Bottom_Thickness])
        bottom.cutpart("Drawer_Box_Parts")
        bottom.prompt('Hide','Hide',[Hide])

        self.update()
    