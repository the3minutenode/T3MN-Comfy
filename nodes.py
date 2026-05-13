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

    RETURN_TYPES = ("STRING")
    RETURN_NAMES = ("json_output")
    FUNCTION = "get_metadata"
    CATEGORY = "t3mn"

    def get_metadata(self, image_path):
        image_path = image_path.strip().strip('"')
        base_path = os.path.dirname(os.path.realpath(__file__))
        
        exiftool_path = get_exiftool(base_path)
        
        if not exiftool_path or not os.path.exists(exiftool_path):
            return (f"ExifTool binary missing or unsupported OS.", {})

        if not os.path.exists(image_path):
            return (f"Image not found at: {image_path}", {})

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
            
            return (json_output)
            
        except Exception as e:
            return (f"Error running ExifTool: {str(e)}", {})

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
            }
        }

    RETURN_TYPES = ("STRING",)
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

