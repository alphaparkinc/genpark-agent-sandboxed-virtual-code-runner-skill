import sys, json
from client import AgentSandboxedCodeRunner

def handle_mcp():
    runner = AgentSandboxedCodeRunner()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(runner.run_sandbox_benchmark(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-agent-sandboxed-virtual-code-runner-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "validate_syntax_ast", "description": "Verify code syntax and inspect AST hierarchy.", "inputSchema": {"type": "object", "properties": {"code": {"type": "string"}, "language": {"type": "string"}}}},
                    {"name": "analyze_code_safety", "description": "Scan code for forbidden modules and dangerous syscalls.", "inputSchema": {"type": "object", "properties": {"code": {"type": "string"}, "language": {"type": "string"}}}},
                    {"name": "execute_virtual_sandbox", "description": "Execute code inside an isolated runtime sandbox.", "inputSchema": {"type": "object", "properties": {"code": {"type": "string"}, "language": {"type": "string"}}}},
                    {"name": "run_sandbox_benchmark", "description": "Run security and execution sandbox benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "validate_syntax_ast":
                    res = runner.validate_syntax_ast(args.get("code", ""), args.get("language", "python"))
                elif tname == "analyze_code_safety":
                    res = runner.analyze_code_safety(args.get("code", ""), args.get("language", "python"))
                elif tname == "execute_virtual_sandbox":
                    res = runner.execute_virtual_sandbox(args.get("code", ""), args.get("language", "python"))
                else:
                    res = runner.run_sandbox_benchmark()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
