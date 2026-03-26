#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skill Management Module
"""

import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class Skill:
    """Skill class representing a capability"""
    
    def __init__(
        self,
        skill_id: str,
        name: str,
        description: str,
        category: str,
        version: str = "1.0.0",
        author: str = "unknown",
        tags: List[str] = None,
        dependencies: List[str] = None,
        parameters: Dict[str, Any] = None,
        handler: callable = None
    ):
        """Initialize skill
        
        Args:
            skill_id: Unique skill identifier
            name: Skill name
            description: Skill description
            category: Skill category (file, browser, api, etc.)
            version: Skill version
            author: Skill author
            tags: Skill tags for search
            dependencies: List of dependencies
            parameters: Skill parameters schema
            handler: Skill execution handler
        """
        self.skill_id = skill_id
        self.name = name
        self.description = description
        self.category = category
        self.version = version
        self.author = author
        self.tags = tags or []
        self.dependencies = dependencies or []
        self.parameters = parameters or {}
        self.handler = handler
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.status = "active"
        self.execution_count = 0
        self.success_count = 0
        self.error_count = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary"""
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "author": self.author,
            "tags": self.tags,
            "dependencies": self.dependencies,
            "parameters": self.parameters,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status,
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "error_count": self.error_count
        }
    
    def update_stats(self, success: bool):
        """Update execution statistics
        
        Args:
            success: Whether execution was successful
        """
        self.execution_count += 1
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
        self.updated_at = datetime.now()


class SkillManager:
    """Skill Manager for managing skills lifecycle"""
    
    def __init__(self):
        """Initialize skill manager"""
        self.skills: Dict[str, Skill] = {}
        self.categories: Dict[str, List[str]] = {}
        self.tags_index: Dict[str, List[str]] = {}
        
        # Register default skills
        self._register_default_skills()
        
        logger.info("Skill manager initialized")
    
    def _register_default_skills(self):
        """Register default built-in skills"""
        default_skills = [
            {
                "name": "file_read",
                "description": "Read file content",
                "category": "file",
                "tags": ["file", "read", "io"],
                "parameters": {
                    "file_path": {"type": "string", "required": True},
                    "encoding": {"type": "string", "default": "utf-8"}
                }
            },
            {
                "name": "file_write",
                "description": "Write content to file",
                "category": "file",
                "tags": ["file", "write", "io"],
                "parameters": {
                    "file_path": {"type": "string", "required": True},
                    "content": {"type": "string", "required": True},
                    "encoding": {"type": "string", "default": "utf-8"}
                }
            },
            {
                "name": "file_delete",
                "description": "Delete file",
                "category": "file",
                "tags": ["file", "delete", "io"],
                "parameters": {
                    "file_path": {"type": "string", "required": True}
                }
            },
            {
                "name": "file_search",
                "description": "Search for files",
                "category": "file",
                "tags": ["file", "search", "find"],
                "parameters": {
                    "pattern": {"type": "string", "required": True},
                    "directory": {"type": "string", "default": "."}
                }
            },
            {
                "name": "browser_open",
                "description": "Open URL in browser",
                "category": "browser",
                "tags": ["browser", "web", "url"],
                "parameters": {
                    "url": {"type": "string", "required": True}
                }
            },
            {
                "name": "browser_click",
                "description": "Click element in browser",
                "category": "browser",
                "tags": ["browser", "click", "interaction"],
                "parameters": {
                    "selector": {"type": "string", "required": True}
                }
            },
            {
                "name": "browser_input",
                "description": "Input text in browser",
                "category": "browser",
                "tags": ["browser", "input", "text"],
                "parameters": {
                    "selector": {"type": "string", "required": True},
                    "text": {"type": "string", "required": True}
                }
            },
            {
                "name": "api_get",
                "description": "Make GET API request",
                "category": "api",
                "tags": ["api", "http", "get"],
                "parameters": {
                    "url": {"type": "string", "required": True},
                    "headers": {"type": "object", "default": {}}
                }
            },
            {
                "name": "api_post",
                "description": "Make POST API request",
                "category": "api",
                "tags": ["api", "http", "post"],
                "parameters": {
                    "url": {"type": "string", "required": True},
                    "data": {"type": "object", "default": {}},
                    "headers": {"type": "object", "default": {}}
                }
            },
            {
                "name": "code_execute",
                "description": "Execute Python code",
                "category": "code",
                "tags": ["code", "python", "execute"],
                "parameters": {
                    "code": {"type": "string", "required": True}
                }
            }
        ]
        
        for skill_data in default_skills:
            skill_id = str(uuid.uuid4())
            skill = Skill(
                skill_id=skill_id,
                name=skill_data["name"],
                description=skill_data["description"],
                category=skill_data["category"],
                tags=skill_data.get("tags", []),
                parameters=skill_data.get("parameters", {})
            )
            self.skills[skill_id] = skill
            self._update_indexes(skill_id, skill)
        
        logger.info(f"Registered {len(default_skills)} default skills")
    
    def _update_indexes(self, skill_id: str, skill: Skill):
        """Update category and tag indexes
        
        Args:
            skill_id: Skill ID
            skill: Skill object
        """
        # Update category index
        if skill.category not in self.categories:
            self.categories[skill.category] = []
        if skill_id not in self.categories[skill.category]:
            self.categories[skill.category].append(skill_id)
        
        # Update tag index
        for tag in skill.tags:
            if tag not in self.tags_index:
                self.tags_index[tag] = []
            if skill_id not in self.tags_index[tag]:
                self.tags_index[tag].append(skill_id)
    
    async def register_skill(self, skill_data: Dict[str, Any]) -> str:
        """Register a new skill
        
        Args:
            skill_data: Skill data
            
        Returns:
            Skill ID
        """
        skill_id = str(uuid.uuid4())
        
        skill = Skill(
            skill_id=skill_id,
            name=skill_data.get("name"),
            description=skill_data.get("description", ""),
            category=skill_data.get("category", "general"),
            version=skill_data.get("version", "1.0.0"),
            author=skill_data.get("author", "unknown"),
            tags=skill_data.get("tags", []),
            dependencies=skill_data.get("dependencies", []),
            parameters=skill_data.get("parameters", {}),
            handler=skill_data.get("handler")
        )
        
        self.skills[skill_id] = skill
        self._update_indexes(skill_id, skill)
        
        logger.info(f"Registered skill: {skill.name} (ID: {skill_id})")
        return skill_id
    
    async def unregister_skill(self, skill_id: str) -> bool:
        """Unregister a skill
        
        Args:
            skill_id: Skill ID
            
        Returns:
            True if successful, False otherwise
        """
        if skill_id not in self.skills:
            return False
        
        skill = self.skills[skill_id]
        
        # Remove from category index
        if skill.category in self.categories:
            if skill_id in self.categories[skill.category]:
                self.categories[skill.category].remove(skill_id)
        
        # Remove from tag index
        for tag in skill.tags:
            if tag in self.tags_index:
                if skill_id in self.tags_index[tag]:
                    self.tags_index[tag].remove(skill_id)
        
        # Remove skill
        del self.skills[skill_id]
        
        logger.info(f"Unregistered skill: {skill.name} (ID: {skill_id})")
        return True
    
    async def get_skill(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """Get skill by ID
        
        Args:
            skill_id: Skill ID
            
        Returns:
            Skill data or None
        """
        if skill_id in self.skills:
            return self.skills[skill_id].to_dict()
        return None
    
    async def list_skills(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List skills with optional filters
        
        Args:
            category: Filter by category
            tags: Filter by tags
            status: Filter by status
            
        Returns:
            List of skills
        """
        skills = []
        
        for skill_id, skill in self.skills.items():
            # Apply filters
            if category and skill.category != category:
                continue
            
            if tags and not any(tag in skill.tags for tag in tags):
                continue
            
            if status and skill.status != status:
                continue
            
            skills.append(skill.to_dict())
        
        return skills
    
    async def search_skills(self, query: str) -> List[Dict[str, Any]]:
        """Search skills by query
        
        Args:
            query: Search query
            
        Returns:
            List of matching skills
        """
        query_lower = query.lower()
        results = []
        
        for skill in self.skills.values():
            if (
                query_lower in skill.name.lower() or
                query_lower in skill.description.lower() or
                query_lower in skill.category.lower() or
                any(query_lower in tag.lower() for tag in skill.tags)
            ):
                results.append(skill.to_dict())
        
        return results
    
    async def get_skills_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get skills by category
        
        Args:
            category: Category name
            
        Returns:
            List of skills in category
        """
        if category not in self.categories:
            return []
        
        return [
            self.skills[skill_id].to_dict()
            for skill_id in self.categories[category]
            if skill_id in self.skills
        ]
    
    async def get_skills_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Get skills by tag
        
        Args:
            tag: Tag name
            
        Returns:
            List of skills with tag
        """
        if tag not in self.tags_index:
            return []
        
        return [
            self.skills[skill_id].to_dict()
            for skill_id in self.tags_index[tag]
            if skill_id in self.skills
        ]
    
    async def update_skill_stats(self, skill_id: str, success: bool):
        """Update skill execution statistics
        
        Args:
            skill_id: Skill ID
            success: Whether execution was successful
        """
        if skill_id in self.skills:
            self.skills[skill_id].update_stats(success)
    
    async def get_skill_handler(self, skill_id: str) -> Optional[callable]:
        """Get skill handler
        
        Args:
            skill_id: Skill ID
            
        Returns:
            Skill handler or None
        """
        if skill_id in self.skills:
            return self.skills[skill_id].handler
        return None
    
    async def validate_parameters(
        self,
        skill_id: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate skill parameters
        
        Args:
            skill_id: Skill ID
            parameters: Parameters to validate
            
        Returns:
            Validation result
        """
        if skill_id not in self.skills:
            return {
                "valid": False,
                "errors": ["Skill not found"]
            }
        
        skill = self.skills[skill_id]
        errors = []
        
        for param_name, param_schema in skill.parameters.items():
            if param_schema.get("required", False):
                if param_name not in parameters:
                    errors.append(f"Missing required parameter: {param_name}")
            
            if param_name in parameters:
                expected_type = param_schema.get("type")
                actual_value = parameters[param_name]
                
                if expected_type == "string" and not isinstance(actual_value, str):
                    errors.append(f"Parameter {param_name} must be a string")
                elif expected_type == "number" and not isinstance(actual_value, (int, float)):
                    errors.append(f"Parameter {param_name} must be a number")
                elif expected_type == "object" and not isinstance(actual_value, dict):
                    errors.append(f"Parameter {param_name} must be an object")
                elif expected_type == "array" and not isinstance(actual_value, list):
                    errors.append(f"Parameter {param_name} must be an array")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
