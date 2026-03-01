# Runtime Logs Tool

Query the three-level runtime logging system for agent execution history.

## Features

- **query_runtime_logs** - Level 1: Run summaries (did the graph succeed?)
- **query_runtime_log_details** - Level 2: Per-node results (which node failed?)
- **query_runtime_log_raw** - Level 3: Full step data (what exactly happened?)

## Overview

The runtime logging system captures agent execution at three levels of detail:

| Level | Tool | Purpose | Data |
|-------|------|---------|------|
| L1 | `query_runtime_logs` | Run summaries | Success/failure, duration, entry point |
| L2 | `query_runtime_log_details` | Node-level results | Per-node outcomes, errors, retries |
| L3 | `query_runtime_log_raw` | Full step data | Complete execution trace, LLM calls |

## Setup

No API keys required. Logs are read from the agent's working directory.

## Usage Examples

### Get Run Summaries (Level 1)
```python
query_runtime_logs(
    agent_work_dir="/path/to/agent/workdir",
    limit=10
)
```

Returns recent runs with:
- Run ID and session ID
- Start/end timestamps
- Success/failure status
- Entry point used
- Duration

### Get Node Details (Level 2)
```python
query_runtime_log_details(
    agent_work_dir="/path/to/agent/workdir",
    run_id="run_20240115_143022"
)
```

Returns per-node execution details:
- Node ID and name
- Execution status (success/failure/skipped)
- Error messages if failed
- Retry count
- Input/output keys

### Get Raw Step Data (Level 3)
```python
query_runtime_log_raw(
    agent_work_dir="/path/to/agent/workdir",
    run_id="run_20240115_143022",
    node_id="gather_info"  # Optional: filter by node
)
```

Returns complete execution trace:
- Every LLM call with prompts/responses
- Tool invocations and results
- State changes
- Timing information

## API Reference

### query_runtime_logs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| agent_work_dir | str | Yes | Path to agent working directory |
| limit | int | No | Max runs to return (default: 20) |
| status | str | No | Filter by "success" or "failure" |

### query_runtime_log_details

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| agent_work_dir | str | Yes | Path to agent working directory |
| run_id | str | Yes | Run ID from Level 1 query |
| node_id | str | No | Filter to specific node |

### query_runtime_log_raw

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| agent_work_dir | str | Yes | Path to agent working directory |
| run_id | str | Yes | Run ID from Level 1 query |
| node_id | str | No | Filter to specific node |
| step_type | str | No | Filter by step type (llm_call, tool_call, etc.) |

## Log Storage Locations
```
{agent_work_dir}/
├── sessions/{session_id}/logs/    # New location
│   ├── summary.json               # L1: Run summary
│   ├── nodes.jsonl                # L2: Node details
│   └── steps.jsonl                # L3: Raw steps
└── runtime_logs/runs/{run_id}/    # Legacy location (deprecated)
```

## Error Handling
```python
{"error": "Agent work directory not found"}
{"error": "Run ID not found: run_xyz"}
{"error": "No logs available for this run"}
{"error": "Failed to parse log file"}
```

## Use Cases

- **Debugging failed runs**: Start with L1 to find failures, drill into L2 for the failing node, then L3 for exact error
- **Performance analysis**: Use L1 durations to identify slow runs, L3 for detailed timing
- **Audit trails**: L3 provides complete execution history for compliance
