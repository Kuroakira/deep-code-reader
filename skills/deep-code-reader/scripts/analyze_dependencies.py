#!/usr/bin/env python3
"""
Dependency Analyzer

Analyzes and visualizes dependencies between modules, packages, and external libraries.
Helps understand coupling, circular dependencies, and overall system structure.
"""

import ast
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class DependencyAnalyzer:
    """Analyze dependencies in a codebase"""
    
    def __init__(self, root_path: str, exclude_dirs: Set[str] = None):
        self.root_path = Path(root_path)
        self.exclude_dirs = exclude_dirs or {
            'node_modules', 'venv', '.git', '__pycache__',
            'dist', 'build', 'coverage', '.pytest_cache'
        }
        
        self.module_deps = defaultdict(set)  # module -> set of dependencies
        self.external_deps = defaultdict(int)  # external package -> usage count
        self.circular_deps = []
        self.package_structure = {}
        
    def analyze(self):
        """Perform full dependency analysis"""
        print(f"Analyzing dependencies in: {self.root_path}")
        
        # Analyze Python files
        for py_file in self.root_path.rglob("*.py"):
            if self._should_exclude(py_file):
                continue
            self.analyze_file(py_file)
        
        # Detect circular dependencies
        self.circular_deps = self._detect_circular_dependencies()
        
        # Analyze package structure
        self.package_structure = self._analyze_package_structure()
        
        return self.get_results()
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
        return any(excluded in path.parts for excluded in self.exclude_dirs)
    
    def analyze_file(self, file_path: Path):
        """Analyze imports in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            module_name = self._get_module_name(file_path)
            imports = self._extract_imports(tree)
            
            for imp in imports:
                if self._is_internal_import(imp):
                    # Internal dependency
                    self.module_deps[module_name].add(imp)
                else:
                    # External dependency
                    external_pkg = imp.split('.')[0]
                    self.external_deps[external_pkg] += 1
                    
        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")
    
    def _get_module_name(self, file_path: Path) -> str:
        """Convert file path to module name"""
        try:
            rel_path = file_path.relative_to(self.root_path)
            return str(rel_path.with_suffix('')).replace('/', '.')
        except ValueError:
            return str(file_path.stem)
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract all imports from AST"""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        return imports
    
    def _is_internal_import(self, import_name: str) -> bool:
        """Check if import is internal to the project"""
        # Check if any module in the project matches this import
        for module in self.module_deps.keys():
            if import_name.startswith(module.split('.')[0]):
                return True
        return False
    
    def _detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies using DFS"""
        visited = set()
        rec_stack = []
        cycles = []
        
        def dfs(module: str):
            visited.add(module)
            rec_stack.append(module)
            
            for dep in self.module_deps.get(module, []):
                if dep not in visited:
                    dfs(dep)
                elif dep in rec_stack:
                    # Found a cycle
                    cycle_start = rec_stack.index(dep)
                    cycle = rec_stack[cycle_start:] + [dep]
                    if cycle not in cycles:
                        cycles.append(cycle)
            
            rec_stack.remove(module)
        
        for module in self.module_deps.keys():
            if module not in visited:
                dfs(module)
        
        return cycles
    
    def _analyze_package_structure(self) -> Dict:
        """Analyze package-level dependencies"""
        package_deps = defaultdict(set)
        
        for module, deps in self.module_deps.items():
            # Get top-level package name
            pkg = module.split('.')[0]
            
            for dep in deps:
                dep_pkg = dep.split('.')[0]
                if dep_pkg != pkg:  # Cross-package dependency
                    package_deps[pkg].add(dep_pkg)
        
        return {pkg: list(deps) for pkg, deps in package_deps.items()}
    
    def get_dependency_metrics(self) -> Dict:
        """Calculate dependency metrics"""
        total_modules = len(self.module_deps)
        
        # Calculate fan-in and fan-out
        fan_out = {mod: len(deps) for mod, deps in self.module_deps.items()}
        
        fan_in = defaultdict(int)
        for deps in self.module_deps.values():
            for dep in deps:
                fan_in[dep] += 1
        
        # Most dependent modules (high fan-out)
        high_fan_out = sorted(fan_out.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Most depended-upon modules (high fan-in)
        high_fan_in = sorted(fan_in.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Most used external packages
        top_external = sorted(self.external_deps.items(), key=lambda x: x[1], reverse=True)[:15]
        
        return {
            'total_modules': total_modules,
            'total_internal_deps': sum(len(deps) for deps in self.module_deps.values()),
            'total_external_deps': len(self.external_deps),
            'circular_dependencies': len(self.circular_deps),
            'high_fan_out': high_fan_out,
            'high_fan_in': high_fan_in,
            'top_external_packages': top_external
        }
    
    def get_results(self) -> Dict:
        """Get structured analysis results"""
        return {
            'module_dependencies': {k: list(v) for k, v in self.module_deps.items()},
            'external_dependencies': dict(self.external_deps),
            'package_structure': self.package_structure,
            'circular_dependencies': self.circular_deps,
            'metrics': self.get_dependency_metrics()
        }


class DependencyDiagramGenerator:
    """Generate dependency diagrams"""
    
    def __init__(self, analysis_results: Dict):
        self.results = analysis_results
    
    def generate_package_dependency_diagram(self) -> str:
        """Generate Mermaid diagram of package-level dependencies"""
        lines = ["graph LR"]
        lines.append("    %% Package Dependencies")
        
        package_struct = self.results.get('package_structure', {})
        
        for pkg, deps in package_struct.items():
            for dep in deps:
                lines.append(f"    {self._sanitize(pkg)} --> {self._sanitize(dep)}")
        
        return "\n".join(lines)
    
    def generate_module_dependency_diagram(self, max_modules: int = 15) -> str:
        """Generate Mermaid diagram of module dependencies"""
        lines = ["graph TB"]
        lines.append("    %% Module Dependencies (Top modules by connections)")
        
        module_deps = self.results.get('module_dependencies', {})
        metrics = self.results.get('metrics', {})
        
        # Get top modules by fan-out
        top_modules = [mod for mod, _ in metrics.get('high_fan_out', [])[:max_modules]]
        
        for module in top_modules:
            deps = module_deps.get(module, [])
            for dep in deps[:5]:  # Limit to 5 deps per module
                if dep in module_deps:  # Only show if it's a known module
                    lines.append(f"    {self._sanitize(module)} --> {self._sanitize(dep)}")
        
        return "\n".join(lines)
    
    def generate_circular_dependency_diagram(self) -> str:
        """Generate diagram highlighting circular dependencies"""
        lines = ["graph LR"]
        lines.append("    %% Circular Dependencies")
        
        circular = self.results.get('circular_dependencies', [])
        
        for cycle_idx, cycle in enumerate(circular[:5]):  # Limit to 5 cycles
            for i in range(len(cycle) - 1):
                source = self._sanitize(cycle[i])
                target = self._sanitize(cycle[i + 1])
                lines.append(f"    {source} -->|cycle {cycle_idx + 1}| {target}")
        
        return "\n".join(lines)
    
    def generate_external_dependencies_chart(self) -> str:
        """Generate bar chart of external dependencies"""
        lines = ["%%{init: {'theme':'base'}}%%"]
        lines.append("pie title External Package Usage")
        
        top_external = self.results.get('metrics', {}).get('top_external_packages', [])
        
        for pkg, count in top_external[:10]:
            lines.append(f'    "{pkg}": {count}')
        
        return "\n".join(lines)
    
    def _sanitize(self, name: str) -> str:
        """Sanitize name for Mermaid"""
        # Shorten long module names
        parts = name.split('.')
        if len(parts) > 2:
            name = f"{parts[0]}...{parts[-1]}"
        return name.replace('.', '_').replace('-', '_')


def main():
    parser = argparse.ArgumentParser(description='Analyze code dependencies')
    parser.add_argument('path', help='Path to codebase')
    parser.add_argument('--output', default='dependencies', help='Output file prefix')
    parser.add_argument('--diagrams', choices=['all', 'package', 'module', 'circular'], 
                        default='all', help='Which diagrams to generate')
    
    args = parser.parse_args()
    
    # Analyze dependencies
    analyzer = DependencyAnalyzer(args.path)
    results = analyzer.analyze()
    
    metrics = results['metrics']
    
    print(f"\n📊 Dependency Analysis:")
    print(f"  Total modules: {metrics['total_modules']}")
    print(f"  Internal dependencies: {metrics['total_internal_deps']}")
    print(f"  External packages: {metrics['total_external_deps']}")
    print(f"  Circular dependencies: {metrics['circular_dependencies']}")
    
    # Save full results
    json_file = f"{args.output}_analysis.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Full analysis: {json_file}")
    
    # Generate diagrams
    diagram_gen = DependencyDiagramGenerator(results)
    
    if args.diagrams in ['all', 'package']:
        pkg_diagram = diagram_gen.generate_package_dependency_diagram()
        pkg_file = f"{args.output}_packages.mmd"
        with open(pkg_file, 'w') as f:
            f.write(pkg_diagram)
        print(f"✅ Package diagram: {pkg_file}")
    
    if args.diagrams in ['all', 'module']:
        mod_diagram = diagram_gen.generate_module_dependency_diagram()
        mod_file = f"{args.output}_modules.mmd"
        with open(mod_file, 'w') as f:
            f.write(mod_diagram)
        print(f"✅ Module diagram: {mod_file}")
    
    if args.diagrams in ['all', 'circular'] and metrics['circular_dependencies'] > 0:
        circ_diagram = diagram_gen.generate_circular_dependency_diagram()
        circ_file = f"{args.output}_circular.mmd"
        with open(circ_file, 'w') as f:
            f.write(circ_diagram)
        print(f"✅ Circular dependencies: {circ_file}")
    
    # Print top metrics
    print(f"\n🔝 Top External Packages:")
    for pkg, count in metrics['top_external_packages'][:10]:
        print(f"  {pkg}: {count} uses")
    
    if metrics['circular_dependencies'] > 0:
        print(f"\n⚠️  Warning: {metrics['circular_dependencies']} circular dependencies detected!")
        print("  See the circular dependencies diagram for details.")


if __name__ == '__main__':
    main()
