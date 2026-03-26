#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Capability Service Entry Point
"""

import asyncio
import logging
import sys
import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add src directory to Python path
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from services.capability.skill import SkillManager
from services.capability.executor import ToolExecutor
from services.capability.sandbox import SandboxManager
from services.capability.result import ResultCollector
from services.capability.resource import ResourceManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CapabilityService:
    """Capability Service Main Class"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8003):
        """Initialize capability service
        
        Args:
            host: Service host
            port: Service port
        """
        self.host = host
        self.port = port
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title="Capability Service",
            description="Skill management, tool execution, and sandbox environment",
            version="0.4.0"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Initialize managers
        self.skill_manager = SkillManager()
        self.tool_executor = ToolExecutor()
        self.sandbox_manager = SandboxManager()
        self.result_collector = ResultCollector()
        self.resource_manager = ResourceManager()
        
        # Setup routes
        self._setup_routes()
        self._setup_websocket()
        
        logger.info(f"Capability service initialized on {host}:{port}")
    
    def _setup_routes(self):
        """Setup HTTP routes"""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "service": "capability",
                "version": "0.4.0",
                "components": {
                    "skill_manager": "active",
                    "tool_executor": "active",
                    "sandbox_manager": "active",
                    "result_collector": "active",
                    "resource_manager": "active"
                }
            }
        
        # Skill management routes
        @self.app.post("/api/capability/skill/register")
        async def register_skill(skill_data: dict):
            """Register a new skill"""
            try:
                skill_id = await self.skill_manager.register_skill(skill_data)
                return {
                    "status": "success",
                    "skill_id": skill_id,
                    "message": "Skill registered successfully"
                }
            except Exception as e:
                logger.error(f"Failed to register skill: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        @self.app.get("/api/capability/skill/list")
        async def list_skills():
            """List all registered skills"""
            try:
                skills = await self.skill_manager.list_skills()
                return {
                    "status": "success",
                    "skills": skills,
                    "total": len(skills)
                }
            except Exception as e:
                logger.error(f"Failed to list skills: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        @self.app.get("/api/capability/skill/{skill_id}")
        async def get_skill(skill_id: str):
            """Get skill information"""
            try:
                skill = await self.skill_manager.get_skill(skill_id)
                if skill:
                    return {
                        "status": "success",
                        "skill": skill
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Skill not found"
                    }
            except Exception as e:
                logger.error(f"Failed to get skill: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        @self.app.delete("/api/capability/skill/{skill_id}")
        async def unregister_skill(skill_id: str):
            """Unregister a skill"""
            try:
                success = await self.skill_manager.unregister_skill(skill_id)
                return {
                    "status": "success" if success else "error",
                    "message": "Skill unregistered successfully" if success else "Skill not found"
                }
            except Exception as e:
                logger.error(f"Failed to unregister skill: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        # Tool execution routes
        @self.app.post("/api/capability/execute")
        async def execute_tool(request: dict):
            """Execute a tool"""
            try:
                tool_name = request.get("tool_name")
                parameters = request.get("parameters", {})
                session_id = request.get("session_id")
                use_sandbox = request.get("use_sandbox", True)
                
                # Check resource availability
                if not await self.resource_manager.check_availability():
                    return {
                        "status": "error",
                        "message": "Insufficient resources"
                    }
                
                # Execute tool
                if use_sandbox:
                    result = await self.sandbox_manager.execute_in_sandbox(
                        tool_name, parameters, session_id
                    )
                else:
                    result = await self.tool_executor.execute(tool_name, parameters, session_id)
                
                # Collect result
                await self.result_collector.collect(session_id, result)
                
                return {
                    "status": "success",
                    "result": result
                }
            except Exception as e:
                logger.error(f"Failed to execute tool: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        @self.app.post("/api/capability/execute/batch")
        async def execute_batch(request: dict):
            """Execute multiple tools in batch"""
            try:
                tools = request.get("tools", [])
                session_id = request.get("session_id")
                
                results = []
                for tool_request in tools:
                    tool_name = tool_request.get("tool_name")
                    parameters = tool_request.get("parameters", {})
                    
                    result = await self.tool_executor.execute(tool_name, parameters, session_id)
                    results.append(result)
                    await self.result_collector.collect(session_id, result)
                
                return {
                    "status": "success",
                    "results": results,
                    "total": len(results)
                }
            except Exception as e:
                logger.error(f"Failed to execute batch: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        # Sandbox management routes
        @self.app.post("/api/capability/sandbox/create")
        async def create_sandbox(request: dict):
            """Create a sandbox environment"""
            try:
                session_id = request.get("session_id")
                config = request.get("config", {})
                
                sandbox_id = await self.sandbox_manager.create_sandbox(session_id, config)
                
                return {
                    "status": "success",
                    "sandbox_id": sandbox_id,
                    "message": "Sandbox created successfully"
                }
            except Exception as e:
                logger.error(f"Failed to create sandbox: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        @self.app.delete("/api/capability/sandbox/{sandbox_id}")
        async def destroy_sandbox(sandbox_id: str):
            """Destroy a sandbox environment"""
            try:
                success = await self.sandbox_manager.destroy_sandbox(sandbox_id)
                return {
                    "status": "success" if success else "error",
                    "message": "Sandbox destroyed successfully" if success else "Sandbox not found"
                }
            except Exception as e:
                logger.error(f"Failed to destroy sandbox: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        # Resource management routes
        @self.app.get("/api/capability/resource/status")
        async def get_resource_status():
            """Get resource status"""
            try:
                status = await self.resource_manager.get_status()
                return {
                    "status": "success",
                    "resources": status
                }
            except Exception as e:
                logger.error(f"Failed to get resource status: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
        
        # Result collection routes
        @self.app.get("/api/capability/result/{session_id}")
        async def get_results(session_id: str):
            """Get execution results for a session"""
            try:
                results = await self.result_collector.get_results(session_id)
                return {
                    "status": "success",
                    "results": results
                }
            except Exception as e:
                logger.error(f"Failed to get results: {e}")
                return {
                    "status": "error",
                    "message": str(e)
                }
    
    def _setup_websocket(self):
        """Setup WebSocket endpoint"""
        
        @self.app.websocket("/ws/capability")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time capability execution"""
            await websocket.accept()
            logger.info("WebSocket connection established")
            
            try:
                while True:
                    data = await websocket.receive_json()
                    message_type = data.get("type")
                    
                    if message_type == "execute":
                        tool_name = data.get("tool_name")
                        parameters = data.get("parameters", {})
                        session_id = data.get("session_id")
                        
                        await websocket.send_json({
                            "type": "status",
                            "message": f"Executing {tool_name}..."
                        })
                        
                        result = await self.tool_executor.execute(
                            tool_name, parameters, session_id
                        )
                        
                        await websocket.send_json({
                            "type": "result",
                            "result": result
                        })
                    
                    elif message_type == "ping":
                        await websocket.send_json({"type": "pong"})
                    
            except WebSocketDisconnect:
                logger.info("WebSocket connection closed")
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await websocket.close()
    
    def run(self):
        """Run the capability service"""
        uvicorn.run(self.app, host=self.host, port=self.port)


if __name__ == "__main__":
    service = CapabilityService()
    service.run()
