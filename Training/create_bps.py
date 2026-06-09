import unreal

"""
Ejecutar en el Editor:  Window > Developer Tools > Python Console
>>> exec(open("C:/Users/aaran/Documents/Unreal Engine Projects/RL_PreyVsPred-USFX2026/Training/create_bps.py").read())
"""

PATH = "/Game/PredatorPreySim"

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
editor_asset_lib = unreal.EditorAssetLibrary

if not editor_asset_lib.does_directory_exist(PATH):
    editor_asset_lib.make_directory(PATH)


def create_bp(parent_class, name):
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("ParentClass", parent_class)
    asset = asset_tools.create_asset(name, PATH, None, factory)
    if asset:
        print(f"  Created {name} ({parent_class.get_name()})")
    else:
        print(f"  FAILED: {name}")
    return asset


print("Creating Blueprints...")

bp_entorno   = create_bp(unreal.AEntorno, "BP_Entorno")
bp_presa     = create_bp(unreal.APresa, "BP_Presa")
bp_predator  = create_bp(unreal.APredator, "BP_Predator")
bp_facade    = create_bp(unreal.AFacadeSimulation, "BP_FacadeSimulation")

# Wire defaults: BP_Entorno -> PreyClass / PredatorClass
if bp_entorno and bp_presa and bp_predator:
    bp_entorno.set_editor_property("PreyClass", bp_presa.get_class())
    bp_entorno.set_editor_property("PredatorClass", bp_predator.get_class())
    print("  Wired PreyClass / PredatorClass in BP_Entorno")

# Wire defaults: BP_FacadeSimulation -> Entorno class hint (optional)
if bp_facade and bp_entorno:
    print("  Remember to assign BP_Entorno to BP_FacadeSimulation.Entorno in the level")

editor_asset_lib.save_directory(PATH)
print(f"\nDone! Check Content Browser under {PATH}")
