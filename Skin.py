import json
import maya.cmds as cmds

def export_skin_weights_to_json(mesh_name, jsonPath):
    """
    Export skin weights from the specified mesh to a JSON file.
    :param mesh_name: The name of the mesh with skin weights.
    :param jsonPath: The path to the JSON file where skin weights will be saved.
    """
    skinCluster = find_skinCluster(mesh_name)
    if not skinCluster:
        print("Error: No skin cluster found on the specified mesh.")
        return

    skin_weights_data = get_skin_weights_data(mesh_name, skinCluster)
    
    with open(jsonPath, 'w') as jsonFile:
        json.dump(skin_weights_data, jsonFile, indent=2)

    print(f"Skin weights exported to: {jsonPath}")

def import_skin_weights_from_json(mesh_name, jsonPath):
    """
    Import skin weights from a JSON file to the specified mesh.
    :param mesh_name: The name of the mesh to import skin weights onto.
    :param jsonPath: The path to the JSON file containing skin weights.
    """
    skinCluster = find_skinCluster(mesh_name)
    if not skinCluster:
        print("Error: No skin cluster found on the specified mesh.")
        return

    with open(jsonPath, 'r') as jsonFile:
        skin_weights_data = json.load(jsonFile)

    set_skin_weights_data(mesh_name, skinCluster, skin_weights_data)
    print(f"Skin weights imported from: {jsonPath}")

def find_skinCluster(mesh_name):
    """
    Find the skin cluster on the specified mesh.
    :param mesh_name: The name of the mesh to find the skin cluster on.
    :return: The name of the skin cluster if found, otherwise None.
    """
    history = cmds.listHistory(mesh_name)
    skinCluster = next((node for node in history if cmds.nodeType(node) == 'skinCluster'), None)
    return skinCluster

def get_skin_weights_data(mesh_name, skinCluster):
    """
    Get skin weights data from the specified mesh and skin cluster.
    :param mesh_name: The name of the mesh.
    :param skinCluster: The name of the skin cluster.
    :return: Skin weights data in dictionary format.
    """
    influence_joints = cmds.skinCluster(skinCluster, q=True, inf=True)
    vertices = cmds.polyEvaluate(mesh_name, vertex=True)
    
    skin_weights_data = {}

    for vertex in range(vertices):
        weights = cmds.skinPercent(skinCluster, f"{mesh_name}.vtx[{vertex}]", q=True, value=True)
        skin_weights_data[vertex] = {joint: weight for joint, weight in zip(influence_joints, weights)}

    return skin_weights_data

def set_skin_weights_data(mesh_name, skinCluster, skin_weights_data):
    # Désactiver la normalisation automatique
    cmds.setAttr(f"{skinCluster}.normalizeWeights", 0)

    for vertex, weights in skin_weights_data.items():
        transform_values = [(joint, weight) for joint, weight in weights.items()]

        cmds.skinPercent(
            skinCluster,
            f"{mesh_name}.vtx[{vertex}]",
            transformValue=transform_values
        )

    # Réactiver et forcer la normalisation
    cmds.setAttr(f"{skinCluster}.normalizeWeights", 1)
    cmds.skinCluster(skinCluster, e=True, forceNormalizeWeights=True)


# Example Usage:
export_skin_weights_to_json("test_geo", "C:/Users/theouser/Documents/trashTEST/test_weights.json")
import_skin_weights_from_json("blabla_geo", "C:/Users/theouser/Documents/trashTEST/test_weights.json")
