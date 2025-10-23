import sys
import os

class ClarityError(Exception):
    """Base class for LanguageNameHere language exceptions"""
    pass

class ClaritySyntaxError(ClarityError):
    """Exception raised for syntax errors in the LanguageNameHere code"""
    def __init__(self, message, line_number, line_content):
        self.message = message
        self.line_number = line_number
        self.line_content = line_content
        super().__init__(f"Syntax error at line {line_number}: {message}\n  {line_content}")

class ClarityRuntimeError(ClarityError):
    """Exception raised for runtime errors in the LanguageNameHere code"""
    pass

sections = {}
variables = {}
block = []
sect_name = ""

def format_error(error_type, message, line_number=None, line_content=None):
    """Format error messages consistently"""
    if line_number is not None and line_content is not None:
        return f"\033[91m{error_type} at line {line_number}:\033[0m {message}\n  \033[93m{line_content}\033[0m"
    return f"\033[91m{error_type}:\033[0m {message}"

def exec_line(s, line_number=None):
    if s.startswith("print"):
        to_print = s.replace("print","").strip()
        if not to_print:
            raise ClaritySyntaxError("Missing argument for print statement", line_number, s)
        
        if to_print.startswith("$"):
            var_name = to_print[1:]
            if var_name not in variables:
                raise ClarityRuntimeError(f"Variable '${var_name}' is not defined")
            print(variables[var_name])
        elif to_print.startswith("\"") and to_print.endswith("\""):
            print(to_print[1:-1])
        else:
            raise ClaritySyntaxError("Print argument must be a variable or string literal", line_number, s)
    elif s.startswith("--"):
        pass
    elif s.startswith("$") and "=" in s:
        s = s[1:]
        name, value = s.split("=")
        name = name.strip()
        value = value.strip()
        if value == "%":
            value = input()
            pass
        ops = ["+","-","*","/","%"]
        for op in ops:
            if op in value:
                lhs, rhs = value.split(op)
                rhs = rhs.strip()
                lhs = lhs.strip()
                if (lhs[1:] in variables):
                    lhs = variables[lhs[1:]]
                    if str(lhs).isdigit():
                        lhs = str(lhs)
                elif (rhs[1:] in variables):
                    rhs = variables[rhs[1:]]
                    if str(rhs).isdigit():
                        rhs = str(rhs)
                elif (lhs[1:] in variables and rhs[1:] in variables):
                    lhs = variables[lhs[1:]]
                    rhs = variables[rhs[1:]]
                    if str(lhs).isdigit() and str(rhs).isdigit():
                        lhs = str(lhs)
                        rhs = str(rhs)
            
                evaluated_value = lhs + op + rhs
                value = str(eval(evaluated_value))
            
        if value.isdigit():
            value = int(value)
        elif value.startswith("\"") and value.endswith("\""):
            value = value[1:-1]
        variables[name] = value
    elif s.startswith("@"):
        sect_name = s[1:]
        exec_sect(sect_name)
    elif s.startswith("if") and "then" in s:
        s = s[3:]
        cond, stmt = s.split("then")
        cond_expr = cond.strip()
        stmt = stmt.strip()
        ops = ["==","!=",">=","<=","<",">"]
        result = False
        for op in ops:
            if op in cond_expr:
                lhs, rhs = cond_expr.split(op)
                rhs = rhs.strip()
                lhs = lhs.strip()
                if lhs.startswith("$"):
                    lhs = str(variables[lhs[1:]])
                if rhs.startswith("$"):
                    rhs = str(variables[rhs[1:]])
                
                # Convert to integers if both are numeric
                if lhs.isdigit() and rhs.isdigit():
                    lhs = int(lhs)
                    rhs = int(rhs)
                
                # Compare directly based on operator
                if op == "==":
                    result = lhs == rhs
                elif op == "!=":
                    result = lhs != rhs
                elif op == ">=":
                    result = lhs >= rhs
                elif op == "<=":
                    result = lhs <= rhs
                elif op == "<":
                    result = lhs < rhs
                elif op == ">":
                    result = lhs > rhs
                break  # Exit loop after finding the operator
        if result:
            exec_line(stmt)
        else:
            pass
    elif s.startswith("exit"):
        exit()

def exec_sect(section_name):
    if section_name not in sections:
        raise ClarityRuntimeError(f"Section '{section_name}' not found")
        
    try:
        for line_num, line in enumerate(sections[section_name], 1):
            try:
                exec_line(line, line_num)
            except ClarityError as e:
                print(format_error("Error", str(e), line_num, line))
                sys.exit(1)
    except Exception as e:
        raise ClarityRuntimeError(f"Error in section '{section_name}': {str(e)}")


def run_file(filename):
    try:
        # Check file extension
        if not filename.lower().endswith('.lnh'):
            print(format_error("Error", "Invalid file extension"))
            print("The Clarity programming language requires files to have a .lnh extension")
            print(f"Please rename '{filename}' to '{filename.rsplit('.', 1)[0]}.lnh'")
            sys.exit(1)
        
        # Check if file exists
        if not os.path.exists(filename):
            print(format_error("Error", f"File not found: {filename}"))
            sys.exit(1)
        
        try:
            with open(filename, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(format_error("Error", f"Failed to read file: {str(e)}"))
            sys.exit(1)
            
        current_section = ""
        block = []
        
        for line_num, line in enumerate(lines, 1):
            try:
                if line.startswith("sect"):
                    if not line[5:].strip():
                        raise ClaritySyntaxError("Missing section name", line_num, line)
                    current_section = line[5:].strip()
                    block = []
                elif line == ";":
                    if current_section:
                        sections[current_section] = block
                        current_section = None
                    else:
                        raise ClaritySyntaxError("Unexpected semicolon outside section", line_num, line)
                elif current_section:
                    block.append(line)
                elif line.startswith("$") and "=" in line:
                    try:
                        exec_line(line, line_num)
                    except ClarityError as e:
                        print(format_error("Error", str(e), line_num, line))
                        sys.exit(1)
                else:
                    raise ClaritySyntaxError("Code must be inside a section", line_num, line)
                    
            except ClarityError as e:
                print(format_error("Error", str(e), line_num, line))
                sys.exit(1)
        
        # Check if any section is unclosed
        if current_section:
            print(format_error("Error", f"Unclosed section: {current_section}"))
            sys.exit(1)
            
        # Execute main section after all sections are processed
        if "main" not in sections:
            print(format_error("Error", "No 'main' section found in the program"))
            sys.exit(1)
            
        try:
            exec_sect("main")
        except ClarityError as e:
            print(format_error("Runtime Error", str(e)))
            sys.exit(1)
            
    except Exception as e:
        print(format_error("Internal Error", f"An unexpected error occurred: {str(e)}"))
        sys.exit(1)

run_file(sys.argv[1])