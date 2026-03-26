#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tool Selection and Execution Module
"""

from typing import Dict, Any, List, Optional
import asyncio

from common.utils.logger import get_logger


class ToolSelector:
    """Tool Selector Class"""
    
    def __init__(self):
        """Initialize Tool Selector"""
        self.logger = get_logger(__name__)
        
        # Define available tools
        self.available_tools = {
            "file_reader": {
                "name": "file_reader",
                "description": "Read content from a file",
                "action": "read_file",
                "parameters": ["file_path"],
                "capabilities": ["read", "file", "text"]
            },
            "file_writer": {
                "name": "file_writer",
                "description": "Write content to a file",
                "action": "write_file",
                "parameters": ["file_path", "content"],
                "capabilities": ["write", "create", "file", "text"]
            },
            "file_searcher": {
                "name": "file_searcher",
                "description": "Search for files in a directory",
                "action": "search_files",
                "parameters": ["directory", "pattern"],
                "capabilities": ["search", "find", "file", "directory"]
            },
            "code_executor": {
                "name": "code_executor",
                "description": "Execute Python code",
                "action": "execute_code",
                "parameters": ["code"],
                "capabilities": ["execute", "run", "code", "python"]
            },
            "web_searcher": {
                "name": "web_searcher",
                "description": "Search the web for information",
                "action": "web_search",
                "parameters": ["query"],
                "capabilities": ["search", "web", "internet", "information"]
            },
            "data_analyzer": {
                "name": "data_analyzer",
                "description": "Analyze data and generate insights",
                "action": "analyze_data",
                "parameters": ["data", "analysis_type"],
                "capabilities": ["analyze", "data", "statistics", "insights"]
            },
            "text_processor": {
                "name": "text_processor",
                "description": "Process and transform text",
                "action": "process_text",
                "parameters": ["text", "operation"],
                "capabilities": ["process", "text", "transform", "format"]
            },
            "api_caller": {
                "name": "api_caller",
                "description": "Make API calls to external services",
                "action": "call_api",
                "parameters": ["url", "method", "data"],
                "capabilities": ["api", "http", "request", "external"]
            }
        }
    
    async def select_tool(self, thought: str, task: Dict[str, Any], context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select appropriate tool based on thought and task
        
        Args:
            thought: Current thought
            task: Current task
            context: Execution context
            
        Returns:
            Selected tool or None
        """
        # Extract keywords from thought
        keywords = self._extract_keywords(thought)
        
        # Extract keywords from task
        task_keywords = self._extract_keywords(task.get("description", ""))
        keywords.extend(task_keywords)
        
        # Score each tool based on keyword matches
        tool_scores = []
        for tool_id, tool_info in self.available_tools.items():
            score = self._calculate_tool_score(keywords, tool_info)
            tool_scores.append((tool_id, score, tool_info))
        
        # Sort by score
        tool_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return best tool if score is above threshold
        if tool_scores and tool_scores[0][1] > 0:
            best_tool_id, score, tool_info = tool_scores[0]
            self.logger.info(f"Selected tool: {best_tool_id} (score: {score})")
            return tool_info
        
        self.logger.warning("No suitable tool found")
        return None
    
    async def execute_tool(self, tool: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute selected tool
        
        Args:
            tool: Tool to execute
            context: Execution context
            
        Returns:
            Execution result
        """
        tool_name = tool.get("name")
        action = tool.get("action")
        
        self.logger.info(f"Executing tool: {tool_name}")
        
        try:
            # Execute based on action type
            if action == "read_file":
                result = await self._execute_read_file(tool, context)
            elif action == "write_file":
                result = await self._execute_write_file(tool, context)
            elif action == "search_files":
                result = await self._execute_search_files(tool, context)
            elif action == "execute_code":
                result = await self._execute_code(tool, context)
            elif action == "web_search":
                result = await self._execute_web_search(tool, context)
            elif action == "analyze_data":
                result = await self._execute_analyze_data(tool, context)
            elif action == "process_text":
                result = await self._execute_process_text(tool, context)
            elif action == "call_api":
                result = await self._execute_call_api(tool, context)
            else:
                result = {
                    "success": False,
                    "error": f"Unknown action: {action}"
                }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Tool execution failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text
        
        Args:
            text: Text to extract keywords from
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction
        # In a real implementation, this would use NLP
        words = text.lower().split()
        keywords = [word for word in words if len(word) > 3]
        return keywords
    
    def _calculate_tool_score(self, keywords: List[str], tool_info: Dict[str, Any]) -> float:
        """Calculate score for tool based on keyword matches
        
        Args:
            keywords: List of keywords
            tool_info: Tool information
            
        Returns:
            Tool score
        """
        score = 0.0
        capabilities = tool_info.get("capabilities", [])
        description = tool_info.get("description", "").lower()
        
        for keyword in keywords:
            # Check if keyword matches any capability
            for capability in capabilities:
                if keyword in capability:
                    score += 1.0
            
            # Check if keyword matches description
            if keyword in description:
                score += 0.5
        
        return score
    
    async def _execute_read_file(self, tool: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file read operation
        
        Args:
            tool: Tool information
            context: Execution context
            
        Returns:
            Execution result
        """
        # In a real implementation, this would actually read a file
        file_path = context.get("parameters", {}).get("files", [""])[0]
        
        return {
            "success": True,
            "action": "read_file",
            "result": f"Content of file: {file_path}",
            "data": "Sample file content..."
        }
    
    async def _execute_write_file(self, tool: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file write operation
        
        Args:
            tool: Tool information
            context: Execution context
            
        Returns:
            Execution result
        """
        # In a real implementation, this would actually write to a file
        file_path = context.get("parameters", {}).get("files", [""])[0]
        
        return {
            "success": True,
            "action": "write_file",
            "result": f"Written to file: {file_path}"
        }
    
    async def _execute_search_files(self, tool: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file search operation
        
        Args:
            tool: Tool information
            context: Execution context
            
        Returns:
            Execution result
        """
        # In a real implementation, this would actually search files
        return {
            "success": True,
            "action": "search_files",
            "result": "Found 3 matching files",
            "files": ["file1.txt", "file2.py", "file3.json"]
        }
    
    async def _execute_code(self, tool: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Python code
        
        Args:
            tool: Tool information
            context: Execution context
            
        Returns:
            Execution result
        """
        # In a real implementation, this would execute code in a sandbox
        code = "print('Hello, World!')"
        
        try:
            # Simple execution (not safe for production)
            output = str(eval(code))
            
            return {
                "success": True,
                "action": "execute_code",
                "result": output
            }
        except Exception as e:
            return {
                "success": False,
                "action": "execute_code",
                "error": str(e)
            }
    
    async def _execute_web_search(self, tool: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute web search
        
        Args:
            tool: Tool information
            context: Execution context
            
        Returns:
            Execution result
        """
        # In a real implementation, this would perform actual web search
        query = context.get("user_input", "")
        
        return {
            "success": True,
            "action": "web_search",
            "result": f"Search results for: {query}",
            "results": [
                {"title": "Result 1", "url": "https://example.com/1"},
                {"title": "Result 2", "url": "https://example.com/2"}
            ]
        }
    
    async def _execute_analyze_data(self, tool: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data analysis
        
        Args:
            tool: Tool information
            context: Execution context
            
        Returns:
            Execution result
        """
        # In a real implementation, this would perform actual data analysis
        return {
            "success": True,
            "action": "analyze_data",
            "result": "Data analysis complete",
            "insights": [
                "Insight 1: Data shows positive trend",
                "Insight 2: Correlation detected between variables"
            ]
        }
    
    async def _execute_process_text(self, tool: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute text processing
        
        Args:
            tool: Tool information
            context: Execution context
            
        Returns:
            Execution result
        """
        # In a real implementation, this would perform actual text processing
        text = context.get("user_input", "")
        
        return {
            "success": True,
            "action": "process_text",
            "result": f"Processed text: {text[:50]}...",
            "processed_text": text.upper()
        }
    
    async def _execute_call_api(self, tool: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API call
        
        Args:
            tool: Tool information
            context: Execution context
            
        Returns:
            Execution result
        """
        # In a real implementation, this would make actual API calls
        return {
            "success": True,
            "action": "call_api",
            "result": "API call successful",
            "response": {"status": "ok", "data": {}}
        }
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools
        
        Returns:
            List of available tools
        """
        return list(self.available_tools.values())
    
    def get_tool_by_name(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get tool by name
        
        Args:
            tool_name: Tool name
            
        Returns:
            Tool information or None
        """
        return self.available_tools.get(tool_name)
