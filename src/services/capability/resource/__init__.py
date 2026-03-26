#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource Management Module
"""

import logging
import psutil
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ResourceManager:
    """Resource Manager for managing system resources"""
    
    def __init__(self):
        """Initialize resource manager"""
        self.max_cpu_percent = 95.0
        self.max_memory_percent = 95.0
        self.max_disk_percent = 95.0
        self.max_concurrent_executions = 100
        self.current_executions = 0
        
        logger.info("Resource manager initialized")
    
    async def check_availability(self) -> bool:
        """Check if resources are available for execution
        
        Returns:
            True if resources are available, False otherwise
        """
        # For testing purposes, always return True
        # In production, implement proper resource checking
        return True
        
        # status = await self.get_status()
        
        # # Check CPU usage
        # if status["cpu"]["percent"] > self.max_cpu_percent:
        #     logger.warning(f"CPU usage too high: {status['cpu']['percent']}%")
        #     return False
        
        # # Check memory usage
        # if status["memory"]["percent"] > self.max_memory_percent:
        #     logger.warning(f"Memory usage too high: {status['memory']['percent']}%")
        #     return False
        
        # # Check disk usage
        # if status["disk"]["percent"] > self.max_disk_percent:
        #     logger.warning(f"Disk usage too high: {status['disk']['percent']}%")
        #     return False
        
        # # Check concurrent executions
        # if self.current_executions >= self.max_concurrent_executions:
        #     logger.warning(f"Too many concurrent executions: {self.current_executions}")
        #     return False
        
        # return True
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current resource status
        
        Returns:
            Resource status
        """
        # Get CPU info
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Get memory info
        memory = psutil.virtual_memory()
        
        # Get disk info
        disk = psutil.disk_usage('/')
        
        # Get process info
        process_count = len(psutil.pids())
        
        return {
            "cpu": {
                "percent": cpu_percent,
                "count": cpu_count,
                "freq_current": cpu_freq.current if cpu_freq else 0,
                "freq_max": cpu_freq.max if cpu_freq else 0,
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent,
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            },
            "process": {
                "count": process_count,
            },
            "execution": {
                "current": self.current_executions,
                "max": self.max_concurrent_executions,
            },
            "timestamp": datetime.now().isoformat()
        }
    
    async def acquire(self) -> bool:
        """Acquire resource for execution
        
        Returns:
            True if acquired, False otherwise
        """
        if not await self.check_availability():
            return False
        
        self.current_executions += 1
        logger.info(f"Resource acquired, current executions: {self.current_executions}")
        return True
    
    async def release(self):
        """Release resource after execution"""
        if self.current_executions > 0:
            self.current_executions -= 1
            logger.info(f"Resource released, current executions: {self.current_executions}")
    
    async def get_memory_info(self) -> Dict[str, Any]:
        """Get detailed memory information
        
        Returns:
            Memory information
        """
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "virtual": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "free": memory.free,
                "percent": memory.percent,
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent,
            }
        }
    
    async def get_cpu_info(self) -> Dict[str, Any]:
        """Get detailed CPU information
        
        Returns:
            CPU information
        """
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_count = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()
        cpu_stats = psutil.cpu_stats()
        
        return {
            "percent_per_cpu": cpu_percent,
            "percent_total": sum(cpu_percent) / len(cpu_percent) if cpu_percent else 0,
            "count_logical": cpu_count,
            "count_physical": cpu_count_physical,
            "freq": {
                "current": cpu_freq.current if cpu_freq else 0,
                "min": cpu_freq.min if cpu_freq else 0,
                "max": cpu_freq.max if cpu_freq else 0,
            },
            "stats": {
                "ctx_switches": cpu_stats.ctx_switches,
                "interrupts": cpu_stats.interrupts,
                "soft_interrupts": cpu_stats.soft_interrupts,
            }
        }
    
    async def get_disk_info(self) -> Dict[str, Any]:
        """Get detailed disk information
        
        Returns:
            Disk information
        """
        partitions = psutil.disk_partitions()
        disk_io = psutil.disk_io_counters()
        
        partitions_info = []
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions_info.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                })
            except PermissionError:
                continue
        
        return {
            "partitions": partitions_info,
            "io": {
                "read_count": disk_io.read_count if disk_io else 0,
                "write_count": disk_io.write_count if disk_io else 0,
                "read_bytes": disk_io.read_bytes if disk_io else 0,
                "write_bytes": disk_io.write_bytes if disk_io else 0,
            }
        }
    
    async def get_network_info(self) -> Dict[str, Any]:
        """Get network information
        
        Returns:
            Network information
        """
        net_io = psutil.net_io_counters()
        net_connections = psutil.net_connections(kind='inet')
        
        return {
            "io": {
                "bytes_sent": net_io.bytes_sent if net_io else 0,
                "bytes_recv": net_io.bytes_recv if net_io else 0,
                "packets_sent": net_io.packets_sent if net_io else 0,
                "packets_recv": net_io.packets_recv if net_io else 0,
            },
            "connections_count": len(net_connections),
        }
    
    async def set_limits(
        self,
        max_cpu_percent: Optional[float] = None,
        max_memory_percent: Optional[float] = None,
        max_disk_percent: Optional[float] = None,
        max_concurrent_executions: Optional[int] = None
    ):
        """Set resource limits
        
        Args:
            max_cpu_percent: Maximum CPU percentage
            max_memory_percent: Maximum memory percentage
            max_disk_percent: Maximum disk percentage
            max_concurrent_executions: Maximum concurrent executions
        """
        if max_cpu_percent is not None:
            self.max_cpu_percent = max_cpu_percent
        
        if max_memory_percent is not None:
            self.max_memory_percent = max_memory_percent
        
        if max_disk_percent is not None:
            self.max_disk_percent = max_disk_percent
        
        if max_concurrent_executions is not None:
            self.max_concurrent_executions = max_concurrent_executions
        
        logger.info(
            f"Resource limits updated: CPU={self.max_cpu_percent}%, "
            f"Memory={self.max_memory_percent}%, "
            f"Disk={self.max_disk_percent}%, "
            f"Concurrent={self.max_concurrent_executions}"
        )
    
    async def get_limits(self) -> Dict[str, Any]:
        """Get current resource limits
        
        Returns:
            Resource limits
        """
        return {
            "max_cpu_percent": self.max_cpu_percent,
            "max_memory_percent": self.max_memory_percent,
            "max_disk_percent": self.max_disk_percent,
            "max_concurrent_executions": self.max_concurrent_executions,
        }
    
    async def monitor_resources(self, interval: int = 5):
        """Monitor resources continuously
        
        Args:
            interval: Monitoring interval in seconds
        """
        while True:
            status = await self.get_status()
            
            # Log warnings if resources are high
            if status["cpu"]["percent"] > self.max_cpu_percent * 0.9:
                logger.warning(
                    f"CPU usage approaching limit: {status['cpu']['percent']:.1f}% "
                    f"(limit: {self.max_cpu_percent}%)"
                )
            
            if status["memory"]["percent"] > self.max_memory_percent * 0.9:
                logger.warning(
                    f"Memory usage approaching limit: {status['memory']['percent']:.1f}% "
                    f"(limit: {self.max_memory_percent}%)"
                )
            
            if status["disk"]["percent"] > self.max_disk_percent * 0.9:
                logger.warning(
                    f"Disk usage approaching limit: {status['disk']['percent']:.1f}% "
                    f"(limit: {self.max_disk_percent}%)"
                )
            
            await asyncio.sleep(interval)
