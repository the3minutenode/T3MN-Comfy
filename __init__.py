# The 3-Minute Node ComfyUI Custom Nodes v0.1 260518
from .nodes import ExifToolMetadata, NodeSourceCodeViewer, ResilientModelExtractor

NODE_CLASS_MAPPINGS = {
    "ExifToolMetadata": ExifToolMetadata,
    "NodeSourceCodeViewer": NodeSourceCodeViewer,
    "ResilientModelExtractor": ResilientModelExtractor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExifToolMetadata": "ExifTool Full Metadata",
    "NodeSourceCodeViewer": "Node Source Code Viewer",
    "ResilientModelExtractor": "Resilient Model Extractor (Recursive)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
RESET = "\033[0m"

node_name = "T3MN Comfy"
version = "v0.1"

print(f"{CYAN}[{node_name}]{RESET} version: {version} Loaded")
