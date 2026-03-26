#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ReAct Loop Engine
"""

from typing import Dict, Any, List, AsyncGenerator
import asyncio
import json

from common.utils.logger import get_logger
from services.execution.tools import ToolSelector


class ReActEngine:
    """ReAct Loop Engine Class"""
    
    def __init__(self):
        """Initialize ReAct Engine"""
        self.logger = get_logger(__name__)
        self.tool_selector = ToolSelector()
        self.max_iterations = 10
        self.max_thought_length = 500
    
    async def execute(self, tasks: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tasks using ReAct loop
        
        Args:
            tasks: List of tasks to execute
            context: Execution context
            
        Returns:
            Execution result
        """
        results = []
        
        for task in tasks:
            task_result = await self._execute_single_task(task, context)
            results.append(task_result)
        
        return {
            "status": "success",
            "results": results,
            "total_tasks": len(tasks)
        }
    
    async def execute_stream(self, tasks: List[Dict[str, Any]], context: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Execute tasks with streaming output
        
        Args:
            tasks: List of tasks to execute
            context: Execution context
            
        Yields:
            Streaming output chunks
        """
        for i, task in enumerate(tasks):
            yield json.dumps({
                "type": "task_start",
                "task_id": task.get("task_id", i),
                "task_description": task.get("description", "")
            })
            
            async for chunk in self._execute_single_task_stream(task, context):
                yield chunk
            
            yield json.dumps({
                "type": "task_complete",
                "task_id": task.get("task_id", i)
            })
        
        yield json.dumps({
            "type": "all_complete",
            "total_tasks": len(tasks)
        })
    
    async def _execute_single_task(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single task using ReAct loop
        
        Args:
            task: Task to execute
            context: Execution context
            
        Returns:
            Task execution result
        """
        iterations = []
        final_answer = None
        
        for iteration in range(self.max_iterations):
            # Thought phase
            thought = await self._think(task, context, iterations)
            iterations.append({
                "iteration": iteration,
                "phase": "thought",
                "content": thought
            })
            
            # Check if we have a final answer
            if self._is_final_answer(thought):
                final_answer = self._extract_answer(thought)
                break
            
            # Action phase
            action = await self._act(thought, task, context)
            iterations.append({
                "iteration": iteration,
                "phase": "action",
                "content": action
            })
            
            # Observation phase
            observation = await self._observe(action, context)
            iterations.append({
                "iteration": iteration,
                "phase": "observation",
                "content": observation
            })
            
            # Update context with observation
            context["observations"].append(observation)
            
            # Check if task is complete
            if self._is_task_complete(observation):
                break
        
        return {
            "task_id": task.get("task_id"),
            "description": task.get("description"),
            "iterations": iterations,
            "final_answer": final_answer,
            "status": "complete" if final_answer else "incomplete"
        }
    
    async def _execute_single_task_stream(self, task: Dict[str, Any], context: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Execute a single task with streaming output
        
        Args:
            task: Task to execute
            context: Execution context
            
        Yields:
            Streaming output chunks
        """
        for iteration in range(self.max_iterations):
            # Thought phase
            thought = await self._think(task, context, context.get("observations", []))
            yield json.dumps({
                "type": "thought",
                "iteration": iteration,
                "content": thought
            })
            
            # Check if we have a final answer
            if self._is_final_answer(thought):
                final_answer = self._extract_answer(thought)
                yield json.dumps({
                    "type": "final_answer",
                    "content": final_answer
                })
                break
            
            # Action phase
            action = await self._act(thought, task, context)
            yield json.dumps({
                "type": "action",
                "iteration": iteration,
                "content": action
            })
            
            # Observation phase
            observation = await self._observe(action, context)
            yield json.dumps({
                "type": "observation",
                "iteration": iteration,
                "content": observation
            })
            
            # Update context with observation
            if "observations" not in context:
                context["observations"] = []
            context["observations"].append(observation)
            
            # Check if task is complete
            if self._is_task_complete(observation):
                yield json.dumps({
                    "type": "task_complete",
                    "iteration": iteration
                })
                break
    
    async def _think(self, task: Dict[str, Any], context: Dict[str, Any], previous_iterations: List[Dict]) -> str:
        """Generate thought for current iteration
        
        Args:
            task: Current task
            context: Execution context
            previous_iterations: Previous iterations
            
        Returns:
            Thought string
        """
        # In a real implementation, this would call the LLM
        # For now, we'll use a simple heuristic approach
        
        task_description = task.get("description", "")
        observations = context.get("observations", [])
        
        if not observations:
            return f"I need to understand the task: {task_description}. Let me think about what tools to use."
        else:
            last_observation = observations[-1]
            return f"Based on the observation: {last_observation}, I should continue with the next step."
    
    async def _act(self, thought: str, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Decide and perform action based on thought
        
        Args:
            thought: Current thought
            task: Current task
            context: Execution context
            
        Returns:
            Action result
        """
        # Select appropriate tool
        tool = await self.tool_selector.select_tool(thought, task, context)
        
        # Execute tool
        if tool:
            action_result = await self.tool_selector.execute_tool(tool, context)
            return {
                "tool": tool.get("name"),
                "action": tool.get("action"),
                "result": action_result
            }
        else:
            return {
                "tool": None,
                "action": "no_action",
                "result": "No suitable tool found"
            }
    
    async def _observe(self, action: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Observe the result of action
        
        Args:
            action: Action that was performed
            context: Execution context
            
        Returns:
            Observation string
        """
        action_result = action.get("result", "")
        return f"Observation: {action_result}"
    
    def _is_final_answer(self, thought: str) -> bool:
        """Check if thought contains final answer
        
        Args:
            thought: Thought string
            
        Returns:
            True if final answer, False otherwise
        """
        # Simple heuristic: check for final answer keywords
        final_keywords = ["final answer", "conclusion", "result", "answer is"]
        return any(keyword in thought.lower() for keyword in final_keywords)
    
    def _extract_answer(self, thought: str) -> str:
        """Extract final answer from thought
        
        Args:
            thought: Thought string
            
        Returns:
            Extracted answer
        """
        # Simple extraction: return the thought itself
        # In a real implementation, this would use more sophisticated parsing
        return thought
    
    def _is_task_complete(self, observation: str) -> bool:
        """Check if task is complete based on observation
        
        Args:
            observation: Observation string
            
        Returns:
            True if task is complete, False otherwise
        """
        # Simple heuristic: check for completion keywords
        completion_keywords = ["complete", "done", "finished", "success"]
        return any(keyword in observation.lower() for keyword in completion_keywords)
