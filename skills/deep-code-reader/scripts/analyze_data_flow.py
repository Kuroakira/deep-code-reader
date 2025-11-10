#!/usr/bin/env python3
"""
Data Flow Analyzer

Traces data flow through a codebase to understand how data moves between components.
Useful for understanding authentication flows, data processing pipelines, etc.
"""

import ast
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque


class DataFlowAnalyzer:
    """Analyze data flow through Python code"""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.functions = {}  # func_name -> {file, params, returns, calls}
        self.call_graph = defaultdict(list)  # caller -> [callees]
        self.data_flows = defaultdict(list)  # variable -> [functions that use it]
        
    def analyze(self):
        """Analyze all Python files in the codebase"""
        print(f"Analyzing data flow in: {self.root_path}")
        
        for py_file in self.root_path.rglob("*.py"):
            if self._should_skip(py_file):
                continue
            self.analyze_file(py_file)
        
        return self.get_results()
    
    def _should_skip(self, path: Path) -> bool:
        """Skip test files and common directories"""
        skip_patterns = ['test_', '_test.', 'tests/', '__pycache__', 'venv/', 'node_modules/']
        return any(pattern in str(path) for pattern in skip_patterns)
    
    def analyze_file(self, file_path: Path):
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))
            
            visitor = FunctionVisitor(str(file_path))
            visitor.visit(tree)
            
            # Merge results
            self.functions.update(visitor.functions)
            
            for caller, callees in visitor.call_graph.items():
                self.call_graph[caller].extend(callees)
                
        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")
    
    def trace_flow(self, start_function: str, max_depth: int = 5) -> Dict:
        """Trace data flow starting from a specific function"""
        print(f"Tracing flow from: {start_function}")
        
        visited = set()
        flow_tree = {'function': start_function, 'calls': []}
        
        def _trace_recursive(func_name: str, depth: int, parent_node: Dict):
            if depth >= max_depth or func_name in visited:
                return
            
            visited.add(func_name)
            
            callees = self.call_graph.get(func_name, [])
            for callee in callees:
                callee_node = {'function': callee, 'calls': []}
                parent_node['calls'].append(callee_node)
                _trace_recursive(callee, depth + 1, callee_node)
        
        _trace_recursive(start_function, 0, flow_tree)
        
        return flow_tree
    
    def find_authentication_flow(self) -> List[str]:
        """Identify potential authentication-related functions"""
        auth_keywords = ['auth', 'login', 'token', 'verify', 'authenticate', 'session']
        
        auth_functions = []
        for func_name in self.functions.keys():
            if any(keyword in func_name.lower() for keyword in auth_keywords):
                auth_functions.append(func_name)
        
        return sorted(auth_functions)
    
    def find_data_processing_flow(self) -> List[str]:
        """Identify data processing pipeline functions"""
        process_keywords = ['process', 'transform', 'parse', 'validate', 'sanitize', 'format']
        
        process_functions = []
        for func_name in self.functions.keys():
            if any(keyword in func_name.lower() for keyword in process_keywords):
                process_functions.append(func_name)
        
        return sorted(process_functions)
    
    def get_results(self) -> Dict:
        """Get structured analysis results"""
        return {
            'functions': self.functions,
            'call_graph': dict(self.call_graph),
            'summary': {
                'total_functions': len(self.functions),
                'total_calls': sum(len(v) for v in self.call_graph.values())
            },
            'patterns': {
                'authentication_functions': self.find_authentication_flow(),
                'data_processing_functions': self.find_data_processing_flow()
            }
        }


class FunctionVisitor(ast.NodeVisitor):
    """AST visitor to extract function information and call graph"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.functions = {}
        self.call_graph = defaultdict(list)
        self.current_function = None
    
    def visit_FunctionDef(self, node):
        """Visit function definition"""
        func_name = node.name
        
        # Extract parameters
        params = [arg.arg for arg in node.args.args]
        
        # Extract return type hint if available
        returns = None
        if node.returns:
            returns = ast.unparse(node.returns)
        
        # Store function info
        self.functions[func_name] = {
            'file': self.filename,
            'params': params,
            'returns': returns,
            'line': node.lineno,
            'decorators': [ast.unparse(dec) for dec in node.decorator_list]
        }
        
        # Track current function for call analysis
        prev_function = self.current_function
        self.current_function = func_name
        
        # Visit function body
        self.generic_visit(node)
        
        self.current_function = prev_function
    
    def visit_Call(self, node):
        """Visit function call"""
        if self.current_function:
            # Get called function name
            called_func = None
            
            if isinstance(node.func, ast.Name):
                called_func = node.func.id
            elif isinstance(node.func, ast.Attribute):
                called_func = node.func.attr
            
            if called_func:
                self.call_graph[self.current_function].append(called_func)
        
        self.generic_visit(node)


class FlowDiagramGenerator:
    """Generate flow diagrams in various formats"""
    
    def __init__(self, analysis_results: Dict):
        self.results = analysis_results
    
    def generate_mermaid_flowchart(self, flow_tree: Dict) -> str:
        """Generate Mermaid flowchart from flow tree"""
        lines = ["flowchart TD"]
        
        node_counter = [0]
        
        def _add_nodes(node: Dict, parent_id: str = None):
            node_counter[0] += 1
            node_id = f"node{node_counter[0]}"
            func_name = node['function']
            
            lines.append(f"    {node_id}[\"{func_name}\"]")
            
            if parent_id:
                lines.append(f"    {parent_id} --> {node_id}")
            
            for child in node.get('calls', []):
                _add_nodes(child, node_id)
        
        _add_nodes(flow_tree)
        
        return "\n".join(lines)
    
    def generate_call_graph_mermaid(self, functions: List[str] = None, max_nodes: int = 20) -> str:
        """Generate Mermaid graph of function calls"""
        lines = ["graph LR"]
        
        call_graph = self.results.get('call_graph', {})
        
        # Filter to specific functions or top functions
        if functions:
            relevant_funcs = functions
        else:
            # Get functions with most calls
            func_call_counts = {f: len(calls) for f, calls in call_graph.items()}
            relevant_funcs = sorted(func_call_counts.keys(), 
                                   key=lambda f: func_call_counts[f], 
                                   reverse=True)[:max_nodes]
        
        added_edges = set()
        
        for func in relevant_funcs:
            callees = call_graph.get(func, [])
            for callee in callees[:5]:  # Limit callees per function
                edge = (func, callee)
                if edge not in added_edges:
                    lines.append(f"    {self._sanitize(func)} --> {self._sanitize(callee)}")
                    added_edges.add(edge)
        
        return "\n".join(lines)
    
    def _sanitize(self, name: str) -> str:
        """Sanitize name for Mermaid"""
        return name.replace('.', '_').replace('-', '_')


def main():
    parser = argparse.ArgumentParser(description='Analyze data flow in codebase')
    parser.add_argument('path', help='Path to codebase')
    parser.add_argument('--trace', help='Function name to trace flow from')
    parser.add_argument('--depth', type=int, default=5, help='Max trace depth')
    parser.add_argument('--output', default='dataflow', help='Output file prefix')
    parser.add_argument('--pattern', choices=['auth', 'data', 'all'], default='all',
                        help='Identify specific patterns')
    
    args = parser.parse_args()
    
    # Analyze codebase
    analyzer = DataFlowAnalyzer(args.path)
    results = analyzer.analyze()
    
    print(f"\n📊 Analysis complete:")
    print(f"  Functions found: {results['summary']['total_functions']}")
    print(f"  Total function calls: {results['summary']['total_calls']}")
    
    # Save full results
    json_file = f"{args.output}_analysis.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Full analysis: {json_file}")
    
    # Generate diagrams
    diagram_gen = FlowDiagramGenerator(results)
    
    # Trace specific function if requested
    if args.trace:
        flow_tree = analyzer.trace_flow(args.trace, max_depth=args.depth)
        
        # Generate flowchart
        flowchart = diagram_gen.generate_mermaid_flowchart(flow_tree)
        flowchart_file = f"{args.output}_trace_{args.trace}.mmd"
        with open(flowchart_file, 'w') as f:
            f.write(flowchart)
        print(f"✅ Flow trace diagram: {flowchart_file}")
        
        # Save flow tree
        tree_file = f"{args.output}_trace_{args.trace}.json"
        with open(tree_file, 'w') as f:
            json.dump(flow_tree, f, indent=2)
        print(f"✅ Flow tree data: {tree_file}")
    
    # Pattern-specific analysis
    patterns = results.get('patterns', {})
    
    if args.pattern in ['auth', 'all']:
        auth_funcs = patterns.get('authentication_functions', [])
        if auth_funcs:
            print(f"\n🔐 Authentication functions found: {len(auth_funcs)}")
            for func in auth_funcs[:10]:
                print(f"  - {func}")
            
            # Generate auth flow diagram
            auth_graph = diagram_gen.generate_call_graph_mermaid(auth_funcs[:10])
            auth_file = f"{args.output}_auth_flow.mmd"
            with open(auth_file, 'w') as f:
                f.write(auth_graph)
            print(f"✅ Auth flow diagram: {auth_file}")
    
    if args.pattern in ['data', 'all']:
        data_funcs = patterns.get('data_processing_functions', [])
        if data_funcs:
            print(f"\n📊 Data processing functions found: {len(data_funcs)}")
            for func in data_funcs[:10]:
                print(f"  - {func}")
            
            # Generate data processing diagram
            data_graph = diagram_gen.generate_call_graph_mermaid(data_funcs[:10])
            data_file = f"{args.output}_data_flow.mmd"
            with open(data_file, 'w') as f:
                f.write(data_graph)
            print(f"✅ Data flow diagram: {data_file}")


if __name__ == '__main__':
    main()
