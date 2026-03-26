#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Execution Service Entry Point
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from common.utils.logger import get_logger
from services.execution.react import ReActEngine
from services.execution.intent import IntentAnalyzer
from services.execution.planning import TaskPlanner
from services.execution.context import ContextManager
from services.execution.tools import ToolSelector


class ExecutionService:
    """Execution Service Class"""
    
    def __init__(self):
        """Initialize Execution Service"""
        self.logger = get_logger(__name__)
        self.app = FastAPI(title="Octopus Execution Service", version="0.3.0")
        
        # Initialize core components
        self.react_engine = ReActEngine()
        self.intent_analyzer = IntentAnalyzer()
        self.task_planner = TaskPlanner()
        self.context_manager = ContextManager()
        self.tool_selector = ToolSelector()
        
        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self):
        """Register routes"""
        
        # Health check
        @self.app.get("/health")
        async def health_check():
            """Health check"""
            return {"status": "healthy", "service": "execution"}
        
        # Execute task
        @self.app.post("/api/execution/execute")
        async def execute_task(request: dict):
            """Execute task"""
            try:
                task_id = request.get("task_id")
                user_input = request.get("user_input")
                session_id = request.get("session_id")
                
                # Create context
                context = await self.context_manager.create_context(session_id, user_input)
                
                # Analyze intent
                intent = await self.intent_analyzer.analyze(user_input, context)
                
                # Plan tasks
                tasks = await self.task_planner.plan(intent, context)
                
                # Execute using ReAct engine
                result = await self.react_engine.execute(tasks, context)
                
                return {
                    "status": "success",
                    "task_id": task_id,
                    "result": result,
                    "intent": intent,
                    "tasks": tasks
                }
            except Exception as e:
                self.logger.error(f"Task execution failed: {e}")
                return {
                    "status": "error",
                    "message": f"Task execution failed: {str(e)}"
                }
        
        # Stream execution
        @self.app.post("/api/execution/stream")
        async def stream_execution(request: dict):
            """Stream execution with real-time output"""
            try:
                task_id = request.get("task_id")
                user_input = request.get("user_input")
                session_id = request.get("session_id")
                
                # Create context
                context = await self.context_manager.create_context(session_id, user_input)
                
                # Analyze intent
                intent = await self.intent_analyzer.analyze(user_input, context)
                
                # Plan tasks
                tasks = await self.task_planner.plan(intent, context)
                
                # Execute using ReAct engine with streaming
                async def generate():
                    async for chunk in self.react_engine.execute_stream(tasks, context):
                        yield f"data: {chunk}\n\n"
                
                from fastapi.responses import StreamingResponse
                return StreamingResponse(generate(), media_type="text/event-stream")
            except Exception as e:
                self.logger.error(f"Stream execution failed: {e}")
                return {
                    "status": "error",
                    "message": f"Stream execution failed: {str(e)}"
                }
        
        # WebSocket endpoint for real-time execution
        @self.app.websocket("/ws/execution")
        async def websocket_execution(websocket: WebSocket):
            """WebSocket endpoint for real-time execution"""
            await websocket.accept()
            try:
                while True:
                    data = await websocket.receive_json()
                    
                    # Create context
                    context = await self.context_manager.create_context(
                        data.get("session_id"),
                        data.get("user_input")
                    )
                    
                    # Analyze intent
                    intent = await self.intent_analyzer.analyze(
                        data.get("user_input"),
                        context
                    )
                    
                    # Plan tasks
                    tasks = await self.task_planner.plan(intent, context)
                    
                    # Execute using ReAct engine with real-time updates
                    async for update in self.react_engine.execute_stream(tasks, context):
                        await websocket.send_json({
                            "type": "update",
                            "data": update
                        })
                    
                    # Send final result
                    await websocket.send_json({
                        "type": "complete",
                        "data": {"status": "success"}
                    })
                    
            except WebSocketDisconnect:
                self.logger.info("WebSocket disconnected")
            except Exception as e:
                self.logger.error(f"WebSocket execution failed: {e}")
                await websocket.send_json({
                    "type": "error",
                    "data": {"message": str(e)}
                })
    
    def run(self, host="0.0.0.0", port=8002):
        """Run execution service"""
        self.logger.info(f"Execution service starting, listening on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


if __name__ == "__main__":
    service = ExecutionService()
    service.run()
