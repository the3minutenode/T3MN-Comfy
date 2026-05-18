# 🟢 T3MN Comfy 

High-efficiency custom nodes for professional ComfyUI workflows. Developed by [The 3-Minute Node](https://www.youtube.com/@The3MinuteNode), this suite provides utility nodes designed to bridge the gap between technical inspection and creative execution. No bloat, no filler—just the tools needed for pro-level CGI pipelines.

## 🛠️ Included Nodes

### 1. ExifTool Full Metadata

A powerful inspection node that leverages the industry-standard **ExifTool** to extract every hidden detail from your images and videos.

* **Inputs:** Local file path to any image/video.
* **Outputs:** A formatted, human-readable json string for UI display.
* **Use Case:** Auditing workflow metadata, checking camera settings, or debugging embedded prompt data.

### 2. Node Source Code Viewer

A developer-centric utility that allows you to inspect the Python source code of *any* installed node directly within the ComfyUI interface.

* **Selection:** Browse nodes by category (e.g., `loaders/CheckpointLoaderSimple`).
* **Outputs:** Returns the full source code string including the file path.
* **Use Case:** Learning how specific nodes function under the hood or troubleshooting custom node conflicts without leaving your browser.

### 3. Resilient Model Extractor

A diagnostic workflow utility that parses ComfyUI JSON files to recursively scan, identify, and map every AI model referenced within the workflow.
* **Inputs**: Local file path to a ComfyUI workflow .json file.
* **Outputs**: Structured text report detailing found model filenames alongside their associated Node Class Type and Node ID.
* **Use Case**: Auditing complex workflows to see exactly which .safetensors checkpoints or Loras are being called, debugging missing model dependencies, or inventorying resources used in shared JSON schemas.

## 🚀 Installation

1. **Clone the repository** into your `ComfyUI/custom_nodes/` folder
```bash
git clone https://github.com/The3MinuteNode/T3MN-Comfy
```

2. **ExifTool Dependency:** This toolkit includes auto downloading ExifTool to the custom node's folder

3. **Restart ComfyUI**
