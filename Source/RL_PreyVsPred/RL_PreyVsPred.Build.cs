// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class RL_PreyVsPred : ModuleRules
{
	public RL_PreyVsPred(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG",
			"Slate"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });

		PublicIncludePaths.AddRange(new string[] {
			"RL_PreyVsPred",
			"RL_PreyVsPred/Variant_Platforming",
			"RL_PreyVsPred/Variant_Platforming/Animation",
			"RL_PreyVsPred/Variant_Combat",
			"RL_PreyVsPred/Variant_Combat/AI",
			"RL_PreyVsPred/Variant_Combat/Animation",
			"RL_PreyVsPred/Variant_Combat/Gameplay",
			"RL_PreyVsPred/Variant_Combat/Interfaces",
			"RL_PreyVsPred/Variant_Combat/UI",
			"RL_PreyVsPred/Variant_SideScrolling",
			"RL_PreyVsPred/Variant_SideScrolling/AI",
			"RL_PreyVsPred/Variant_SideScrolling/Gameplay",
			"RL_PreyVsPred/Variant_SideScrolling/Interfaces",
			"RL_PreyVsPred/Variant_SideScrolling/UI"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
