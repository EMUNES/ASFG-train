"""
Convert jupyter notebook (.ipynb) to clean python scripts using a top-down
approach - reading the jupyter notebook from top to bottom and deal with
each block, including markdown, plain text and python code.

For markdown blocks:
1. Ignore all markdown. This is the DEFAULT.
2. Convert markdown to python notations (block).

For plain text blocks:
1. Ignore all text. This is the DEFAULT.  
2. Convert plain text to python notations (block or line).

For code blocks: 
1. Keep all block notations but ignore all line notations. This is the default.
2. Keep all notations.
3. Ignore all notations.
4. Ignore or keep all commandline codes as notations.
5. Ignore or keep all jupyter codes as notations.

############
PROGRAM DESIGN:
- As for classes, handle each cell's source content and get formatted output choosed.
- In the main loop, record the output of each cell and separate them with blank line.   
"""

import json

TYPES = ["markdown", "raw", "code"]
CHOICES = [None, "block", "line", "keep"]

# Modify those two lines for input and output path, other modification are not required.
INPUT_FILE_PATH = "./sample.ipynb"
OUTPUT_FILE_PATH = "./test.py"

class Cell(object):
    """
    Exposes APIs to handle content in different cells.
    
    If the handler is passed None, the source content will be ignored.
    
    ############ 
    In each cell, there are five fileds: cell_type, execution_count, metadata, outputs and source.
    
    cell_type: The type of the cell, including "markdown", "raw", "code".
    excution_count: Only exists in code cell.
    metadata: .
    outputs: Only exists in code cell.
    source: Content of the cell.
    
    We only need cell_type and source to handle each cell.
    ############
    
    Attributes:
        output_content(list[str]): Clean content after using handler.
    
    Args:
        cell_type(str): The type of the cell.
        source(list([str])): The source content of the cell.
        handler: The way to handle the content.
    """
    
    output_content = []
    
    def __init__(self, cell_type, source, handler=None) -> None:
        
        self.cell_type = cell_type
        assert cell_type in TYPES, f"!!!Error: Unknown cell type in jupyter. {(TYPES)}"
        
        self.source = source
        self._check_empty()
        
        assert handler in CHOICES, f"!!!Error: Unknown handler.{(CHOICES)}"
        self.handler = handler
        self._check_handler()
                                
    def _check_empty(self):
        if not self.source:
            self.output_content = None
        
    def _check_handler(self):
        if not self.handler:
            self.output_content = None
            
    def _as_block(self):
        self.output_content = ["\"\"\"\n", *self.source, "\n\"\"\""]
            
    def _as_line(self):
        self.output_content = [f"# {line}" for line in self.source]
                    
    def _as_code(self):
        self.output_content = [*self.source]
            
    def handle(self):
        if self.output_content==None:
            return None
        elif self.handler=="block":
            self._as_block()
        elif self.handler=="line":
            self._as_line()
        else:
            self._as_code()
                                
            
class MarkdownCell(Cell):
    """
    Handle Markdown Cell.
    """
        
    def __init__(self, cell_type, source, handler=None) -> None:
        super().__init__(cell_type, source, handler)
        
        self.handle()
        
    
class RawCell(Cell):
    """
    Handle Raw Cell.
    """
    
    def __init__(self, cell_type, source, handler=None) -> None:
        super().__init__(cell_type, source, handler)
        
        self.handle()


class CodeCell(Cell):
    """
    Handle Code Cell.
    
    No need to handle block content, because it usually works as docstring.
    
    Args:
        cmd_handler(None/str): How to handle commamndline code.
        juy_handler(None/str): How to handle jupyter built-in code.
        ntt_handler(None/str): How to handle line notations.
    """
        
    def __init__(self, cell_type, source, cmd_handler=None, juy_handler=None, ntt_handler="keep") -> None:
        super().__init__(cell_type, source, handler="keep")
        self.cmd_handler = cmd_handler
        self.juy_handler = juy_handler
        self.ntt_handler = ntt_handler
        
        self.handle()
        
        self.f_handle()
            
    def _handle_juy_code(self, line, idx):
        if self.juy_handler==None:
            self.output_content[idx] = ""
        if self.juy_handler=="block":
            self.output_content[idx] = f"\n\"\"\"\n{line}\n\"\"\"\n"
        if self.juy_handler=="line":
            self.output_content[idx] = f"#  {line}"
    
    def _handle_cmd_code(self, line, idx):
        if self.cmd_handler==None:
            self.output_content[idx] = ""
        if self.cmd_handler=="block":
            self.output_content[idx] = f"\n\"\"\"\n{line}\n\"\"\"\n"
        if self.cmd_handler=="line":
            self.output_content[idx] = f"#  {line}"
            
    def _handle_notatation(self, line, idx):
        if self.ntt_handler==None:
            self.output_content[idx] = ""

    def f_handle(self):
        for (idx, line) in enumerate(self.output_content):
            if line.lstrip().startswith("!"):
                self._handle_cmd_code(line, idx)
                continue
            elif line.lstrip().startswith("%"):
                self._handle_juy_code(line, idx)
                continue
            elif line.lstrip().startswith("#"):
                self._handle_notatation(line, idx)
        
        self.output_content = [line for line in self.output_content if line != ""]

if __name__ == "__main__":
    
    # Content from reading process for writing.
    content = []
    
    # Read and get each cell's formatted output content.
    with open(INPUT_FILE_PATH, encoding="utf-8") as rf:
        text = json.load(rf) # text is a dict contatining all information in the block
        cells = text["cells"]
        
        for cell in cells:
            cell_type = cell["cell_type"]
            cell_source = cell["source"]
            
            # If the cell is not empty, deal with it.
            if cell_source:
                
                if cell_type == "markdown":
                    cell = MarkdownCell(cell_type, cell_source)
                elif cell_type == "raw":
                    cell = RawCell(cell_type, cell_source)
                else: # It's a code cell.
                    cell = CodeCell(cell_type, cell_source, juy_handler=None, cmd_handler=None, ntt_handler=None)
                
                if cell.output_content:
                    content.append(cell.output_content)
    
    # Write each cell's content and separate them with blank lines. 
    with open(OUTPUT_FILE_PATH, mode="w", encoding="utf-8") as wf:
        for p in content:
            wf.writelines(p)
            wf.writelines(["\n", "\n"])
            
