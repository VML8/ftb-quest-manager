import ftb_snbt_lib as slib
import json

# JSON String
def snbt_to_json(snbt_text: str) -> str:
    data = slib.loads(snbt_text)   # parse SNBT string → Compound Python Data Type
    return json.dumps(data, indent=2)  # convert Compound Python Data Type → pretty JSON string

if __name__ == "__main__":
    file_path = "v:\\Quest_Manager\\tests\\cwd_test\\config\\ftbquests\\quests\\chapters\\welcome.snbt"
    
    with open(file_path, "r") as f:
        print(snbt_to_json(f.read()))