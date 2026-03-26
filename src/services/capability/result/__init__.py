#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Result Collection Module
"""

import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class ExecutionResult:
    """Execution result class"""
    
    def __init__(
        self,
        result_id: str,
        session_id: str,
        tool_name: str,
        parameters: Dict[str, Any],
        result: Dict[str, Any],
        execution_time: float = 0.0
    ):
        """Initialize execution result
        
        Args:
            result_id: Result ID
            session_id: Session ID
            tool_name: Tool name
            parameters: Tool parameters
            result: Execution result
            execution_time: Execution time in seconds
        """
        self.result_id = result_id
        self.session_id = session_id
        self.tool_name = tool_name
        self.parameters = parameters
        self.result = result
        self.execution_time = execution_time
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "result_id": self.result_id,
            "session_id": self.session_id,
            "tool_name": self.tool_name,
            "parameters": self.parameters,
            "result": self.result,
            "execution_time": self.execution_time,
            "created_at": self.created_at.isoformat()
        }


class ResultCollector:
    """Result Collector for collecting and managing execution results"""
    
    def __init__(self):
        """Initialize result collector"""
        self.results: Dict[str, List[ExecutionResult]] = {}
        self.all_results: Dict[str, ExecutionResult] = {}
        
        logger.info("Result collector initialized")
    
    async def collect(
        self,
        session_id: str,
        result: Dict[str, Any],
        tool_name: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        execution_time: float = 0.0
    ) -> str:
        """Collect execution result
        
        Args:
            session_id: Session ID
            result: Execution result
            tool_name: Tool name
            parameters: Tool parameters
            execution_time: Execution time
            
        Returns:
            Result ID
        """
        result_id = str(uuid.uuid4())
        
        execution_result = ExecutionResult(
            result_id=result_id,
            session_id=session_id,
            tool_name=tool_name or "unknown",
            parameters=parameters or {},
            result=result,
            execution_time=execution_time
        )
        
        # Add to session results
        if session_id not in self.results:
            self.results[session_id] = []
        self.results[session_id].append(execution_result)
        
        # Add to all results
        self.all_results[result_id] = execution_result
        
        logger.info(f"Collected result {result_id} for session {session_id}")
        return result_id
    
    async def get_results(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all results for a session
        
        Args:
            session_id: Session ID
            
        Returns:
            List of results
        """
        if session_id not in self.results:
            return []
        
        return [result.to_dict() for result in self.results[session_id]]
    
    async def get_result(self, result_id: str) -> Optional[Dict[str, Any]]:
        """Get specific result by ID
        
        Args:
            result_id: Result ID
            
        Returns:
            Result data or None
        """
        if result_id in self.all_results:
            return self.all_results[result_id].to_dict()
        return None
    
    async def get_latest_result(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get latest result for a session
        
        Args:
            session_id: Session ID
            
        Returns:
            Latest result or None
        """
        if session_id not in self.results or len(self.results[session_id]) == 0:
            return None
        
        return self.results[session_id][-1].to_dict()
    
    async def get_successful_results(self, session_id: str) -> List[Dict[str, Any]]:
        """Get successful results for a session
        
        Args:
            session_id: Session ID
            
        Returns:
            List of successful results
        """
        if session_id not in self.results:
            return []
        
        return [
            result.to_dict()
            for result in self.results[session_id]
            if result.result.get("status") == "success"
        ]
    
    async def get_failed_results(self, session_id: str) -> List[Dict[str, Any]]:
        """Get failed results for a session
        
        Args:
            session_id: Session ID
            
        Returns:
            List of failed results
        """
        if session_id not in self.results:
            return []
        
        return [
            result.to_dict()
            for result in self.results[session_id]
            if result.result.get("status") == "error"
        ]
    
    async def get_results_by_tool(
        self,
        session_id: str,
        tool_name: str
    ) -> List[Dict[str, Any]]:
        """Get results by tool name
        
        Args:
            session_id: Session ID
            tool_name: Tool name
            
        Returns:
            List of results
        """
        if session_id not in self.results:
            return []
        
        return [
            result.to_dict()
            for result in self.results[session_id]
            if result.tool_name == tool_name
        ]
    
    async def get_statistics(self, session_id: str) -> Dict[str, Any]:
        """Get execution statistics for a session
        
        Args:
            session_id: Session ID
            
        Returns:
            Statistics data
        """
        if session_id not in self.results:
            return {
                "total": 0,
                "successful": 0,
                "failed": 0,
                "total_time": 0.0,
                "average_time": 0.0
            }
        
        results = self.results[session_id]
        total = len(results)
        successful = sum(1 for r in results if r.result.get("status") == "success")
        failed = sum(1 for r in results if r.result.get("status") == "error")
        total_time = sum(r.execution_time for r in results)
        average_time = total_time / total if total > 0 else 0.0
        
        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0.0,
            "total_time": total_time,
            "average_time": average_time
        }
    
    async def clear_results(self, session_id: str):
        """Clear results for a session
        
        Args:
            session_id: Session ID
        """
        if session_id in self.results:
            # Remove from all_results
            for result in self.results[session_id]:
                if result.result_id in self.all_results:
                    del self.all_results[result.result_id]
            
            # Remove from results
            del self.results[session_id]
            
            logger.info(f"Cleared results for session {session_id}")
    
    async def export_results(
        self,
        session_id: str,
        format: str = "json"
    ) -> str:
        """Export results for a session
        
        Args:
            session_id: Session ID
            format: Export format (json, csv)
            
        Returns:
            Exported data
        """
        results = await self.get_results(session_id)
        
        if format == "json":
            return json.dumps(results, indent=2)
        elif format == "csv":
            # Simple CSV export
            lines = ["result_id,tool_name,status,execution_time,created_at"]
            for result in results:
                lines.append(
                    f"{result['result_id']},{result['tool_name']},"
                    f"{result['result'].get('status', 'unknown')},"
                    f"{result['execution_time']},{result['created_at']}"
                )
            return "\n".join(lines)
        else:
            return json.dumps(results, indent=2)
    
    async def get_all_sessions(self) -> List[str]:
        """Get all session IDs
        
        Returns:
            List of session IDs
        """
        return list(self.results.keys())
    
    async def get_total_results_count(self) -> int:
        """Get total number of results
        
        Returns:
            Total count
        """
        return len(self.all_results)
