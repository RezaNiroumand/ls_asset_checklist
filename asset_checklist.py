from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from maya import OpenMayaUI as omu
from shiboken2 import wrapInstance
import maya.cmds as cmds
import os, sys
import maya.mel as mel
SCRIPT_FILE_PATH = 'D:/reza_niroumand/Script/asset_checklist_tool/'
mainObject = omu.MQtUtil.mainWindow()
mayaMainWind = wrapInstance(int(mainObject), QtWidgets.QWidget)
class AssetChecklist(QtWidgets.QWidget):    
    
    def __init__(self,parent=mayaMainWind):
        
        super(AssetChecklist, self).__init__(parent=parent)
                   
        if(__name__ == '__main__'):
            self.ui = SCRIPT_FILE_PATH+"ui/asset_checklist_tool.ui"
        else:
            self.ui = os.path.abspath(os.path.dirname(__file__)+'/ui/asset_checklist_tool.ui')
        
        self.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle('Asset Checklist')
        self.resize(700,300)                
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(self.ui)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.theMainWidget = loader.load(ui_file)
        ui_file.close()
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.theMainWidget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)


        self.theMainWidget.world_node_names_pushButton.clicked.connect(self.check_world_node_names)
               
        self.theMainWidget.subdivision_availability_pushButton.clicked.connect(self.check_set_exists)

        self.theMainWidget.hierarchy_structure_pushButton.clicked.connect(self.check_hierarchy_structure)

        self.theMainWidget.hierarchy_structure_fix_pushButton.setEnabled(False)
        self.theMainWidget.hierarchy_structure_fix_pushButton.clicked.connect(self.fix_hierarchy_structure)
      
        self.theMainWidget.visibility_off_groups_pushButton.clicked.connect(self.check_visibility_off_groups)
        
        self.theMainWidget.visibility_off_groups_fix_pushButton.setEnabled(False)
        self.theMainWidget.visibility_off_groups_fix_pushButton.clicked.connect(self.fix_visibility_off_groups)
                   
        self.theMainWidget.object_names_pushButton.clicked.connect(self.check_object_names)

        self.theMainWidget.non_deformer_history_pushButton.clicked.connect(self.check_non_deformer_history)

        self.theMainWidget.duplicate_names_pushButton.clicked.connect(self.check_duplicate_names)
        
        self.theMainWidget.ghost_nodes_pushButton.clicked.connect(self.check_ghost_nodes)
        
        self.theMainWidget.ghost_nodes_fix_pushButton.setEnabled(False)
        self.theMainWidget.ghost_nodes_fix_pushButton.clicked.connect(self.fix_ghost_nodes)

        
        self.theMainWidget.extra_camera_pushButton.clicked.connect(self.check_extra_cameras)
        
        self.theMainWidget.extra_camera_fix_pushButton.setEnabled(False)
        self.theMainWidget.extra_camera_fix_pushButton.clicked.connect(self.fix_extra_cameras)


        self.theMainWidget.transform_values_pushButton.clicked.connect(self.check_transform_values)

        self.theMainWidget.two_shape_pushButton.clicked.connect(self.check_two_shape)

        
        self.log_textEdit = self.findChild(QtWidgets.QTextEdit, 'log_textEdit')

        
    
    def log(self, message):
        self.log_textEdit.append(message)
    


    def check_set_exists(self):
        self.log_textEdit.clear()
        all_sets = cmds.ls(sets=True)
        if "SubdivisionSet" in all_sets:
            self.log('SubdivisionSet is there.')
        else:
            self.log("Can't find SubdivisionSet.")


    def check_world_node_names(self):
        self.log_textEdit.clear()
        # Get all group nodes in the scene
        root_nodes = cmds.ls(assemblies=True)
        group_nodes = [node for node in root_nodes if cmds.nodeType(node) == "transform"]
        world_groups = []

        # Check each group node if it starts with "World_"
        for node in group_nodes:
            if node.startswith("World_"):
                # If the node starts with "World_", add it to the list
                world_groups.append(node)

        # Check the number of found world groups
        if len(world_groups) > 1:
            # If more than one world group is found, list them
            self.log("Multiple world groups found:")
            for group in world_groups:
                self.log(group)
        elif len(world_groups) == 1:
            # If only one world group is found, check its name
            if world_groups[0] != "World_AssetName":
                if world_groups[0] in cmds.ls(assemblies=True):
                    self.log("Found one correct world group: "+ world_groups[0])
                else:
                    self.log("Found one world group " + world_groups[0] + " but it should be in root.")
            else:
                self.log("The only world group found is named 'World_AssetName'")
        else:
            # If no world group is found
            self.log("No world group found in the scene.")

    def check_hierarchy_structure(self):
        self.log_textEdit.clear()
        root_ref = ['persp', 'top', 'front', 'side']
        level_one_group_ref = ['Geometry', 'Texture', 'Controllers', 'Rigging', 'Lighting', 'FX', 'Misc']
        inside_Geometry_ref = ['HiRes', 'Proxy_Grp']
        inside_Rigging_ref = ['Deformers', 'Skeleton']
        inside_Texture_ref = ['Place3d', 'Texture_Ref']
        # Get all group nodes in the scene
        root_nodes = cmds.ls(assemblies=True)
        group_nodes = [node for node in root_nodes if cmds.nodeType(node) == "transform"]
        world_groups = []
        self.missing_groups = []
        # Check each group node if it starts with "World_"
        for node in group_nodes:
            if node.startswith("World_"):
                # If the node starts with "World_", add it to the list
                world_groups.append(node)
        if (len(world_groups) == 1) and (world_groups[0] != "World_AssetName") and (world_groups[0] in cmds.ls(assemblies=True)):
            hierarchy_error = 0
            missing_error = 0
            top_elements = cmds.ls(assemblies=True)
            extra_elements = set(top_elements) - set(root_ref)
            if(len(extra_elements)>1):
                hierarchy_error = 1
                self.log("These items are extra in outliner root :")
                for item in extra_elements:
                    if not item.startswith('World_'):
                        self.log(item) 


            children = cmds.listRelatives(world_groups[0], children=True)
            missing_elements = set(level_one_group_ref) - set(children)
            if missing_elements:
                hierarchy_error = 1
                missing_error = 1
                self.log("These items are missings in "+world_groups[0]+" :")
                for item in missing_elements:
                    self.missing_groups.append(world_groups[0]+'|'+item)
                    self.log(item)
            extra_elements = set(children) - set(level_one_group_ref)
            if extra_elements:
                hierarchy_error = 1
                self.log("These items are extra in "+world_groups[0]+" :")
                for item in extra_elements:
                    self.log(item)
                
            if cmds.objExists(world_groups[0]+'|Geometry'):
                inside_Geometry = cmds.listRelatives(world_groups[0]+'|Geometry', children=True)
                if inside_Geometry:
                    extra_elements = set(inside_Geometry) - set(inside_Geometry_ref)
                    missing_elements = set(inside_Geometry_ref) - set(inside_Geometry)                
                    if extra_elements:
                        hierarchy_error = 1
                        self.log("These items are extra in "+world_groups[0]+"|Geometry :")
                        for item in extra_elements:
                            self.log(item)

                    if missing_elements:
                        hierarchy_error = 1
                        missing_error = 1
                        self.log("These items are missing in "+world_groups[0]+"|Geometry :")
                        for item in missing_elements:
                            self.missing_groups.append(world_groups[0]+"|Geometry|"+item)
                            self.log(item)
                else:
                    missing_error = 1
                    hierarchy_error = 1
                    self.missing_groups += [world_groups[0]+'|Geometry|HiRes', world_groups[0]+'|Geometry|Proxy']
                    self.log("These items are missing in Geometry : \nHiRes\nProxy")
            
            
            
            if cmds.objExists(world_groups[0]+'|Rigging'):
                inside_Rigging = cmds.listRelatives(world_groups[0]+'|Rigging', children=True)
                if inside_Rigging:
                    extra_elements = set(inside_Rigging) - set(inside_Rigging_ref)
                    missing_elements = set(inside_Rigging_ref) - set(inside_Rigging)                
                    if extra_elements:
                        hierarchy_error = 1
                        self.log("These items are extra in "+world_groups[0]+"|Rigging :")
                        for item in extra_elements:
                            self.log(item)

                    if missing_elements:
                        hierarchy_error = 1
                        missing_error = 1
                        self.log("These items are missing in "+world_groups[0]+"|Rigging :")
                        for item in missing_elements:
                            self.missing_groups.append(world_groups[0]+"|Rigging|"+item)
                            self.log(item)                
                else:
                    missing_error = 1
                    hierarchy_error = 1
                    self.missing_groups += [world_groups[0]+'|Rigging|Deformers', world_groups[0]+'|Rigging|Skeleton']
                    self.log("These items are missing in Rigging : \nDeformers\nSkeleton")

            if cmds.objExists(world_groups[0]+'|Texture'):
                inside_Texture = cmds.listRelatives(world_groups[0]+'|Texture', children=True)
                if inside_Texture:
                    extra_elements = set(inside_Texture) - set(inside_Texture_ref)
                    missing_elements = set(inside_Texture_ref) - set(inside_Texture)                
                    if extra_elements:
                        hierarchy_error = 1
                        self.log("These items are extra in "+world_groups[0]+"|Texture :")
                        for item in extra_elements:
                            self.log(item)

                    if missing_elements:
                        hierarchy_error = 1
                        missing_error = 1
                        self.log("These items are missing in "+world_groups[0]+"|Texture :")
                        for item in missing_elements:
                            self.missing_groups.append(world_groups[0]+"|Texture|"+item)
                            self.log(item)           
                else:
                    missing_error = 1
                    hierarchy_error = 1
                    self.missing_groups += [world_groups[0]+'|Texture|Place3d', world_groups[0]+'|Texture|Texture_Ref']
                    self.log("These items are missing in Texture : \nPlace3d\nTexture_Ref")

            if not hierarchy_error:
                self.log("There isn't any error in hierarchy.")
            else:
                if missing_error == 1:
                    self.theMainWidget.hierarchy_structure_fix_pushButton.setEnabled(True)
        
        
        else:
            # If no world group is found
            self.log("Check World Node Naming First!")

    def fix_hierarchy_structure(self):
        self.missing_groups = sorted(self.missing_groups, key=len)
        print(self.missing_groups)
        for item in self.missing_groups:
            destination, group_name = item.rsplit('|',1)
            cmds.group(em=True, name=group_name, parent=destination)
            if group_name in ['Proxy', 'Place3d', 'Texture_Ref', 'Deformers', 'Skeleton']:
                cmds.setAttr(item + ".visibility", 0)

            
        self.theMainWidget.hierarchy_structure_fix_pushButton.setEnabled(False)

    
    
    def check_visibility_off_groups(self):
        self.log_textEdit.clear()
        visibility_error = 0
        self.visibility_error_nodes = []
        root_nodes = cmds.ls(assemblies=True)
        group_nodes = [node for node in root_nodes if cmds.nodeType(node) == "transform"]       
        world_groups = []        
        for node in group_nodes:
            if node.startswith("World_"):
                world_groups.append(node)
        if (len(world_groups) == 1) and (world_groups[0] != "World_AssetName") and (world_groups[0] in cmds.ls(assemblies=True)):

            visibility_off_groups = ['|'+world_groups[0]+'|Geometry|Proxy','|'+world_groups[0]+'|Texture|Place3d','|'+world_groups[0]+'|Texture|Texture_Ref','|'+world_groups[0]+'|Rigging|Deformers','|'+world_groups[0]+'|Rigging|Skeleton']
            for node in visibility_off_groups:
                if cmds.objExists(node):
                    visibility = cmds.getAttr(node + '.visibility')
                    if visibility:
                        visibility_error = 1
                        self.visibility_error_nodes.append(node)
                        self.log(node+" visibility is on!")
            if not visibility_error:
                self.log("Visibility of the hidden groups are correct.")
            else:
                self.theMainWidget.visibility_off_groups_fix_pushButton.setEnabled(True)

        else:
            self.log("Check World Node Naming First!")

    def fix_visibility_off_groups(self):
        self.log_textEdit.clear()
        vis_fix_error = False
        for node in self.visibility_error_nodes:
            is_locked = cmds.getAttr(node + '.visibility', lock=True)
            connections = cmds.listConnections(node + '.visibility', source=True, destination=False)
            if not is_locked and not connections:
                cmds.setAttr(node+'.visibility', 0)
                self.log(node+" visibility is off!")
            else:
                self.log("Visibility attribute of "+node+" is locked or connected.")
                vis_fix_error = True
        if not vis_fix_error:
            self.log("Proxy, Place3d, Texture_Ref, Deformers, Skeleton groups are hidden now.")
        self.theMainWidget.visibility_off_groups_fix_pushButton.setEnabled(False)
            
    def check_object_names(self):
        self.log_textEdit.clear()
        naming_error = 0
        root_nodes = cmds.ls(assemblies=True)
        group_nodes = [node for node in root_nodes if cmds.nodeType(node) == "transform"]
        world_groups = []        
        for node in group_nodes:
            if node.startswith("World_"):
                world_groups.append(node)
        if (len(world_groups) == 1) and (world_groups[0] != "World_AssetName") and (world_groups[0] in cmds.ls(assemblies=True)):
            
            # geo
            all_geometry = cmds.listRelatives(world_groups[0]+'|Geometry', allDescendents=True, fullPath=True) or []
            meshes = [geo for geo in all_geometry if cmds.nodeType(geo) == 'mesh']
            geo_transforms = []
            for geo in meshes:
                transform = cmds.listRelatives(geo, parent=True)[0]
                geo_transforms.append(transform)        
                
            for geo in geo_transforms:
                if not geo.endswith('_Geo'):
                    naming_error = 1
                    self.log("Geometries without '_Geo' extension : "+geo)
            
            # curves in Controllers group
            group_name = '|'+world_groups[0]+'|Controllers'
            curve_transforms = []
            curves = cmds.listRelatives(group_name, ad=True, type='nurbsCurve') or []
            for curve in curves:
                transform = cmds.listRelatives(curve, parent=True)[0]
                curve_transforms.append(transform)
            curve_transforms = list(set(curve_transforms))
            for curve in curve_transforms:
                if not curve.endswith('_Ctrl'):
                    naming_error = 1
                    self.log("Controllers without '_Ctrl' extension : "+curve)     
            # joints
            joints = cmds.ls(type="joint")
            for joint in joints:
                if not joint.endswith("_jnt"):
                    naming_error = 1
                    self.log("joints without '_jnt' extension : "+joint)     

            # proxies in Proxy group
            group_name = '|'+world_groups[0]+'|Geometry|Proxy'
            mesh_transforms = []
            meshes = cmds.listRelatives(group_name, ad=True, type='mesh') or []
            for mesh in meshes:
                transform = cmds.listRelatives(mesh, parent=True)[0]
                mesh_transforms.append(transform)
            for mesh in mesh_transforms:
                if not mesh.endswith('_Proxy_Geo'):
                    naming_error = 1
                    self.log("Proxies without '_Proxy_Geo' extension : "+mesh)        
            if not naming_error:
                self.log("There isn't any naming error.")        
                
        else:
            self.log("Check World Node Naming First!")
    
    def check_non_deformer_history(self):
        self.log_textEdit.clear()
        construction_error = 0
        all_objects = cmds.ls(type='transform')
        mesh_geometries = []
        for obj in all_objects:
            # Check if the object is a mesh
            if cmds.objectType(obj) == 'transform' and cmds.listRelatives(obj, shapes=True):
                shape_node = cmds.listRelatives(obj, shapes=True, fullPath=True)[0]
                if cmds.objectType(shape_node) == 'mesh':
                    mesh_geometries.append(obj)

        polyNodes = cmds.nodeType('polyBase', itn=True, d=True)
        for mesh in mesh_geometries:
            history = cmds.listHistory(mesh)
            for item in history:                
                if cmds.nodeType(item) in polyNodes:
                    self.log(item+' node in '+mesh+' geometry is a construction history.\n')
                    construction_error = 1
        if not construction_error:
            self.log("There isn't any construction history in the scene.")


    def check_duplicate_names(self):
        self.log_textEdit.clear()
        duplicate_names_error = 0
        allNames= cmds.ls(dag=1)
        nameClash=[]
        for Name in allNames:
            if len(Name.split('|'))>1:
                nameClash.append(Name.split('|')[-1])
        # Create an empty dictionary to store counts
        counts = {}
        # Count occurrences of each item
        for item in nameClash:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        # Print repeated items with repeat count
        for item, count in counts.items():
            if count > 1:
                self.log("'"+item+"' name is appears "+count+" times in the scene.")
                duplicate_names_error = 1
        if not duplicate_names_error:
            self.log("There isn't any name error in the scene.")
    
    def check_ghost_nodes(self):
        self.log_textEdit.clear()
        ghost_node_error = 0
        self.ghost_nodes = []
        maya_default_isolated_nodes = ['time1',
        'sequenceManager1',
        'hardwareRenderingGlobals',
        'renderPartition',
        'renderGlobalsList1',
        'defaultLightList1',
        'defaultShaderList1',
        'postProcessList1',
        'defaultRenderUtilityList1',
        'defaultRenderingList1',
        'lightList1',
        'defaultTextureList1',
        'lambert1',
        'standardSurface1',
        'particleCloud1',
        'initialShadingGroup',
        'initialParticleSE',
        'initialMaterialInfo',
        'shaderGlow1',
        'dof1',
        'defaultRenderGlobals',
        'defaultRenderQuality',
        'defaultResolution',
        'defaultLightSet',
        'defaultObjectSet',
        'defaultViewColorManager',
        'defaultColorMgtGlobals',
        'hardwareRenderGlobals',
        'characterPartition',
        'defaultHardwareRenderGlobals',
        'ikSystem',
        'hyperGraphInfo',
        'hyperGraphLayout',
        'globalCacheControl',
        'strokeGlobals',
        'dynController1',
        'lightLinker1',
        'persp',
        'perspShape',
        'top',
        'topShape',
        'front',
        'frontShape',
        'side',
        'sideShape',
        'shapeEditorManager',
        'poseInterpolatorManager',
        'layerManager',
        'defaultLayer',
        'renderLayerManager',
        'defaultRenderLayer',
        'defaultArnoldRenderOptions',
        'defaultArnoldFilter',
        'defaultArnoldDriver',
        'defaultArnoldDisplayDriver',
        'mayaUsdLayerManager1',
        'uiConfigurationScriptNode',
        'sceneConfigurationScriptNode',
        'MayaNodeEditorSavedTabsInfo']

        root_nodes = cmds.ls(assemblies=True)
        group_nodes = [node for node in root_nodes if cmds.nodeType(node) == "transform"]
        world_groups = []        
        for node in group_nodes:
            if node.startswith("World_"):
                world_groups.append(node)
        if (len(world_groups) == 1) and (world_groups[0] != "World_AssetName") and (world_groups[0] in cmds.ls(assemblies=True)):        
                       
            project_groups = [world_groups[0],
            'Geometry',
            'Texture',
            'Controllers',
            'Rigging',
            'Lighting',
            'FX',
            'Misc',
            'Deformers',
            'Skeleton',
            'Place3d',
            'Texture_Ref',
            'HiRes',
            'Proxy']
        
               
            all_nodes = cmds.ls(dag=0)
            node_types_to_remove = ["joint", "nurbsCurve", "camera"]
            filtered_nodes = [node for node in all_nodes if cmds.nodeType(node) not in node_types_to_remove]
            
            # remove shapes that they have transform
            mesh_nodes = cmds.ls(all_nodes, type='mesh')
            shapes_with_transform = []
            for mesh_node in mesh_nodes:
                if(cmds.listRelatives(mesh_node, parent=True, fullPath=True)):
                    shapes_with_transform.append(mesh_node)
            filtered_nodes_2 = [item for item in filtered_nodes if item not in shapes_with_transform]       
            
            # find nodes without connection
            isolate_nodes = []
            for node in filtered_nodes_2:

                input_connections = cmds.listConnections(node, source=True, destination=False)
                output_connections = cmds.listConnections(node, source=False, destination=True)
                if not input_connections and not output_connections:
                    isolate_nodes.append(node)            


            # remove maya default nodes
            filtered_nodes_3 = [item for item in isolate_nodes if item not in maya_default_isolated_nodes]
            # remove project groups nodes
            filtered_nodes_4 = [item for item in filtered_nodes_3 if item not in project_groups]
            
            for item in filtered_nodes_4[:]:
                # print(item)
                # if cmds.objectType(item)== 'transform' and len(cmds.listRelatives(item) or [])>0:
                # if node have a parnet it's node ghost
                if len(cmds.listRelatives(item,p=1) or [])>0:
                    filtered_nodes_4.remove(item)

            # remove lock nodes
            for item in filtered_nodes_4[:]:
                is_locked = cmds.lockNode(item, q=True, lock=True)[0]
                if is_locked:
                    filtered_nodes_4.remove(item)              
            
            
            for item in filtered_nodes_4:
                self.ghost_nodes.append(item)
                self.theMainWidget.ghost_nodes_fix_pushButton.setEnabled(True)
                self.log('ghost nodes:\n' + item+'\n')
                ghost_node_error = 1
            if not ghost_node_error:
                self.log("There isn't any ghost node in the scene.")
        else:
            self.log("Check World Node Naming First!")


    def fix_ghost_nodes(self):
        self.log_textEdit.clear()
        for item in self.ghost_nodes:
            self.log("deleting :"+item)
            cmds.delete(item)
        self.theMainWidget.ghost_nodes_fix_pushButton.setEnabled(False)
    
    
    def check_extra_cameras(self):        
        self.log_textEdit.clear()
        light_camera_error = 0
        # List all lights in the scene
        self.extra_lights = cmds.ls(type='light')
        if self.extra_lights:
            self.theMainWidget.extra_camera_fix_pushButton.setEnabled(True)
            light_camera_error = 1
            self.log("Extra lights found in the scene:")
            for light in self.extra_lights:
                self.log(light)
            

        # List all cameras in the scene
        all_cameras = cmds.ls(type='camera')
        
        # List default cameras
        default_cameras = ['frontShape', 'perspShape', 'sideShape', 'topShape']
        
        self.extra_cameras = []
        # Check if any camera is not in the default cameras list
        for camera in all_cameras:
            if camera not in default_cameras:
                self.extra_cameras.append(camera)
        
        if self.extra_cameras: 
            light_camera_error = 1           
            self.log("Extra cameras found in the scene:")
            for camera in self.extra_cameras:
                self.log(camera)
            self.theMainWidget.extra_camera_fix_pushButton.setEnabled(True)
        if not light_camera_error:
            self.log("No light and camera error in the scene.")

    def fix_extra_cameras(self):
        self.log_textEdit.clear()
        
        for item in self.extra_lights:
            if cmds.listRelatives(item, parent=True, fullPath=True):
                cmds.delete(cmds.listRelatives(item, parent=True, fullPath=True))      
                
        for item in self.extra_cameras:
            if cmds.listRelatives(item, parent=True, fullPath=True):
                cmds.delete(cmds.listRelatives(item, parent=True, fullPath=True))
        self.theMainWidget.extra_camera_fix_pushButton.setEnabled(False)


    def check_transform_values(self):
        self.log_textEdit.clear()
        root_nodes = cmds.ls(assemblies=True)
        group_nodes = [node for node in root_nodes if cmds.nodeType(node) == "transform"]
        world_groups = []        
        for node in group_nodes:
            if node.startswith("World_"):
                world_groups.append(node)
        if (len(world_groups) == 1) and (world_groups[0] != "World_AssetName") and (world_groups[0] in cmds.ls(assemblies=True)):        
                       
            project_groups = [world_groups[0],
            'Geometry',
            'Texture',
            'Controllers',
            'Rigging',
            'Lighting',
            'FX',
            'Misc',
            'Deformers',
            'Skeleton',
            'Place3d',
            'Texture_Ref',
            'HiRes',
            'Proxy']
            self.log_textEdit.clear()
            transform_error = 0
            all_transforms = []
            all_shapes = cmds.ls(type='mesh')
            for shape in all_shapes:
                # Get the transform node of the shape
                all_transforms.append(cmds.listRelatives(shape, parent=True)[0])
            
            all_curves = cmds.ls(type='nurbsCurve')
            for curve in all_curves:
                # Get the transform node of the shape
                all_transforms.append(cmds.listRelatives(curve, parent=True)[0])

            all_transforms+=project_groups
            for transform in all_transforms:

                translation = cmds.getAttr(transform + ".translate")[0]
                rotation = cmds.getAttr(transform + ".rotate")[0]
                scale = cmds.getAttr(transform + ".scale")[0]

                if (translation != (0.0, 0.0, 0.0) or 
                    rotation != (0.0, 0.0, 0.0) or 
                    scale != (1.0, 1.0, 1.0)):
                    transform_error = 1
                    self.log(transform+" has non-zero transform attributes.")
            if not transform_error:
                self.log("There is no transform value.")    
        else:
            self.log("Check World Node Naming First!")


    def check_two_shape(self):
        two_shape_error = False
        self.log_textEdit.clear()
        all_meshes = cmds.ls(type='mesh', long=True)
        
        # Dictionary to hold parent and their child meshes
        parent_dict = {}
        
        for mesh in all_meshes:
            parents = cmds.listRelatives(mesh, parent=True, fullPath=True) 
            
            if parents:
                parents = parents[0]
                if parents in parent_dict:
                    parent_dict[parents].append(mesh)
                else:
                    parent_dict[parents] = [mesh]
        
        have_deformer = False        
        for parents, meshes in parent_dict.items():
            Origins = []
            have_deformer = False
            if cmds.bakePartialHistory(parents,query=True,prePostDeformers=True, preDeformers=True ):
                have_deformer = True
            for item in meshes:
                if item.endswith('Orig'):
                    Origins.append(item)
            if len(meshes) > 1 and not have_deformer:
                self.log(parents+' have more than one shape.\n')
                two_shape_error = True
            elif len(meshes) > 1 and have_deformer:
                if len(Origins)>1:
                    self.log(parents+' have more than one shape. and deformer\n')
                    two_shape_error = True
        if not two_shape_error:
            self.log("There isn't any mesh with two shape.")     



try:
    ui.deleteLater()
except:
    pass
ui = AssetChecklist()

def main():
    ui.show()


    
