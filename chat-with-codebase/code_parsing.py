import os
import json
import ast
from openai import OpenAI

class CodeAnalyzer(ast.NodeVisitor):
    """
    Custom AST visitor to extract imports, functions, and classes with inline code.
    """
    def __init__(self, code):
        self.code = code.splitlines()  # Split code into lines for extracting specific segments
        self.imports = []
        self.functions = []
        self.classes = []

    def get_code_segment(self, node):
        """Extracts code corresponding to an AST node."""
        start = node.lineno - 1
        end = node.end_lineno
        return "\n".join(self.code[start:end])

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({
                "type": "import",
                "module": alias.name,
                "as": alias.asname,
                "code": self.get_code_segment(node)
            })
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            self.imports.append({
                "type": "from_import",
                "module": module,
                "name": alias.name,
                "as": alias.asname,
                "code": self.get_code_segment(node)
            })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append({
            "type": "function",
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "docstring": ast.get_docstring(node),
            "code": self.get_code_segment(node)
        })
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append({
                    "type": "method",
                    "name": item.name,
                    "args": [arg.arg for arg in item.args.args],
                    "docstring": ast.get_docstring(item),
                    "code": self.get_code_segment(item)
                })
        self.classes.append({
            "type": "class",
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "methods": methods,
            "code": self.get_code_segment(node)
        })
        self.generic_visit(node)


def parse_code(file_path):
    """
    Parse the given Python file and extract entities using AST.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        tree = ast.parse(code)
        analyzer = CodeAnalyzer(code)
        analyzer.visit(tree)

        # Extract remaining inline code (outside of functions/classes)
        used_lines = set(
            line
            for item in analyzer.imports + analyzer.functions + analyzer.classes
            for line in range(item["code"].count("\n") + 1)
        )
        inline_code = "\n".join(
            line for i, line in enumerate(code.splitlines()) if i not in used_lines
        )

        return {
            "imports": analyzer.imports,
            "functions": analyzer.functions,
            "classes": analyzer.classes,
            "inline_code": inline_code.strip() or None
        }
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return {"imports": [], "functions": [], "classes": [], "inline_code": None}


def extract_hierarchy_with_code(root_path, allowed_extensions, include_levels, output_file, summary_flag):
    """
    Traverse the directory and extract a flat structure with code and relationships.
    """
    root_path = os.path.normpath(root_path)
    output_data = []
    print(include_levels)
    for root, _, files in os.walk(root_path):
        # Add folder details (Folders do not have code)
        if "folders" in include_levels:
            folder_name = os.path.basename(root)
            parent_folder = os.path.dirname(root) if root != root_path else None
            print(parent_folder)
            output_data.append({
                "type": "folder",
                "name": folder_name,
                "path": root,
                "parent_name": None,  # Folder has no parent name
                "parent_type": None,  # Folder has no parent type
                "code": None
            })

        # Initialize a place to store imports by file
        file_imports = {}

        for file in files:
            if any(file.endswith(ext) for ext in allowed_extensions):
                file_path = os.path.join(root, file)
                file_parent = root

                # Extract code entities if detailed analysis is included
                code_entities = parse_code(file_path)
                inline_code = code_entities.get("inline_code")
                
                # Collect imports and group by file
                if "imports" in include_levels:
                    if file not in file_imports:
                        file_imports[file] = []
                    file_imports[file].extend(code_entities["imports"])
                    
                # Add file details (files may have inline code)
                if "files" in include_levels:
                    file_summary =  generate_code_summary(inline_code,summary_flag)
                    output_data.append({
                        "type": "file",
                        "name": file,
                        "path": file_path,
                        "parent_name": os.path.basename(file_parent),
                        "parent_type": "folder",
                    })
                    output_data.append({
                        "type": "file_code",
                        "name": "code-" + file,
                        "path": file_path,
                        "parent_name": file,
                        "parent_type": "file",
                        "code": inline_code,  # Include inline code directly under file
    
                    })
                    output_data.append({
                        "type": "summary",
                        "name": "summary-" + file,
                        "path": file_path,
                        "parent_name": file,
                        "parent_type": "file",
                        "code_summary" : file_summary
                    })
                    

                # Add imports grouped by file
                if file in file_imports:
                    for imp in file_imports[file]:
                        output_data.append({
                            "type": imp["type"],
                            "name": imp["module"] if imp["type"] == "import" else imp["name"],
                            "path": file_path,
                            "parent_name": file,
                            "parent_type": "file",
                            "code": imp["code"]
                        })

                # Add functions
                if "functions" in include_levels:
                    for func in code_entities["functions"]:
                        func_summary =  generate_code_summary(func["code"],summary_flag)
                        output_data.append({
                            "type": "function",
                            "name": func["name"],
                            "path": file_path,
                            "parent_name": file,
                            "parent_type": "file",
                            "docstring": func.get("docstring"),
                        })
                        output_data.append({
                        "type": "function_code",
                        "name": "code-" + func["name"],
                        "path": file_path,
                        "parent_name": func["name"],
                        "parent_type": "function",
                        "code": func["code"],  
                       
                        })
                        output_data.append({
                        "type": "summary",
                        "name": "summary-" + func["name"],
                        "path": file_path,
                        "parent_name": func["name"],
                        "parent_type": "function",
                        
                        "code_summary" : func_summary
                        })
                    
               
                if "imports" in include_levels and file in file_imports:
                    for imp in file_imports[file]:
                        output_data.append({
                            "type": imp["type"],
                            "name": imp["module"] if imp["type"] == "import" else imp["name"],
                            "path": file_path,
                            "parent_name": file,
                            "parent_type": "file",
                            "code": imp["code"]
                        })
                
                # Add classes
                if "classes" in include_levels:
                    for cls in code_entities["classes"]:
                        output_data.append({
                            "type": "class",
                            "name": cls["name"],
                            "path": file_path,
                            "parent_name": file,
                            "parent_type": "file",
                           # "code": cls["code"],
                            "docstring": cls.get("docstring"),
                            #"code_summary" : generate_code_summary(cls["code"],summary_flag)
                        })
                        output_data.append({
                            "type": "class_code",
                            "name": "code-" + cls["name"],
                            "path": file_path,
                            "parent_name": cls["name"],
                            "parent_type": "class",
                            "code": cls["code"],
                            "docstring": cls.get("docstring"),
                        })
                        output_data.append({
                            "type": "summary",
                            "name": "summary-" + cls["name"],
                            "path": file_path,
                            "parent_name": cls["name"],
                            "parent_type": "class",
                            
                            "code_summary" : generate_code_summary(cls["code"],summary_flag)
                        })
                        # Add methods within classes
                        if "methods" in include_levels:
                            for method in cls["methods"]:
                                output_data.append({
                                    "type": "method",
                                    "name": method["name"],
                                    "path": file_path,
                                    "parent_name": cls["name"],
                                    "parent_type": "class",
                                    "code": method["code"],
                                    "docstring": method.get("docstring"),
                                   
                                })
                                output_data.append({
                                    "type": "method_code",
                                    "name": "code-" + method["name"],
                                    "path": file_path,
                                    "parent_name": method["name"],
                                    "parent_type": "method",
                                    
                                    "code_summary" : generate_code_summary(method["code"],summary_flag)
                                })

                # Add code (if code exists outside functions/classes)
                if inline_code:
                    output_data.append({
                        "type": "code",
                        "name": file,
                        "parent_name": file,
                        "parent_type": "file",
                        "code": inline_code
                    })

    # Save the data
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(output_data, json_file, indent=4)
        print(f"Data saved to {output_file}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

    return output_data

def generate_code_summary(source_code,summary_flag):
    if summary_flag == 'False':
        return 
    prompt = f"""
    You are a highly skilled software developer and code reviewer. 
    Your task is to provide a concise summary of the following code. 
    Focus on explaining what the code does, its purpose, 
    and any key details about its functionality. 
    Do not include comments or technical jargon that is unnecessary.

    Code:
    {source_code}

    Summary:
    """
    model_name = os.getenv('MODEL_NAME')
    open_ai = os.getenv('OPEN_AI')
    client = OpenAI(
        api_key= open_ai  
    )

    # Define the input messages
    messages = [
        {"role": "system", "content": "You are an AI assistant that summarizes source code."},
        {"role": "user", "content": prompt}
    ]

    # Call the ChatCompletion API
    response = client.chat.completions.create(
        model= model_name, 
        messages=messages,
        #temperature=0.5
    )

    # Extract the assistant's reply
    summary = response.choices[0].message.content
    
    return summary


