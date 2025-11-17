import os
import json
import ftb_snbt_lib as slib
from typing import Dict, List, Any, Optional
from rich import print
from rich.tree import Tree

data = {
	"ae2": {
		"default_hide_dependency_lines": 0,
		"default_quest_shape": "",
		"filename": "ae2",
		"group": "1762581C74A6AA93",
		"id": "5571D3126CC74A4D",
		"order_index": 0,
		"quest_links": [],
		"quests": {
			"27777A5CD65CF52D": {
				"id": "27777A5CD65CF52D",
				"rewards": {
					"1E7BBCBA4689BB77": {
						"id": "1E7BBCBA4689BB77",
						"item": {
							"count": 1,
							"id": "ae2:flawless_budding_quartz"
						},
						"type": "item"
					}
				},
				"tasks": {
					"7BCF714BA47BACC3": {
						"id": "7BCF714BA47BACC3",
						"item": {
							"count": 1,
							"id": "ae2:meteorite_compass"
						},
						"optional_task": 1,
						"type": "item"
					},
					"040B4FBBB43C86BA": {
						"count": 8,
						"id": "040B4FBBB43C86BA",
						"item": {
							"count": 1,
							"id": "ae2:sky_stone_block"
						},
						"type": "item"
					},
					"20B26628DFD499B4": {
						"id": "20B26628DFD499B4",
						"item": {
							"count": 1,
							"id": "ae2:calculation_processor_press"
						},
						"type": "item"
					},
					"669F38187ADA9DF6": {
						"id": "669F38187ADA9DF6",
						"item": {
							"count": 1,
							"id": "ae2:engineering_processor_press"
						},
						"type": "item"
					},
					"4C8E2D981ACAE0AC": {
						"id": "4C8E2D981ACAE0AC",
						"item": {
							"count": 1,
							"id": "ae2:logic_processor_press"
						},
						"type": "item"
					},
					"3B0A88FDE6A6FBF5": {
						"id": "3B0A88FDE6A6FBF5",
						"item": {
							"count": 1,
							"id": "ae2:silicon_press"
						},
						"type": "item"
					}
				},
				"x": 0,
				"y": 0,
				"quest_subtitle": "Poor dinosaur..."
			}
		},
		"title": "AE2"
	},
	"drawer": {
		"default_hide_dependency_lines": 0,
		"default_quest_shape": "",
		"filename": "drawer",
		"group": "1762581C74A6AA93",
		"id": "2884DF15DC3D8354",
		"order_index": 1,
		"quest_links": [],
		"quests": {
			"2BE61628814654B9": {
				"id": "2BE61628814654B9",
				"rewards": {
					"1E61B1EC90592120": {
						"id": "1E61B1EC90592120",
						"item": {
							"count": 1,
							"id": "storagedrawers:drawer_key"
						},
						"type": "item"
					}
				},
				"tasks": {
					"51D3FB070290C4AA": {
						"id": "51D3FB070290C4AA",
						"item": {
							"components": {
								"ftbfiltersystem:filter": "ftbfiltersystem:item_tag(storagedrawers:drawers)"
							},
							"count": 1,
							"id": "ftbfiltersystem:smart_filter"
						},
						"type": "item",
						"title": "Any #storagedrawers:drawers"
					}
				},
				"x": 0,
				"y": 0,
				"title": "Drawer"
			},
			"261110CB645DABB9": {
				"dependencies": [
					"2BE61628814654B9"
				],
				"id": "261110CB645DABB9",
				"rewards": {
					"6BA361C5F6FE8AC7": {
						"id": "6BA361C5F6FE8AC7",
						"item": {
							"count": 1,
							"id": "storagedrawers:keyring"
						},
						"type": "item"
					}
				},
				"tasks": {
					"01241D9931596A31": {
						"id": "01241D9931596A31",
						"item": {
							"count": 1,
							"id": "storagedrawers:controller"
						},
						"type": "item"
					}
				},
				"x": 0,
				"y": -1.5,
				"quest_subtitle": "Centralized"
			},
			"5A03F5DC8945508D": {
				"dependencies": [
					"261110CB645DABB9"
				],
				"hide_dependency_lines": 1,
				"hide_details_until_startable": 1,
				"hide_lock_icon": 1,
				"hide_text_until_complete": 1,
				"hide_until_deps_complete": 1,
				"hide_until_deps_visible": 1,
				"id": "5A03F5DC8945508D",
				"rewards": {
					"4EC1BF753EAEC604": {
						"id": "4EC1BF753EAEC604",
						"item": {
							"count": 1,
							"id": "storagedrawers:drawer_puller"
						},
						"type": "item"
					}
				},
				"tasks": {
					"491D756E8249316D": {
						"id": "491D756E8249316D",
						"item": {
							"components": {
								"ftbfiltersystem:filter": "or(item(storagedrawers:compacting_half_drawers_3)item(storagedrawers:compacting_half_drawers_2)item(storagedrawers:compacting_drawers_3)item(storagedrawers:compacting_drawers_2))"
							},
							"count": 1,
							"id": "ftbfiltersystem:smart_filter"
						},
						"type": "item"
					}
				},
				"x": 2,
				"y": -1.5,
				"title": "Compacting Drawer"
			}
		},
		"title": "Drawer"
	},
	"shop": {
		"default_hide_dependency_lines": 0,
		"default_quest_shape": "",
		"default_repeatable_quest": 1,
		"filename": "shop",
		"group": "",
		"id": "0825DC43C37BB9E1",
		"order_index": 1,
		"quest_links": [],
		"quests": {
			"2F47C361835F9304": {
				"can_repeat": 1,
				"id": "2F47C361835F9304",
				"rewards": {
					"043163683B23C6D5": {
						"count": 4,
						"id": "043163683B23C6D5",
						"item": {
							"count": 1,
							"id": "create:experience_nugget"
						},
						"type": "item"
					}
				},
				"tasks": {
					"0C7B7417A40E4773": {
						"consume_items": 1,
						"count": 16,
						"id": "0C7B7417A40E4773",
						"item": {
							"count": 1,
							"id": "minecraft:quartz"
						},
						"type": "item"
					}
				},
				"x": 0,
				"y": 0
			}
		}
	},
	"welcome": {
		"default_hide_dependency_lines": 0,
		"default_quest_shape": "",
		"filename": "welcome",
		"group": "",
		"id": "647758C6161A52AF",
		"order_index": 0,
		"quest_links": [],
		"quests": {
			"2B665C5D30FC7E86": {
				"icon": {
					"id": "minecraft:grass_block"
				},
				"id": "2B665C5D30FC7E86",
				"rewards": {
					"65AC6680636196E9": {
						"count": 4,
						"id": "65AC6680636196E9",
						"item": {
							"count": 1,
							"id": "minecraft:bread"
						},
						"type": "item"
					}
				},
				"shape": "rsquare",
				"tasks": {
					"434E457C0D56A2A1": {
						"advancement": "minecraft:story/root",
						"criterion": "",
						"id": "434E457C0D56A2A1",
						"type": "advancement"
					}
				},
				"x": 0,
				"y": -2.5,
				"title": "WELCOME"
			},
			"46E93DBB901E4B0E": {
				"dependencies": [
					"2B665C5D30FC7E86"
				],
				"icon": {
					"id": "minecraft:apple"
				},
				"id": "46E93DBB901E4B0E",
				"rewards": {
					"2FB185E66EFB64D9": {
						"count": 4,
						"id": "2FB185E66EFB64D9",
						"item": {
							"count": 1,
							"id": "minecraft:bread"
						},
						"type": "item"
					}
				},
				"shape": "rsquare",
				"tasks": {
					"5F6931C9D5CC8FE4": {
						"id": "5F6931C9D5CC8FE4",
						"type": "checkmark",
						"title": "I understand"
					}
				},
				"x": 2,
				"y": -2.5,
				"title": "Appleskin QoL"
			},
			"468DD0A0480ADDAB": {
				"dependencies": [
					"2B665C5D30FC7E86"
				],
				"icon": {
					"id": "waystones:waystone"
				},
				"id": "468DD0A0480ADDAB",
				"rewards": {
					"2736A5A4BDF98652": {
						"count": 4,
						"id": "2736A5A4BDF98652",
						"item": {
							"count": 1,
							"id": "minecraft:bread"
						},
						"type": "item"
					}
				},
				"shape": "rsquare",
				"tasks": {
					"7098263B6DF24D2D": {
						"id": "7098263B6DF24D2D",
						"type": "checkmark"
					}
				},
				"x": 0,
				"y": -0.5,
				"title": "Waystones"
			},
			"6C73E1BB9B998906": {
				"dependencies": [
					"2B665C5D30FC7E86"
				],
				"icon": {
					"id": "minecraft:map"
				},
				"id": "6C73E1BB9B998906",
				"rewards": {
					"6C9064F959BBF0A2": {
						"count": 4,
						"id": "6C9064F959BBF0A2",
						"item": {
							"count": 1,
							"id": "minecraft:bread"
						},
						"type": "item"
					}
				},
				"shape": "rsquare",
				"tasks": {
					"3B8CBE4E06E998C6": {
						"id": "3B8CBE4E06E998C6",
						"type": "checkmark"
					}
				},
				"x": 2,
				"y": -0.5,
				"title": "Xaero's Maps"
			},
			"150588F2351A7539": {
				"dependencies": [
					"2B665C5D30FC7E86"
				],
				"icon": {
					"id": "buildinggadgets2:gadget_building"
				},
				"id": "150588F2351A7539",
				"rewards": {
					"37BC75746A854C15": {
						"count": 4,
						"id": "37BC75746A854C15",
						"item": {
							"count": 1,
							"id": "minecraft:bread"
						},
						"type": "item"
					}
				},
				"shape": "rsquare",
				"tasks": {
					"23148E6C476E4238": {
						"id": "23148E6C476E4238",
						"type": "checkmark"
					}
				},
				"x": -2,
				"y": -0.5,
				"title": "Building Gadgets Tools"
			},
			"54B1A4D1DCC9ACF2": {
				"dependencies": [
					"2B665C5D30FC7E86"
				],
				"icon": {
					"id": "gateways:gate_pearl"
				},
				"id": "54B1A4D1DCC9ACF2",
				"rewards": {
					"329259F0DD30948C": {
						"count": 4,
						"id": "329259F0DD30948C",
						"item": {
							"count": 1,
							"id": "minecraft:bread"
						},
						"type": "item"
					}
				},
				"shape": "rsquare",
				"tasks": {
					"5E26275EC94F88AA": {
						"id": "5E26275EC94F88AA",
						"type": "checkmark"
					}
				},
				"x": -2,
				"y": -2.5,
				"title": "GatewaysToEternity *"
			},
			"1A2B3C4D5E6F7890": {
				"dependencies": [
					"2B665C5D30FC7E86"
				],
				"icon": {
					"id": "denseores:dense_diamond_ore"
				},
				"id": "1A2B3C4D5E6F7890",
				"rewards": {
					"37D81649B93290F8": {
						"count": 4,
						"id": "37D81649B93290F8",
						"item": {
							"count": 1,
							"id": "minecraft:bread"
						},
						"type": "item"
					}
				},
				"shape": "rsquare",
				"tasks": {
					"06A82CBF58AEB0DD": {
						"id": "06A82CBF58AEB0DD",
						"type": "checkmark"
					}
				},
				"x": -2,
				"y": -4.5,
				"title": "Dense Ores"
			},
			"7A28674DC1D382B6": {
				"dependencies": [
					"2B665C5D30FC7E86"
				],
				"icon": {
					"components": {
						"minecraft:custom_data": {
							"GunCurrentAmmoCount": 17,
							"GunFireMode": "SEMI",
							"GunId": "tacz:glock_17",
							"HasBulletInBarrel": 1
						}
					},
					"id": "tacz:modern_kinetic_gun"
				},
				"id": "7A28674DC1D382B6",
				"rewards": {
					"2188CD026B0044A4": {
						"id": "2188CD026B0044A4",
						"item": {
							"components": {
								"minecraft:custom_data": {
									"GunCurrentAmmoCount": 17,
									"GunFireMode": "SEMI",
									"GunId": "tacz:glock_17",
									"HasBulletInBarrel": 1
								}
							},
							"count": 1,
							"id": "tacz:modern_kinetic_gun"
						},
						"type": "item"
					},
					"0D1E64E740583358": {
						"count": 54,
						"id": "0D1E64E740583358",
						"item": {
							"components": {
								"minecraft:custom_data": {
									"AmmoId": "tacz:9mm"
								},
								"minecraft:max_stack_size": 60
							},
							"count": 1,
							"id": "tacz:ammo"
						},
						"type": "item"
					}
				},
				"shape": "rsquare",
				"tasks": {
					"143A9DD0038D2FE8": {
						"id": "143A9DD0038D2FE8",
						"type": "checkmark",
						"title": "Give me guns!"
					}
				},
				"x": 2,
				"y": -4.5,
				"title": "TACZ"
			},
			"25563CA6CCCC2FA1": {
				"dependencies": [
					"2B665C5D30FC7E86"
				],
				"icon": {
					"id": "easy_villagers:trader"
				},
				"id": "25563CA6CCCC2FA1",
				"shape": "rsquare",
				"tasks": {
					"00778466F52A5062": {
						"id": "00778466F52A5062",
						"type": "checkmark",
						"title": "Easy Villager"
					}
				},
				"x": 0,
				"y": -4.5
			}
		},
		"title": "Welcome"
	}
}

def display(target_navigation: list[str], data) -> None:
	'''
	Displays the tree structure of the stored data.
	'''
	
	_data: Optional[dict[str, Any]] = data
	data_tree: Tree = None

	temp_tree_reference: Tree = None
	temp_data: list[str] = []
	current_data = _data
	current_tree: Tree = None

	container_name = ''
	
	# initialize
	data_tree = Tree(f"[bold blue]{target_navigation[0]}[/bold blue]")
	current_tree = data_tree
	for item in current_data.keys():
		if item not in target_navigation:   # Skip item that will be navigated
			data_tree.add(item)

	# Loop through target navigation
	for i, step in enumerate(target_navigation[1:], start=1):
		
		for key, value in current_data.items():
			if key in target_navigation:
				temp_tree_reference = current_tree.add(f"[bold green]{key}[/bold green]") # Reference to the deeper tree


		# move data pointer deeper
		current_data = current_data[step]
		current_tree = temp_tree_reference
		

		# add attribute key and value except type container
		for key, value in current_data.items():

			# Keep data and skip if dict
			if isinstance(value, dict):
				
				# unpack this temp_data for deeper keys
				for sub_key, sub_value in value.items():
					container_name = key
					temp_data.append(sub_key) # store child key in list

				continue
			
			temp_tree_reference.add(f"{key}: {value}") # add attribute
		
		current_tree = temp_tree_reference.add(f"[bold yellow]{container_name}[/bold yellow]")   # add and highlight container
		temp_tree_reference = Tree('empty')
		for key in temp_data:
			current_tree.add(key)    # Add deeper Key
		temp_data = []
		
		# Move data pointer
		current_data = current_data[container_name]

		# print('current_tree', current_tree)
		# for k, v in current_data.items():
		# 	print(k)
	
	print(data_tree)


# target_navigation = ['root']
# display(target_navigation, data)
# target_navigation = ['root', 'welcome']
# display(target_navigation, data)
target_navigation = ['root', 'welcome', '2B665C5D30FC7E86']
display(target_navigation, data)