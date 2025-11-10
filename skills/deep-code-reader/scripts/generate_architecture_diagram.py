#!/usr/bin/env python3
"""
Architecture Diagram Generator

Analyzes a codebase and generates architecture diagrams in multiple formats:
- Mermaid (for easy viewing in markdown)
- draw.io XML (for detailed editing)
"""

import os
import ast
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import xml.etree.ElementTree as ET


class CodebaseAnalyzer:
    """Analyzes codebase structure to extract architectural components"""
    
    def __init__(self, root_path: str, exclude_dirs: Set[str] = None):
        self.root_path = Path(root_path)
        self.exclude_dirs = exclude_dirs or {
            'node_modules', 'venv', '.git', '__pycache__', 
            'dist', 'build', '.next', 'coverage'
        }
        self.modules = {}
        self.dependencies = defaultdict(set)
        self.layers = defaultdict(list)
        
    def analyze(self):
        """Main analysis entry point"""
        print(f"Analyzing codebase at: {self.root_path}")
        
        # Detect project structure
        self.detect_project_structure()
        
        # Analyze Python files
        for py_file in self.root_path.rglob("*.py"):
            if self._should_exclude(py_file):
                continue
            self.analyze_python_file(py_file)
        
        # Analyze JavaScript/TypeScript files
        for js_file in self.root_path.rglob("*.js"):
            if self._should_exclude(js_file):
                continue
            self.analyze_js_file(js_file)
            
        for ts_file in self.root_path.rglob("*.ts"):
            if self._should_exclude(ts_file):
                continue
            self.analyze_js_file(ts_file)
        
        return self.get_analysis_results()
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
        return any(excluded in path.parts for excluded in self.exclude_dirs)
    
    def detect_project_structure(self):
        """Detect common project patterns (MVC, Clean Architecture, etc.)"""
        common_patterns = {
            'controllers': 'Controller Layer',
            'models': 'Model Layer',
            'views': 'View Layer',
            'services': 'Service Layer',
            'repositories': 'Data Access Layer',
            'api': 'API Layer',
            'domain': 'Domain Layer',
            'infrastructure': 'Infrastructure Layer',
            'presentation': 'Presentation Layer',
            'middleware': 'Middleware',
            'utils': 'Utilities',
            'helpers': 'Helpers'
        }
        
        for pattern, layer_name in common_patterns.items():
            pattern_path = self.root_path / pattern
            if pattern_path.exists() and pattern_path.is_dir():
                self.layers[layer_name].append(pattern)
    
    def analyze_python_file(self, file_path: Path):
        """Analyze Python file for imports and structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            module_name = self._get_module_name(file_path)
            imports = self._extract_imports(tree)
            
            self.modules[module_name] = {
                'path': str(file_path),
                'type': 'python',
                'imports': imports
            }
            
            # Build dependency graph
            for imp in imports:
                if imp.startswith('.'):  # Relative import
                    continue
                self.dependencies[module_name].add(imp.split('.')[0])
                
        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")
    
    def analyze_js_file(self, file_path: Path):
        """Analyze JavaScript/TypeScript file for imports"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            module_name = self._get_module_name(file_path)
            imports = self._extract_js_imports(content)
            
            self.modules[module_name] = {
                'path': str(file_path),
                'type': 'javascript',
                'imports': imports
            }
            
            # Build dependency graph
            for imp in imports:
                if imp.startswith('.') or imp.startswith('/'):
                    continue
                self.dependencies[module_name].add(imp.split('/')[0])
                
        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")
    
    def _get_module_name(self, file_path: Path) -> str:
        """Get module name from file path"""
        rel_path = file_path.relative_to(self.root_path)
        return str(rel_path.with_suffix('')).replace(os.sep, '.')
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract imports from Python AST"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports
    
    def _extract_js_imports(self, content: str) -> List[str]:
        """Extract imports from JavaScript/TypeScript content"""
        imports = []
        import re
        
        # Match: import ... from '...'
        import_pattern = r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]"
        imports.extend(re.findall(import_pattern, content))
        
        # Match: require('...')
        require_pattern = r"require\(['\"]([^'\"]+)['\"]\)"
        imports.extend(re.findall(require_pattern, content))
        
        return imports
    
    def get_analysis_results(self) -> Dict:
        """Get structured analysis results"""
        return {
            'modules': self.modules,
            'dependencies': {k: list(v) for k, v in self.dependencies.items()},
            'layers': dict(self.layers),
            'summary': {
                'total_modules': len(self.modules),
                'total_dependencies': sum(len(v) for v in self.dependencies.values()),
                'identified_layers': len(self.layers)
            }
        }


class MermaidGenerator:
    """Generate Mermaid diagrams from analysis results"""
    
    def __init__(self, analysis_results: Dict):
        self.results = analysis_results
    
    def generate_architecture_diagram(self) -> str:
        """Generate high-level architecture diagram"""
        lines = ["graph TB"]
        lines.append("    %% Architecture Overview")
        lines.append("")
        
        # Add layers
        layers = self.results.get('layers', {})
        for layer_name, directories in layers.items():
            node_id = self._sanitize_id(layer_name)
            lines.append(f"    {node_id}[{layer_name}]")
        
        # Add connections between layers
        layer_connections = self._infer_layer_connections(layers)
        for source, target in layer_connections:
            lines.append(f"    {self._sanitize_id(source)} --> {self._sanitize_id(target)}")
        
        return "\n".join(lines)
    
    def generate_dependency_graph(self, max_nodes: int = 20) -> str:
        """Generate module dependency graph"""
        lines = ["graph LR"]
        lines.append("    %% Module Dependencies")
        lines.append("")
        
        # Get top modules by dependency count
        deps = self.results.get('dependencies', {})
        top_modules = sorted(deps.keys(), key=lambda k: len(deps[k]), reverse=True)[:max_nodes]
        
        for module in top_modules:
            module_deps = deps[module]
            for dep in list(module_deps)[:5]:  # Limit to 5 deps per module
                source_id = self._sanitize_id(module.split('.')[-1])
                target_id = self._sanitize_id(dep)
                lines.append(f"    {source_id} --> {target_id}")
        
        return "\n".join(lines)
    
    def _sanitize_id(self, name: str) -> str:
        """Sanitize name for use as Mermaid node ID"""
        return name.replace(' ', '_').replace('-', '_').replace('.', '_')
    
    def _infer_layer_connections(self, layers: Dict) -> List[Tuple[str, str]]:
        """Infer typical connections between architectural layers"""
        connections = []
        layer_order = [
            'Presentation Layer', 'API Layer', 'Controller Layer',
            'Service Layer', 'Domain Layer', 'Data Access Layer',
            'Infrastructure Layer'
        ]
        
        present_layers = [l for l in layer_order if l in layers]
        for i in range(len(present_layers) - 1):
            connections.append((present_layers[i], present_layers[i + 1]))
        
        return connections


class DrawIOGenerator:
    """Generate draw.io XML diagrams"""
    
    def __init__(self, analysis_results: Dict):
        self.results = analysis_results
        self.cell_id = 0
    
    def generate_architecture_diagram(self) -> str:
        """Generate draw.io XML for architecture diagram"""
        # Create root mxfile element
        mxfile = ET.Element('mxfile', {
            'host': 'app.diagrams.net',
            'modified': '2025-01-01T00:00:00.000Z',
            'agent': 'Claude Deep Code Reader',
            'version': '1.0'
        })
        
        diagram = ET.SubElement(mxfile, 'diagram', {
            'id': 'architecture',
            'name': 'Architecture Overview'
        })
        
        mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', {
            'dx': '1422',
            'dy': '794',
            'grid': '1',
            'gridSize': '10',
            'guides': '1'
        })
        
        root = ET.SubElement(mxGraphModel, 'root')
        
        # Add default parent cells
        ET.SubElement(root, 'mxCell', {'id': '0'})
        ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
        
        # Add layer boxes
        layers = self.results.get('layers', {})
        y_offset = 50
        for layer_name in layers.keys():
            self._add_rectangle(root, layer_name, 100, y_offset, 200, 80)
            y_offset += 120
        
        # Convert to string
        return ET.tostring(mxfile, encoding='unicode', method='xml')
    
    def _add_rectangle(self, parent, label: str, x: int, y: int, width: int, height: int):
        """Add a rectangle to the diagram"""
        cell_id = self._get_next_id()
        
        cell = ET.SubElement(parent, 'mxCell', {
            'id': cell_id,
            'value': label,
            'style': 'rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;',
            'vertex': '1',
            'parent': '1'
        })
        
        ET.SubElement(cell, 'mxGeometry', {
            'x': str(x),
            'y': str(y),
            'width': str(width),
            'height': str(height),
            'as': 'geometry'
        })
    
    def _get_next_id(self) -> str:
        """Get next unique cell ID"""
        self.cell_id += 1
        return f'cell_{self.cell_id}'


def main():
    parser = argparse.ArgumentParser(description='Generate architecture diagrams from codebase')
    parser.add_argument('path', help='Path to codebase root')
    parser.add_argument('--format', choices=['mermaid', 'drawio', 'both'], default='both',
                        help='Output format')
    parser.add_argument('--output', default='architecture', help='Output file prefix')
    parser.add_argument('--type', choices=['architecture', 'dependencies', 'both'], default='architecture',
                        help='Diagram type')
    
    args = parser.parse_args()
    
    # Analyze codebase
    analyzer = CodebaseAnalyzer(args.path)
    results = analyzer.analyze()
    
    print(f"\nAnalysis complete:")
    print(f"  Total modules: {results['summary']['total_modules']}")
    print(f"  Identified layers: {results['summary']['identified_layers']}")
    
    # Generate diagrams
    if args.format in ['mermaid', 'both']:
        mermaid_gen = MermaidGenerator(results)
        
        if args.type in ['architecture', 'both']:
            arch_diagram = mermaid_gen.generate_architecture_diagram()
            output_file = f"{args.output}_architecture.mmd"
            with open(output_file, 'w') as f:
                f.write(arch_diagram)
            print(f"\n✅ Mermaid architecture diagram: {output_file}")
        
        if args.type in ['dependencies', 'both']:
            dep_diagram = mermaid_gen.generate_dependency_graph()
            output_file = f"{args.output}_dependencies.mmd"
            with open(output_file, 'w') as f:
                f.write(dep_diagram)
            print(f"✅ Mermaid dependency diagram: {output_file}")
    
    if args.format in ['drawio', 'both']:
        drawio_gen = DrawIOGenerator(results)
        arch_xml = drawio_gen.generate_architecture_diagram()
        output_file = f"{args.output}_architecture.drawio"
        with open(output_file, 'w') as f:
            f.write(arch_xml)
        print(f"✅ draw.io diagram: {output_file}")
    
    # Save analysis JSON
    json_file = f"{args.output}_analysis.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✅ Analysis JSON: {json_file}")


if __name__ == '__main__':
    main()
