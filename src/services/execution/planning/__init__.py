#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Task Planning Module
"""

from typing import Dict, Any, List
import uuid

from common.utils.logger import get_logger


class TaskPlanner:
    """Task Planner Class"""
    
    def __init__(self):
        """Initialize Task Planner"""
        self.logger = get_logger(__name__)
        
        # Define task templates for different intents
        self.task_templates = {
            "query": [
                {
                    "type": "search",
                    "description": "Search for relevant information",
                    "priority": 1
                },
                {
                    "type": "analyze",
                    "description": "Analyze search results",
                    "priority": 2
                },
                {
                    "type": "summarize",
                    "description": "Summarize findings",
                    "priority": 3
                }
            ],
            "action": [
                {
                    "type": "validate",
                    "description": "Validate input parameters",
                    "priority": 1
                },
                {
                    "type": "prepare",
                    "description": "Prepare resources",
                    "priority": 2
                },
                {
                    "type": "execute",
                    "description": "Execute main action",
                    "priority": 3
                },
                {
                    "type": "verify",
                    "description": "Verify results",
                    "priority": 4
                }
            ],
            "analysis": [
                {
                    "type": "collect",
                    "description": "Collect data for analysis",
                    "priority": 1
                },
                {
                    "type": "process",
                    "description": "Process and analyze data",
                    "priority": 2
                },
                {
                    "type": "report",
                    "description": "Generate analysis report",
                    "priority": 3
                }
            ],
            "modification": [
                {
                    "type": "locate",
                    "description": "Locate target for modification",
                    "priority": 1
                },
                {
                    "type": "backup",
                    "description": "Create backup if needed",
                    "priority": 2
                },
                {
                    "type": "modify",
                    "description": "Apply modifications",
                    "priority": 3
                },
                {
                    "type": "validate",
                    "description": "Validate modifications",
                    "priority": 4
                }
            ],
            "deletion": [
                {
                    "type": "identify",
                    "description": "Identify items to delete",
                    "priority": 1
                },
                {
                    "type": "confirm",
                    "description": "Confirm deletion targets",
                    "priority": 2
                },
                {
                    "type": "delete",
                    "description": "Perform deletion",
                    "priority": 3
                }
            ],
            "search": [
                {
                    "type": "query",
                    "description": "Formulate search query",
                    "priority": 1
                },
                {
                    "type": "search",
                    "description": "Execute search",
                    "priority": 2
                },
                {
                    "type": "filter",
                    "description": "Filter and rank results",
                    "priority": 3
                }
            ]
        }
    
    async def plan(self, intent: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan tasks based on intent and context
        
        Args:
            intent: Intent analysis result
            context: Execution context
            
        Returns:
            List of planned tasks
        """
        intent_type = intent.get("intent", "unknown")
        entities = intent.get("entities", [])
        parameters = intent.get("parameters", {})
        
        # Get task template for intent
        template = self.task_templates.get(intent_type, self._get_default_template())
        
        # Generate tasks from template
        tasks = []
        for i, task_template in enumerate(template):
            task = {
                "task_id": str(uuid.uuid4()),
                "type": task_template["type"],
                "description": self._customize_description(task_template["description"], entities, parameters),
                "priority": task_template["priority"],
                "status": "pending",
                "dependencies": self._get_dependencies(i, tasks),
                "context": context,
                "entities": entities,
                "parameters": parameters
            }
            tasks.append(task)
        
        # Sort tasks by priority
        tasks.sort(key=lambda x: x["priority"])
        
        self.logger.info(f"Planned {len(tasks)} tasks for intent: {intent_type}")
        
        return tasks
    
    def _get_default_template(self) -> List[Dict[str, Any]]:
        """Get default task template for unknown intent
        
        Returns:
            Default task template
        """
        return [
            {
                "type": "analyze",
                "description": "Analyze request",
                "priority": 1
            },
            {
                "type": "execute",
                "description": "Execute request",
                "priority": 2
            }
        ]
    
    def _customize_description(self, base_description: str, entities: List[Dict[str, Any]], parameters: Dict[str, Any]) -> str:
        """Customize task description based on entities and parameters
        
        Args:
            base_description: Base task description
            entities: Extracted entities
            parameters: Extracted parameters
            
        Returns:
            Customized description
        """
        description = base_description
        
        # Add entity information
        if entities:
            entity_types = list(set([e["type"] for e in entities]))
            description += f" involving {', '.join(entity_types)}"
        
        # Add parameter information
        if parameters.get("files"):
            description += f" for files: {', '.join(parameters['files'])}"
        
        if parameters.get("quoted_strings"):
            description += f" with targets: {', '.join(parameters['quoted_strings'])}"
        
        return description
    
    def _get_dependencies(self, task_index: int, previous_tasks: List[Dict[str, Any]]) -> List[str]:
        """Get task dependencies
        
        Args:
            task_index: Current task index
            previous_tasks: List of previous tasks
            
        Returns:
            List of task IDs that this task depends on
        """
        dependencies = []
        
        # Each task depends on the previous task
        if task_index > 0 and previous_tasks:
            dependencies.append(previous_tasks[-1]["task_id"])
        
        return dependencies
    
    async def update_task_status(self, task_id: str, status: str, result: Any = None):
        """Update task status
        
        Args:
            task_id: Task ID
            status: New status (pending, in_progress, completed, failed)
            result: Task result (if completed or failed)
        """
        # In a real implementation, this would update a database
        self.logger.info(f"Task {task_id} status updated to {status}")
        
        if result:
            self.logger.debug(f"Task result: {result}")
    
    async def get_task_progress(self, task_ids: List[str]) -> Dict[str, Any]:
        """Get progress of multiple tasks
        
        Args:
            task_ids: List of task IDs
            
        Returns:
            Progress information
        """
        # In a real implementation, this would query a database
        total_tasks = len(task_ids)
        completed_tasks = 0
        
        return {
            "total": total_tasks,
            "completed": completed_tasks,
            "in_progress": 0,
            "pending": total_tasks - completed_tasks,
            "progress_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
    
    async def validate_plan(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate task plan
        
        Args:
            tasks: List of tasks to validate
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        # Check for circular dependencies
        if self._has_circular_dependencies(tasks):
            errors.append("Circular dependencies detected in task plan")
        
        # Check for missing dependencies
        for task in tasks:
            for dep_id in task.get("dependencies", []):
                if not any(t["task_id"] == dep_id for t in tasks):
                    warnings.append(f"Task {task['task_id']} depends on non-existent task {dep_id}")
        
        # Check priority ordering
        priorities = [task["priority"] for task in tasks]
        if len(set(priorities)) < len(priorities):
            warnings.append("Some tasks have duplicate priorities")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _has_circular_dependencies(self, tasks: List[Dict[str, Any]]) -> bool:
        """Check if tasks have circular dependencies
        
        Args:
            tasks: List of tasks
            
        Returns:
            True if circular dependencies exist, False otherwise
        """
        # Build dependency graph
        graph = {task["task_id"]: task.get("dependencies", []) for task in tasks}
        
        # Check for cycles using DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                if has_cycle(node):
                    return True
        
        return False
