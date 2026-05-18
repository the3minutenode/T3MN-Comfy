import subprocess
import os
import json
import folder_paths
import inspect
import nodes
from .helper import get_exiftool

class ExifToolMetadata:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_path": ("STRING", {"default": "path/to/image or video.png"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_output",)
    FUNCTION = "get_metadata"
    CATEGORY = "t3mn"

    def get_metadata(self, image_path):
        image_path = image_path.strip().strip('"')
        base_path = os.path.dirname(os.path.realpath(__file__))
        
        exiftool_path = get_exiftool(base_path)
        
        if not exiftool_path or not os.path.exists(exiftool_path):
            return (f"ExifTool binary missing or unsupported OS.",)

        if not os.path.exists(image_path):
            return (f"Image not found at: {image_path}",)

        # Execute: exiftool -a -u -g1 -json [path]
        try:
            process = subprocess.run(
                [exiftool_path, "-a", "-u", "-g1", "-json", image_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            metadata_list = json.loads(process.stdout)
            metadata_dict = metadata_list[0] if metadata_list else {}
            
            # Format as a readable string for the UI
            json_output = json.dumps(metadata_dict, indent=4)
            
            return (json_output,)
            
        except Exception as e:
            return (f"Error: {str(e)}",)

class NodeSourceCodeViewer:
    @classmethod
    def INPUT_TYPES(s):
        # Create a list of "Category -> NodeName" strings
        grouped_list = []
        
        for name, cls in nodes.NODE_CLASS_MAPPINGS.items():
            # Get the category, defaulting to "Uncategorized"
            category = getattr(cls, "CATEGORY", "Uncategorized")
            grouped_list.append(f"{category}/{name}")
            
        return {
            "required": {
                # Sort them so groups stick together
                "node_path": (sorted(grouped_list),),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("source_code",)
    FUNCTION = "get_source"
    CATEGORY = "t3mn"

    def get_source(self, node_path):
        # Extract the actual node name from our "Group -> Name" string
        try:
            node_name = node_path.split("/")[-1]
            node_class = nodes.NODE_CLASS_MAPPINGS.get(node_name)
            
            if node_class is None:
                return (f"Node '{node_name}' not found.",)

            file_path = inspect.getfile(node_class)
            source_code = inspect.getsource(node_class)
            
            header = f"# Category: {node_path.split('/')[0]}\n# Path: {file_path}\n\n"
            return (header + source_code,)
            
        except Exception as e:
            return (f"Error: {str(e)}",)

class ResilientModelExtractor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_path": ("STRING", {"default": "path/to/.json"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_report",)
    FUNCTION = "extract_models"
    CATEGORY = "t3mn"
    
    def extract_models(self, json_path=""):
        data = None
        report_lines = []
        json_path = json_path.strip().strip('"')

        # load the JSON data
        if json_path and os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                return (f"Error reading JSON file path: {str(e)}",)
        else:
            return ("Invalid JSON file path.",)

        # scan the "nodes" array
        nodes = data.get("nodes", [])
        extracted_models = []

        for node in nodes:
            if not isinstance(node, dict):
                continue
            
            if node.get("type") == "MarkdownNote":
                continue

            # gather all .safetensors files found anywhere inside this specific node
            found_files = []
            self.find_safetensors_recursive(node, found_files)

            if found_files:
                node_type = node.get("type", "Unknown Class")
                node_id = node.get("id", "Unknown ID")
                # node_title = node.get("title") or node.get("properties", {}).get("Node name for S&R", "No Title")

                for file_name in set(found_files): # set() avoids duplicates if it appears twice in one node
                    extracted_models.append({
                        "file_name": file_name,
                        "node_type": node_type,
                        "node_id": node_id,
                        # "node_title": node_title
                    })

        # build the report
        report_lines.append("--- safetensors search ---")
        if not extracted_models:
            report_lines.append("No '.safetensors' references discovered in this workflow structure.")
        else:
            for item in extracted_models:
                report_lines.append(f"Model File: {item['file_name']}")
                report_lines.append(f"  ├── Node Class (Type): {item['node_type']}")
                report_lines.append(f"  ├── Node ID: {item['node_id']}")
                # report_lines.append(f"  └── Node Title/Alias: {item['node_title']}")
                report_lines.append("-" * 45)

        return ("\n".join(report_lines),)

    def find_safetensors_recursive(self, target, found_list):
        """Recursively traverses lists and dicts looking for .safetensors strings"""
        if isinstance(target, str):
            cleaned_target = target.split('?')[0].strip()

            if cleaned_target.lower().endswith(".safetensors"):
                file_name = os.path.basename(cleaned_target)
                if file_name not in found_list:
                    found_list.append(file_name)
        elif isinstance(target, dict):
            for value in target.values():
                self.find_safetensors_recursive(value, found_list)
        elif isinstance(target, list):
            for item in target:
                self.find_safetensors_recursive(item, found_list)

