#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Context Management Module
"""

from typing import Dict, Any, List, Optional
import time
import uuid

from common.utils.logger import get_logger


class ContextManager:
    """Context Manager Class"""
    
    def __init__(self):
        """Initialize Context Manager"""
        self.logger = get_logger(__name__)
        self.contexts = {}
        self.context_timeout = 3600  # 1 hour
    
    async def create_context(self, session_id: str, user_input: str) -> Dict[str, Any]:
        """Create new execution context
        
        Args:
            session_id: Session ID
            user_input: User input
            
        Returns:
            Created context
        """
        context_id = str(uuid.uuid4())
        
        context = {
            "context_id": context_id,
            "session_id": session_id,
            "user_input": user_input,
            "created_at": time.time(),
            "last_activity": time.time(),
            "status": "active",
            "observations": [],
            "thoughts": [],
            "actions": [],
            "results": [],
            "metadata": {
                "total_iterations": 0,
                "successful_actions": 0,
                "failed_actions": 0
            }
        }
        
        self.contexts[context_id] = context
        
        self.logger.info(f"Created context {context_id} for session {session_id}")
        
        return context
    
    async def get_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Get context by ID
        
        Args:
            context_id: Context ID
            
        Returns:
            Context if found, None otherwise
        """
        context = self.contexts.get(context_id)
        
        if not context:
            return None
        
        # Check if context is expired
        if time.time() - context["last_activity"] > self.context_timeout:
            context["status"] = "expired"
            return context
        
        # Update last activity
        context["last_activity"] = time.time()
        
        return context
    
    async def update_context(self, context_id: str, updates: Dict[str, Any]) -> bool:
        """Update context
        
        Args:
            context_id: Context ID
            updates: Updates to apply
            
        Returns:
            True if successful, False otherwise
        """
        context = await self.get_context(context_id)
        
        if not context:
            return False
        
        # Apply updates
        for key, value in updates.items():
            if key in context and isinstance(context[key], list):
                context[key].append(value)
            else:
                context[key] = value
        
        context["last_activity"] = time.time()
        
        self.logger.debug(f"Updated context {context_id}")
        
        return True
    
    async def add_observation(self, context_id: str, observation: str) -> bool:
        """Add observation to context
        
        Args:
            context_id: Context ID
            observation: Observation string
            
        Returns:
            True if successful, False otherwise
        """
        return await self.update_context(context_id, {
            "observations": observation
        })
    
    async def add_thought(self, context_id: str, thought: str) -> bool:
        """Add thought to context
        
        Args:
            context_id: Context ID
            thought: Thought string
            
        Returns:
            True if successful, False otherwise
        """
        return await self.update_context(context_id, {
            "thoughts": thought
        })
    
    async def add_action(self, context_id: str, action: Dict[str, Any]) -> bool:
        """Add action to context
        
        Args:
            context_id: Context ID
            action: Action dictionary
            
        Returns:
            True if successful, False otherwise
        """
        success = await self.update_context(context_id, {
            "actions": action
        })
        
        if success:
            # Update metadata
            context = await self.get_context(context_id)
            if context:
                if action.get("success", False):
                    context["metadata"]["successful_actions"] += 1
                else:
                    context["metadata"]["failed_actions"] += 1
        
        return success
    
    async def add_result(self, context_id: str, result: Dict[str, Any]) -> bool:
        """Add result to context
        
        Args:
            context_id: Context ID
            result: Result dictionary
            
        Returns:
            True if successful, False otherwise
        """
        return await self.update_context(context_id, {
            "results": result
        })
    
    async def increment_iteration(self, context_id: str) -> bool:
        """Increment iteration counter
        
        Args:
            context_id: Context ID
            
        Returns:
            True if successful, False otherwise
        """
        context = await self.get_context(context_id)
        
        if not context:
            return False
        
        context["metadata"]["total_iterations"] += 1
        context["last_activity"] = time.time()
        
        return True
    
    async def get_context_summary(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Get context summary
        
        Args:
            context_id: Context ID
            
        Returns:
            Context summary if found, None otherwise
        """
        context = await self.get_context(context_id)
        
        if not context:
            return None
        
        return {
            "context_id": context["context_id"],
            "session_id": context["session_id"],
            "user_input": context["user_input"],
            "status": context["status"],
            "total_observations": len(context["observations"]),
            "total_thoughts": len(context["thoughts"]),
            "total_actions": len(context["actions"]),
            "total_results": len(context["results"]),
            "metadata": context["metadata"],
            "duration": time.time() - context["created_at"]
        }
    
    async def cleanup_expired_contexts(self) -> int:
        """Clean up expired contexts
        
        Returns:
            Number of contexts cleaned up
        """
        current_time = time.time()
        expired_contexts = []
        
        for context_id, context in self.contexts.items():
            if current_time - context["last_activity"] > self.context_timeout:
                expired_contexts.append(context_id)
        
        for context_id in expired_contexts:
            del self.contexts[context_id]
        
        if expired_contexts:
            self.logger.info(f"Cleaned up {len(expired_contexts)} expired contexts")
        
        return len(expired_contexts)
    
    async def get_all_contexts(self) -> List[Dict[str, Any]]:
        """Get all active contexts
        
        Returns:
            List of all contexts
        """
        current_time = time.time()
        active_contexts = []
        
        for context in self.contexts.values():
            if current_time - context["last_activity"] <= self.context_timeout:
                active_contexts.append(context)
        
        return active_contexts
    
    async def delete_context(self, context_id: str) -> bool:
        """Delete context
        
        Args:
            context_id: Context ID
            
        Returns:
            True if successful, False otherwise
        """
        if context_id in self.contexts:
            del self.contexts[context_id]
            self.logger.info(f"Deleted context {context_id}")
            return True
        
        return False
    
    async def merge_contexts(self, context_id1: str, context_id2: str) -> Optional[Dict[str, Any]]:
        """Merge two contexts
        
        Args:
            context_id1: First context ID
            context_id2: Second context ID
            
        Returns:
            Merged context if successful, None otherwise
        """
        context1 = await self.get_context(context_id1)
        context2 = await self.get_context(context_id2)
        
        if not context1 or not context2:
            return None
        
        # Merge observations
        context1["observations"].extend(context2["observations"])
        
        # Merge thoughts
        context1["thoughts"].extend(context2["thoughts"])
        
        # Merge actions
        context1["actions"].extend(context2["actions"])
        
        # Merge results
        context1["results"].extend(context2["results"])
        
        # Update metadata
        context1["metadata"]["total_iterations"] += context2["metadata"]["total_iterations"]
        context1["metadata"]["successful_actions"] += context2["metadata"]["successful_actions"]
        context1["metadata"]["failed_actions"] += context2["metadata"]["failed_actions"]
        
        # Delete second context
        await self.delete_context(context_id2)
        
        self.logger.info(f"Merged context {context_id2} into {context_id1}")
        
        return context1
