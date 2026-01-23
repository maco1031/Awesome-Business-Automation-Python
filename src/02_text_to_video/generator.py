"""
Text-to-Video Generator
=======================
Wrapper script to generate videos using Remotion.
"""

import os
import json
import subprocess
import sys
import shutil

# Path to the inner Remotion app
REMOTION_APP_DIR = os.path.join(os.path.dirname(__file__), "remotion_app")
INPUT_JSON_PATH = os.path.join(REMOTION_APP_DIR, "input.json")

def check_dependencies():
    """Check if node_modules exists, else prompt to install."""
    if not os.path.exists(os.path.join(REMOTION_APP_DIR, "node_modules")):
        print("⚠️  First time setup: Installing Node.js dependencies...")
        try:
            subprocess.check_call(["npm", "install"], cwd=REMOTION_APP_DIR, shell=True)
            print("✅ Dependencies installed.")
        except subprocess.CalledProcessError:
            print("❌ Error: Failed to install dependencies. Make sure Node.js is installed.")
            sys.exit(1)

def generate_video(text, title_color="#333333", bg_color="#ffffff", is_vertical=False):
    """
    1. Write inputs to input.json
    2. Run Remotion render
    3. Move output
    """
    check_dependencies()

    # Prepare input props
    input_data = {
        "text": text,
        "titleColor": title_color,
        "bgColor": bg_color,
        "durationInFrames": 150
    }
    
    props_json = json.dumps(input_data)
    
    # Select composition based on format
    # Select composition based on format
    if is_vertical:
        comp_id = "TerminalVertical" # Default to Terminal for now as it's the requested upgrade
    else:
        comp_id = "HelloWorld"
        
    output_filename = "output_vertical.mp4" if is_vertical else "output_horizontal.mp4"
    
    # Calc duration based on text length (approx 10 chars per sec + buffer)
    duration = max(150, len(text) * 2 + 60)
    input_data["durationInFrames"] = duration
    props_json = json.dumps(input_data)

    output_path = os.path.join(os.getcwd(), output_filename)

    print(f"🎬 Rendering video ({comp_id}) with text length: {len(text)}...")
    
    cmd = [
        "npx", "remotion", "render",
        "src/index.ts",
        comp_id,
        output_path,
        f"--props={props_json}",
        "--overwrite"
    ]

    try:
        subprocess.check_call(cmd, cwd=REMOTION_APP_DIR, shell=True)
        print(f"✅ Video saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Rendering failed: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate text-to-video")
    parser.add_argument("--text", type=str, help="Text to display (use \\n for newlines)")
    parser.add_argument("--props_file", type=str, help="Path to props json file")
    parser.add_argument("--bg", type=str, default="#ffffff", help="Background color hex")
    parser.add_argument("--vertical", action="store_true", help="Generate vertical video (9:16)")
    parser.add_argument("--interactive", action="store_true", help="Use interactive mode")

    args = parser.parse_args()

    if args.props_file:
        # Direct render with file
        comp_id = "TerminalVertical" if args.vertical else "HelloWorld"
        output_filename = "output_vertical.mp4" if args.vertical else "output_horizontal.mp4"
        output_path = os.path.join(os.getcwd(), output_filename)
        props_abs_path = os.path.abspath(args.props_file)
        print(f"🎬 Rendering from file: {props_abs_path}")
        cmd = [
            "npx", "remotion", "render",
            "src/index.ts",
            comp_id,
            output_path,
            f"--props={props_abs_path}",
            "--overwrite"
        ]
        try:
            subprocess.check_call(cmd, cwd=REMOTION_APP_DIR, shell=True)
            print(f"✅ Video saved to: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Rendering failed: {e}")
    elif args.interactive:
        print("--- Text-to-Video Generator ---")
        user_text = input("Enter text (use \\n for new lines): ").replace("\\n", "\n")
        if not user_text:
            user_text = "Hello World"
            
        user_bg = input("Background Color (hex, default #ffffff): ")
        if not user_bg:
            user_bg = "#ffffff"

        format_in = input("Vertical format for Pinterest? (y/n, default n): ").lower()
        vertical = format_in == 'y'

        generate_video(user_text, bg_color=user_bg, is_vertical=vertical)
    else:
        if not args.text:
            print("--- Text-to-Video Generator (Interactive) ---")
            print("Tip: Use --text 'Foo' --vertical to skip prompts.")
            user_text = input("Enter text (use \\n for new lines): ").replace("\\n", "\n")
            if not user_text:
                user_text = "Hello World"
            user_bg = input("Background Color (hex, default #ffffff): ") or "#ffffff"
            format_in = input("Vertical format for Pinterest? (y/n, default n): ").lower()
            generate_video(user_text, bg_color=user_bg, is_vertical=(format_in == 'y'))
        else:
            text_clean = args.text.replace("\\n", "\n")
            generate_video(text_clean, bg_color=args.bg, is_vertical=args.vertical)
