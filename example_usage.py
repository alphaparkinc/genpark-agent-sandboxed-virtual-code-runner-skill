from client import AgentSandboxedCodeRunner
import json

runner = AgentSandboxedCodeRunner()
print("=== AGENT SANDBOXED CODE RUNNER BENCHMARK ===")
res = runner.run_sandbox_benchmark()
print(json.dumps(res, indent=2))
