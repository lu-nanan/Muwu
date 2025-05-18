import subprocess
import os
import sys

def process_markdown_file(input_path, output_dir):
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist")
        return False
    
    input_dir = os.path.dirname(input_path)
    input_filename = os.path.basename(input_path)
    filename_without_ext = os.path.splitext(input_filename)[0]
    
    if output_dir is None:
        output_dir = input_dir
    
    os.makedirs(output_dir, exist_ok=True)
    
    html_file_path = os.path.join(output_dir, f"{filename_without_ext}.html")
    
    print(f"Processing Markdown file: {input_path}")
    print(f"Output HTML will be saved to: {html_file_path}")
        
    try:
        markdown_cmd = f"markmap \"{input_path}\" --output \"{html_file_path}\" --no-open"
        
        if os.name == 'nt':
            markdown_cmd = f"powershell -Command markmap \"{input_path}\" --output \"{html_file_path}\" --no-open"
        
        print(f"Executing command: {markdown_cmd}")
        
        result = subprocess.run(
            markdown_cmd,
            check=True, 
            text=True, 
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )
        
        print(f"Command return code: {result.returncode}")
        print(f"Command output: {result.stdout}")
        
        if result.returncode != 0:
            print(f"Command error: {result.stderr}")
            return False
        
        print(f"Successfully converted Markdown to HTML mindmap: {html_file_path}")
        return {
            "status": "success",
            "html_path": html_file_path
        }
        
    except subprocess.CalledProcessError as e:
        print(f"Error generating HTML file: {e.output}\n{e.stderr}")
        return {
            "status": "failure",
            "result": f"Error generating HTML file: {e.output}\n{e.stderr}"
        }
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            "status": "failure",
            "result": f"Unexpected error: {str(e)}"
        }

def main():
    input_path = r"F:\大三下学期\移动应用开发\仓库\Muwu\项目计划书s.md"
    output_dir = r"F:\大三下学期\移动应用开发\仓库\Muwu"

    success = process_markdown_file(input_path, output_dir)

    print(success)
    

if __name__ == "__main__":
    main()