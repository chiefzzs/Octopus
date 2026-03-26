#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tool Execution Module
"""

import logging
import asyncio
import os
import json
from typing import Dict, Any, Optional
import aiohttp
import aiofiles

logger = logging.getLogger(__name__)


class ToolExecutor:
    """Tool Executor for executing various tools"""
    
    def __init__(self):
        """Initialize tool executor"""
        self.execution_history: Dict[str, list] = {}
        
        logger.info("Tool executor initialized")
    
    async def execute(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute a tool
        
        Args:
            tool_name: Tool name
            parameters: Tool parameters
            session_id: Session ID
            
        Returns:
            Execution result
        """
        logger.info(f"Executing tool: {tool_name} with parameters: {parameters}")
        
        try:
            # Execute based on tool name
            if tool_name == "file_read":
                result = await self._execute_file_read(parameters)
            elif tool_name == "file_write":
                result = await self._execute_file_write(parameters)
            elif tool_name == "file_delete":
                result = await self._execute_file_delete(parameters)
            elif tool_name == "file_search":
                result = await self._execute_file_search(parameters)
            elif tool_name == "browser_open":
                result = await self._execute_browser_open(parameters)
            elif tool_name == "browser_click":
                result = await self._execute_browser_click(parameters)
            elif tool_name == "browser_input":
                result = await self._execute_browser_input(parameters)
            elif tool_name == "api_get":
                result = await self._execute_api_get(parameters)
            elif tool_name == "api_post":
                result = await self._execute_api_post(parameters)
            elif tool_name == "code_execute":
                result = await self._execute_code(parameters)
            else:
                result = {
                    "status": "error",
                    "message": f"Unknown tool: {tool_name}"
                }
            
            # Record execution history
            if session_id:
                if session_id not in self.execution_history:
                    self.execution_history[session_id] = []
                self.execution_history[session_id].append({
                    "tool_name": tool_name,
                    "parameters": parameters,
                    "result": result
                })
            
            logger.info(f"Tool execution completed: {tool_name}")
            return result
            
        except Exception as e:
            logger.error(f"Tool execution failed: {tool_name} - {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def _execute_file_read(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file read operation
        
        Args:
            parameters: File read parameters
            
        Returns:
            Execution result
        """
        file_path = parameters.get("file_path")
        encoding = parameters.get("encoding", "utf-8")
        
        if not file_path:
            return {
                "status": "error",
                "message": "Missing file_path parameter"
            }
        
        try:
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "message": f"File not found: {file_path}"
                }
            
            async with aiofiles.open(file_path, mode='r', encoding=encoding) as f:
                content = await f.read()
            
            return {
                "status": "success",
                "content": content,
                "file_path": file_path,
                "size": len(content)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def _execute_file_write(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file write operation
        
        Args:
            parameters: File write parameters
            
        Returns:
            Execution result
        """
        file_path = parameters.get("file_path")
        content = parameters.get("content")
        encoding = parameters.get("encoding", "utf-8")
        
        if not file_path or content is None:
            return {
                "status": "error",
                "message": "Missing file_path or content parameter"
            }
        
        try:
            # Create directory if not exists
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            async with aiofiles.open(file_path, mode='w', encoding=encoding) as f:
                await f.write(content)
            
            return {
                "status": "success",
                "message": f"File written successfully: {file_path}",
                "file_path": file_path,
                "size": len(content)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def _execute_file_delete(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file delete operation
        
        Args:
            parameters: File delete parameters
            
        Returns:
            Execution result
        """
        file_path = parameters.get("file_path")
        
        if not file_path:
            return {
                "status": "error",
                "message": "Missing file_path parameter"
            }
        
        try:
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "message": f"File not found: {file_path}"
                }
            
            os.remove(file_path)
            
            return {
                "status": "success",
                "message": f"File deleted successfully: {file_path}",
                "file_path": file_path
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def _execute_file_search(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file search operation
        
        Args:
            parameters: File search parameters
            
        Returns:
            Execution result
        """
        pattern = parameters.get("pattern")
        directory = parameters.get("directory", ".")
        
        if not pattern:
            return {
                "status": "error",
                "message": "Missing pattern parameter"
            }
        
        try:
            matches = []
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    if pattern in filename:
                        matches.append(os.path.join(root, filename))
            
            return {
                "status": "success",
                "matches": matches,
                "total": len(matches),
                "pattern": pattern,
                "directory": directory
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def _execute_browser_open(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute browser open operation (simulated)
        
        Args:
            parameters: Browser open parameters
            
        Returns:
            Execution result
        """
        url = parameters.get("url")
        
        if not url:
            return {
                "status": "error",
                "message": "Missing url parameter"
            }
        
        # Simulated browser operation
        return {
            "status": "success",
            "message": f"Browser opened URL: {url}",
            "url": url,
            "note": "This is a simulated operation"
        }
    
    async def _execute_browser_click(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute browser click operation (simulated)
        
        Args:
            parameters: Browser click parameters
            
        Returns:
            Execution result
        """
        selector = parameters.get("selector")
        
        if not selector:
            return {
                "status": "error",
                "message": "Missing selector parameter"
            }
        
        # Simulated browser operation
        return {
            "status": "success",
            "message": f"Clicked element: {selector}",
            "selector": selector,
            "note": "This is a simulated operation"
        }
    
    async def _execute_browser_input(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute browser input operation (simulated)
        
        Args:
            parameters: Browser input parameters
            
        Returns:
            Execution result
        """
        selector = parameters.get("selector")
        text = parameters.get("text")
        
        if not selector or text is None:
            return {
                "status": "error",
                "message": "Missing selector or text parameter"
            }
        
        # Simulated browser operation
        return {
            "status": "success",
            "message": f"Input text into element: {selector}",
            "selector": selector,
            "text": text,
            "note": "This is a simulated operation"
        }
    
    async def _execute_api_get(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API GET request
        
        Args:
            parameters: API GET parameters
            
        Returns:
            Execution result
        """
        url = parameters.get("url")
        headers = parameters.get("headers", {})
        
        if not url:
            return {
                "status": "error",
                "message": "Missing url parameter"
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    data = await response.text()
                    
                    return {
                        "status": "success",
                        "status_code": response.status,
                        "data": data,
                        "url": url
                    }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def _execute_api_post(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API POST request
        
        Args:
            parameters: API POST parameters
            
        Returns:
            Execution result
        """
        url = parameters.get("url")
        data = parameters.get("data", {})
        headers = parameters.get("headers", {})
        
        if not url:
            return {
                "status": "error",
                "message": "Missing url parameter"
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as response:
                    response_data = await response.text()
                    
                    return {
                        "status": "success",
                        "status_code": response.status,
                        "data": response_data,
                        "url": url
                    }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def _execute_code(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Python code (restricted)
        
        Args:
            parameters: Code execution parameters
            
        Returns:
            Execution result
        """
        code = parameters.get("code")
        
        if not code:
            return {
                "status": "error",
                "message": "Missing code parameter"
            }
        
        try:
            # Create restricted execution environment
            local_vars = {}
            global_vars = {
                "__builtins__": {
                    "print": print,
                    "len": len,
                    "str": str,
                    "int": int,
                    "float": float,
                    "list": list,
                    "dict": dict,
                    "range": range,
                }
            }
            
            # Execute code in restricted environment
            exec(code, global_vars, local_vars)
            
            # Get output
            output = local_vars.get("result", "Code executed successfully")
            
            return {
                "status": "success",
                "output": str(output),
                "note": "Code executed in restricted environment"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def get_execution_history(self, session_id: str) -> list:
        """Get execution history for a session
        
        Args:
            session_id: Session ID
            
        Returns:
            Execution history
        """
        return self.execution_history.get(session_id, [])
    
    async def clear_execution_history(self, session_id: str):
        """Clear execution history for a session
        
        Args:
            session_id: Session ID
        """
        if session_id in self.execution_history:
            del self.execution_history[session_id]
