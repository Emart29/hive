#!/usr/bin/env python3
"""
MCP Integration Examples - Self-Contained
==========================================
This example demonstrates how to integrate MCP servers with agents,
without requiring any pre-built agents in exports/.

Examples:
1. Register MCP server programmatically
2. Use MCP tools in a simple agent
3. Build custom agent with MCP tools

Run with:
    python core/examples/mcp_integration_example.py
"""

import asyncio
import logging
import tempfile
from pathlib import Path

from framework.graph import Goal, NodeSpec, EdgeSpec, GraphSpec, EdgeCondition
from framework.graph.executor import GraphExecutor
from framework.runtime.core import Runtime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def create_simple_agent_graph() -> tuple[GraphSpec, Goal]:
    """
    Create a simple agent graph for demonstrating MCP integration.
    
    This agent will:
    1. Accept a search query
    2. Process it (simple uppercase transformation)
    3. Return result
    
    In a real scenario, you'd use MCP tools here.
    """
    # Define goal with proper structure
    goal = Goal(
        id="search-processor",
        name="Search Query Processor",
        description="Process search queries efficiently",
        success_criteria=[
            {
                "id": "query_processed",
                "description": "Query processed successfully",
                "metric": "custom",
                "target": "any"
            }
        ]
    )
    
    # Define nodes
    processor_node = NodeSpec(
        id="query_processor",
        name="Query Processor",
        description="Process the search query",
        node_type="function",
        function="process_query",
        input_keys=["query"],
        output_keys=["processed_query"]
    )
    
    formatter_node = NodeSpec(
        id="result_formatter",
        name="Result Formatter",
        description="Format the final result",
        node_type="function",
        function="format_result",
        input_keys=["processed_query"],
        output_keys=["final_result"]
    )
    
    # Define edges
    edges = [
        EdgeSpec(
            id="process-to-format",
            source="query_processor",
            target="result_formatter",
            condition=EdgeCondition.ON_SUCCESS
        )
    ]
    
    # Create graph
    graph = GraphSpec(
        id="mcp-demo-agent",
        goal_id="search-processor",
        entry_node="query_processor",
        terminal_nodes=["result_formatter"],
        nodes=[processor_node, formatter_node],
        edges=edges
    )
    
    return graph, goal


async def example_1_basic_mcp_registration():
    """
    Example 1: Register MCP server programmatically
    
    This shows how to register an MCP server with your agent runtime.
    Note: Actual MCP tools integration requires the tools package.
    """
    logger.info("\n" + "="*60)
    logger.info("Example 1: Basic MCP Server Registration")
    logger.info("="*60 + "\n")
    
    # Create runtime with temporary storage
    storage_path = Path(tempfile.mkdtemp())
    runtime = Runtime(storage_path=storage_path)
    
    # Create simple agent
    graph, goal = create_simple_agent_graph()
    
    logger.info("✓ Agent graph created")
    logger.info("✓ Runtime initialized")
    
    # Note: To actually register MCP tools, you would do:
    # runtime.register_mcp_server(
    #     name="tools",
    #     transport="stdio",
    #     command="python",
    #     args=["-m", "aden_tools.mcp_server", "--stdio"]
    # )
    
    logger.info("\nMCP Server Registration:")
    logger.info("  • Transport: stdio")
    logger.info("  • Command: python -m aden_tools.mcp_server --stdio")
    logger.info("  • Status: Example (not actually connected)")
    
    # Execute agent
    logger.info("\n▶ Running agent with sample input...")
    
    # Create executor and register functions
    executor = GraphExecutor(runtime=runtime)
    
    # Register function implementations
    executor.register_function("query_processor", 
                              lambda query: f"PROCESSED: {query.upper()}")
    executor.register_function("result_formatter",
                              lambda processed_query: f"Search completed: {processed_query}")
    
    result = await executor.execute(
        graph=graph,
        goal=goal,
        input_data={"query": "artificial intelligence"}
    )
    
    if result.success:
        logger.info(f"✓ Agent completed successfully")
        logger.info(f"  Result: {result.output.get('final_result', 'No result')}")
    else:
        logger.info(f"✗ Agent failed: {result.error}")


async def example_2_mcp_with_custom_tools():
    """
    Example 2: Custom agent that would use MCP tools
    
    This demonstrates the pattern for building agents that integrate
    with MCP tools for web search, file operations, etc.
    """
    logger.info("\n" + "="*60)
    logger.info("Example 2: Custom Agent with MCP Tools Pattern")
    logger.info("="*60 + "\n")
    
    # Define goal for web research agent
    goal = Goal(
        id="web-researcher",
        name="Web Research Agent",
        description="Search the web and summarize findings",
        success_criteria=[
            {
                "id": "search_completed",
                "description": "Web search completed successfully",
                "metric": "custom",
                "target": "any"
            },
            {
                "id": "summary_generated",
                "description": "Summary generated from results",
                "metric": "custom",
                "target": "any"
            }
        ]
    )
    
    logger.info("Agent Configuration:")
    logger.info(f"  Goal: {goal.description}")
    logger.info(f"  Success Criteria: {len(goal.success_criteria)} criteria defined")
    
    # Define nodes (in real scenario, these would use MCP tools)
    search_node = NodeSpec(
        id="web_searcher",
        name="Web Searcher",
        description="Search the web for information",
        node_type="function",
        function="search_web",
        input_keys=["query"],
        output_keys=["search_results"]
    )
    
    summary_node = NodeSpec(
        id="summarizer",
        name="Summarizer",
        description="Summarize search results",
        node_type="function",
        function="summarize_results",
        input_keys=["search_results"],
        output_keys=["summary"]
    )
    
    edges = [
        EdgeSpec(
            id="search-to-summary",
            source="web_searcher",
            target="summarizer",
            condition=EdgeCondition.ON_SUCCESS
        )
    ]
    
    graph = GraphSpec(
        id="web-research-agent",
        goal_id="web-researcher",
        entry_node="web_searcher",
        terminal_nodes=["summarizer"],
        nodes=[search_node, summary_node],
        edges=edges
    )
    
    logger.info("\nAgent Structure:")
    logger.info(f"  Nodes: {len(graph.nodes)}")
    logger.info(f"    1. web_searcher - Searches the web")
    logger.info(f"    2. summarizer - Summarizes results")
    logger.info(f"  Entry: web_searcher")
    
    # Execute
    logger.info("\n▶ Running agent...")
    
    # Create runtime with temporary storage
    storage_path = Path(tempfile.mkdtemp())
    runtime = Runtime(storage_path=storage_path)
    
    executor = GraphExecutor(runtime=runtime)
    
    # Register mock functions
    def mock_search(query):
        return f"Mock results for: {query}\n1. AI advances in 2026\n2. Machine learning trends\n3. Neural network research"
    
    def mock_summarize(search_results):
        return "Summary: Based on the search, key trends include advances in AI, ML applications, and neural research."
    
    executor.register_function("web_searcher", mock_search)
    executor.register_function("summarizer", mock_summarize)
    
    result = await executor.execute(
        graph=graph,
        goal=goal,
        input_data={"query": "latest AI breakthroughs"}
    )
    
    if result.success:
        logger.info(f"✓ Agent completed successfully")
        logger.info(f"\n{result.output.get('summary', 'No summary')}")
    else:
        logger.info(f"✗ Agent failed: {result.error}")


async def example_3_mcp_configuration_pattern():
    """
    Example 3: Show MCP server configuration pattern
    
    This demonstrates how MCP servers would be configured
    in a production agent setup.
    """
    logger.info("\n" + "="*60)
    logger.info("Example 3: MCP Server Configuration Pattern")
    logger.info("="*60 + "\n")
    
    logger.info("MCP Server Configuration (mcp_servers.json):")
    logger.info("")
    logger.info("Example configuration for agent folder:")
    logger.info("""
{
  "tools": {
    "transport": "stdio",
    "command": "python",
    "args": ["-m", "aden_tools.mcp_server", "--stdio"]
  },
  "custom-service": {
    "transport": "http",
    "url": "http://localhost:4001"
  }
}
    """)
    
    logger.info("\nWhen an agent is loaded with this configuration:")
    logger.info("  1. MCP servers are auto-discovered")
    logger.info("  2. Tools are registered automatically")
    logger.info("  3. Agent can use all available tools")
    
    logger.info("\nAvailable MCP Tools (when tools package is registered):")
    logger.info("  • web_search - Search the web")
    logger.info("  • read_file - Read file contents")
    logger.info("  • write_file - Write to files")
    logger.info("  • list_files - List directory contents")
    logger.info("  • execute_command - Run shell commands")
    logger.info("  • And 14 more tools...")


async def main():
    """Run all examples"""
    logger.info("="*60)
    logger.info("MCP Integration Examples - Self-Contained")
    logger.info("="*60)
    logger.info("")
    logger.info("These examples demonstrate MCP integration patterns")
    logger.info("without requiring pre-built agents.")
    logger.info("")
    
    try:
        # Run examples
        await example_1_basic_mcp_registration()
        await example_2_mcp_with_custom_tools()
        await example_3_mcp_configuration_pattern()
        
        logger.info("\n" + "="*60)
        logger.info("Examples Complete!")
        logger.info("="*60)
        logger.info("\nNext Steps:")
        logger.info("  1. Install aden_tools: cd tools && pip install -e .")
        logger.info("  2. Build an agent with Claude Code: /building-agents")
        logger.info("  3. Register MCP tools in your agent")
        logger.info("  4. Use tools like web_search, read_file, etc.")
        logger.info("")
        logger.info("Documentation: See core/MCP_INTEGRATION_GUIDE.md")
        
    except Exception as e:
        logger.error(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())