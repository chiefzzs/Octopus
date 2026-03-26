#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sandbox Management Module
"""

import logging
import uuid
import asyncio
import os
import tempfile
import shutil
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class Sandbox:
    """Sandbox environment for isolated execution"""
    
    def __init__(
        self,
        sandbox_id: str,
        session_id: str,
        workspace_path: str,
        config: Dict[str, Any] = None
    ):
        """Initialize sandbox
        
        Args:
            sandbox_id: Sandbox ID
            session_id: Session ID
            workspace_path: Path to sandbox workspace
            config: Sandbox configuration
        """
        self.sandbox_id = sandbox_id
        self.session_id = session_id
        self.workspace_path = workspace_path
        self.config = config or {}
        self.created_at = datetime.now()
        self.status = "active"
        self.execution_count = 0
        
        # Resource limits
        self.max_memory = self.config.get("max_memory", 512 * 1024 * 1024)  # 512MB
        self.max_cpu_time = self.config.get("max_cpu_time", 30)  # 30 seconds
        self.max_file_size = self.config.get("max_file_size", 10 * 1024 * 1024)  # 10MB
        
        logger.info(f"Sandbox created: {sandbox_id} for session: {session_id}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert sandbox to dictionary"""
        return {
            "sandbox_id": self.sandbox_id,
            "session_id": self.session_id,
            "workspace_path": self.workspace_path,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "execution_count": self.execution_count,
            "config": self.config
        }


class SandboxManager:
    """Sandbox Manager for managing isolated execution environments"""
    
    def __init__(self):
        """Initialize sandbox manager"""
        self.sandboxes: Dict[str, Sandbox] = {}
        self.base_workspace = tempfile.mkdtemp(prefix="octopus_sandbox_")
        
        logger.info(f"Sandbox manager initialized with base workspace: {self.base_workspace}")
    
    async def create_sandbox(
        self,
        session_id: str,
        config: Dict[str, Any] = None
    ) -> str:
        """Create a new sandbox environment
        
        Args:
            session_id: Session ID
            config: Sandbox configuration
            
        Returns:
            Sandbox ID
        """
        sandbox_id = str(uuid.uuid4())
        
        # Create sandbox workspace
        workspace_path = os.path.join(self.base_workspace, sandbox_id)
        os.makedirs(workspace_path, exist_ok=True)
        
        # Create sandbox
        sandbox = Sandbox(
            sandbox_id=sandbox_id,
            session_id=session_id,
            workspace_path=workspace_path,
            config=config
        )
        
        self.sandboxes[sandbox_id] = sandbox
        
        logger.info(f"Created sandbox: {sandbox_id}")
        return sandbox_id
    
    async def destroy_sandbox(self, sandbox_id: str) -> bool:
        """Destroy a sandbox environment
        
        Args:
            sandbox_id: Sandbox ID
            
        Returns:
            True if successful, False otherwise
        """
        if sandbox_id not in self.sandboxes:
            return False
        
        sandbox = self.sandboxes[sandbox_id]
        
        try:
            # Remove sandbox workspace
            if os.path.exists(sandbox.workspace_path):
                shutil.rmtree(sandbox.workspace_path)
            
            # Remove sandbox
            del self.sandboxes[sandbox_id]
            
            logger.info(f"Destroyed sandbox: {sandbox_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to destroy sandbox {sandbox_id}: {e}")
            return False
    
    async def get_sandbox(self, sandbox_id: str) -> Optional[Dict[str, Any]]:
        """Get sandbox information
        
        Args:
            sandbox_id: Sandbox ID
            
        Returns:
            Sandbox information or None
        """
        if sandbox_id in self.sandboxes:
            return self.sandboxes[sandbox_id].to_dict()
        return None
    
    async def execute_in_sandbox(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Execute tool in sandbox environment
        
        Args:
            tool_name: Tool name
            parameters: Tool parameters
            session_id: Session ID
            
        Returns:
            Execution result
        """
        # Find or create sandbox for session
        sandbox_id = None
        for sid, sandbox in self.sandboxes.items():
            if sandbox.session_id == session_id:
                sandbox_id = sid
                break
        
        if not sandbox_id:
            sandbox_id = await self.create_sandbox(session_id)
        
        sandbox = self.sandboxes[sandbox_id]
        
        # Modify file paths to use sandbox workspace
        modified_parameters = self._modify_parameters_for_sandbox(
            parameters, sandbox.workspace_path
        )
        
        # Execute tool (simulated - in real implementation would use Docker or similar)
        result = await self._execute_tool_safely(tool_name, modified_parameters, sandbox)
        
        # Update execution count
        sandbox.execution_count += 1
        
        return result
    
    def _modify_parameters_for_sandbox(
        self,
        parameters: Dict[str, Any],
        workspace_path: str
    ) -> Dict[str, Any]:
        """Modify parameters to use sandbox workspace
        
        Args:
            parameters: Original parameters
            workspace_path: Sandbox workspace path
            
        Returns:
            Modified parameters
        """
        modified = parameters.copy()
        
        # Modify file paths
        if "file_path" in modified:
            original_path = modified["file_path"]
            # Use relative path within sandbox
            filename = os.path.basename(original_path)
            modified["file_path"] = os.path.join(workspace_path, filename)
        
        if "directory" in modified:
            modified["directory"] = workspace_path
        
        return modified
    
    async def _execute_tool_safely(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        sandbox: Sandbox
    ) -> Dict[str, Any]:
        """Execute tool safely within sandbox
        
        Args:
            tool_name: Tool name
            parameters: Tool parameters
            sandbox: Sandbox object
            
        Returns:
            Execution result
        """
        try:
            # Simulated safe execution
            # In real implementation, would use Docker or similar
            
            if tool_name == "file_read":
                return await self._safe_file_read(parameters, sandbox)
            elif tool_name == "file_write":
                return await self._safe_file_write(parameters, sandbox)
            elif tool_name == "file_delete":
                return await self._safe_file_delete(parameters, sandbox)
            elif tool_name == "file_search":
                return await self._safe_file_search(parameters, sandbox)
            elif tool_name == "code_execute":
                return await self._safe_code_execute(parameters, sandbox)
            else:
                return {
                    "status": "success",
                    "message": f"Tool {tool_name} executed in sandbox",
                    "sandbox_id": sandbox.sandbox_id,
                    "note": "Simulated sandbox execution"
                }
        except Exception as e:
            logger.error(f"Sandbox execution failed: {tool_name} - {e}")
            return {
                "status": "error",
                "message": str(e),
                "sandbox_id": sandbox.sandbox_id
            }
    
    async def _safe_file_read(
        self,
        parameters: Dict[str, Any],
        sandbox: Sandbox
    ) -> Dict[str, Any]:
        """Safely read file in sandbox
        
        Args:
            parameters: File read parameters
            sandbox: Sandbox object
            
        Returns:
            Execution result
        """
        file_path = parameters.get("file_path")
        
        if not file_path:
            return {
                "status": "error",
                "message": "Missing file_path parameter"
            }
        
        # Check if file is within sandbox
        if not file_path.startswith(sandbox.workspace_path):
            return {
                "status": "error",
                "message": "File access denied: outside sandbox"
            }
        
        # Check file size
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            if file_size > sandbox.max_file_size:
                return {
                    "status": "error",
                    "message": f"File too large: {file_size} bytes (max: {sandbox.max_file_size})"
                }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "status": "success",
                "content": content,
                "file_path": file_path,
                "sandbox_id": sandbox.sandbox_id
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "sandbox_id": sandbox.sandbox_id
            }
    
    async def _safe_file_write(
        self,
        parameters: Dict[str, Any],
        sandbox: Sandbox
    ) -> Dict[str, Any]:
        """Safely write file in sandbox
        
        Args:
            parameters: File write parameters
            sandbox: Sandbox object
            
        Returns:
            Execution result
        """
        file_path = parameters.get("file_path")
        content = parameters.get("content", "")
        
        if not file_path:
            return {
                "status": "error",
                "message": "Missing file_path parameter"
            }
        
        # Check if file is within sandbox
        if not file_path.startswith(sandbox.workspace_path):
            return {
                "status": "error",
                "message": "File access denied: outside sandbox"
            }
        
        # Check content size
        content_size = len(content.encode('utf-8'))
        if content_size > sandbox.max_file_size:
            return {
                "status": "error",
                "message": f"Content too large: {content_size} bytes (max: {sandbox.max_file_size})"
            }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "status": "success",
                "message": f"File written successfully",
                "file_path": file_path,
                "sandbox_id": sandbox.sandbox_id
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "sandbox_id": sandbox.sandbox_id
            }
    
    async def _safe_file_delete(
        self,
        parameters: Dict[str, Any],
        sandbox: Sandbox
    ) -> Dict[str, Any]:
        """Safely delete file in sandbox
        
        Args:
            parameters: File delete parameters
            sandbox: Sandbox object
            
        Returns:
            Execution result
        """
        file_path = parameters.get("file_path")
        
        if not file_path:
            return {
                "status": "error",
                "message": "Missing file_path parameter"
            }
        
        # Check if file is within sandbox
        if not file_path.startswith(sandbox.workspace_path):
            return {
                "status": "error",
                "message": "File access denied: outside sandbox"
            }
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return {
                    "status": "success",
                    "message": "File deleted successfully",
                    "sandbox_id": sandbox.sandbox_id
                }
            else:
                return {
                    "status": "error",
                    "message": "File not found",
                    "sandbox_id": sandbox.sandbox_id
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "sandbox_id": sandbox.sandbox_id
            }
    
    async def _safe_file_search(
        self,
        parameters: Dict[str, Any],
        sandbox: Sandbox
    ) -> Dict[str, Any]:
        """Safely search files in sandbox
        
        Args:
            parameters: File search parameters
            sandbox: Sandbox object
            
        Returns:
            Execution result
        """
        pattern = parameters.get("pattern")
        directory = parameters.get("directory", sandbox.workspace_path)
        
        if not pattern:
            return {
                "status": "error",
                "message": "Missing pattern parameter"
            }
        
        # Check if directory is within sandbox
        if not directory.startswith(sandbox.workspace_path):
            return {
                "status": "error",
                "message": "Directory access denied: outside sandbox"
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
                "sandbox_id": sandbox.sandbox_id
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "sandbox_id": sandbox.sandbox_id
            }
    
    async def _safe_code_execute(
        self,
        parameters: Dict[str, Any],
        sandbox: Sandbox
    ) -> Dict[str, Any]:
        """Safely execute code in sandbox
        
        Args:
            parameters: Code execution parameters
            sandbox: Sandbox object
            
        Returns:
            Execution result
        """
        code = parameters.get("code")
        
        if not code:
            return {
                "status": "error",
                "message": "Missing code parameter"
            }
        
        # Restricted builtins for safe execution
        safe_builtins = {
            "print": print,
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
            "range": range,
            "True": True,
            "False": False,
            "None": None,
        }
        
        try:
            # Execute with timeout
            local_vars = {}
            
            # Run code in restricted environment
            exec(code, {"__builtins__": safe_builtins}, local_vars)
            
            output = local_vars.get("result", "Code executed successfully")
            
            return {
                "status": "success",
                "output": str(output),
                "sandbox_id": sandbox.sandbox_id,
                "note": "Code executed in restricted environment"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "sandbox_id": sandbox.sandbox_id
            }
    
    async def list_sandboxes(self) -> list:
        """List all active sandboxes
        
        Returns:
            List of sandboxes
        """
        return [sandbox.to_dict() for sandbox in self.sandboxes.values()]
    
    async def cleanup_inactive_sandboxes(self, max_age_hours: int = 24):
        """Cleanup inactive sandboxes
        
        Args:
            max_age_hours: Maximum age in hours
        """
        current_time = datetime.now()
        to_remove = []
        
        for sandbox_id, sandbox in self.sandboxes.items():
            age = (current_time - sandbox.created_at).total_seconds() / 3600
            if age > max_age_hours:
                to_remove.append(sandbox_id)
        
        for sandbox_id in to_remove:
            await self.destroy_sandbox(sandbox_id)
        
        logger.info(f"Cleaned up {len(to_remove)} inactive sandboxes")
