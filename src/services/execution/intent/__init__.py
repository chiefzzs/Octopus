#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Intent Analysis Module
"""

from typing import Dict, Any, List
import re

from common.utils.logger import get_logger


class IntentAnalyzer:
    """Intent Analyzer Class"""
    
    def __init__(self):
        """Initialize Intent Analyzer"""
        self.logger = get_logger(__name__)
        
        # Define intent patterns
        self.intent_patterns = {
            "query": [
                r"what is",
                r"how do",
                r"tell me about",
                r"explain",
                r"describe",
                r"what are"
            ],
            "action": [
                r"create",
                r"generate",
                r"write",
                r"make",
                r"build",
                r"develop",
                r"produce"
            ],
            "analysis": [
                r"analyze",
                r"evaluate",
                r"assess",
                r"compare",
                r"review",
                r"examine"
            ],
            "modification": [
                r"modify",
                r"change",
                r"update",
                r"edit",
                r"adjust",
                r"fix"
            ],
            "deletion": [
                r"delete",
                r"remove",
                r"erase",
                r"clear"
            ],
            "search": [
                r"find",
                r"search",
                r"look for",
                r"locate",
                r"discover"
            ]
        }
        
        # Define entity patterns
        self.entity_patterns = {
            "file": [
                r"\.txt$",
                r"\.py$",
                r"\.js$",
                r"\.json$",
                r"\.md$",
                r"file",
                r"document"
            ],
            "code": [
                r"code",
                r"function",
                r"class",
                r"script",
                r"program"
            ],
            "data": [
                r"data",
                r"information",
                r"record",
                r"entry"
            ],
            "system": [
                r"system",
                r"service",
                r"process",
                r"application"
            ]
        }
    
    async def analyze(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user intent
        
        Args:
            user_input: User input string
            context: Execution context
            
        Returns:
            Intent analysis result
        """
        # Normalize input
        normalized_input = user_input.lower().strip()
        
        # Detect intent
        intent = self._detect_intent(normalized_input)
        
        # Extract entities
        entities = self._extract_entities(normalized_input)
        
        # Extract parameters
        parameters = self._extract_parameters(user_input, entities)
        
        # Determine confidence
        confidence = self._calculate_confidence(intent, entities, normalized_input)
        
        # Build result
        result = {
            "intent": intent,
            "entities": entities,
            "parameters": parameters,
            "confidence": confidence,
            "original_input": user_input,
            "context": context
        }
        
        self.logger.info(f"Intent analyzed: {intent} (confidence: {confidence})")
        
        return result
    
    def _detect_intent(self, normalized_input: str) -> str:
        """Detect user intent from normalized input
        
        Args:
            normalized_input: Normalized user input
            
        Returns:
            Detected intent
        """
        best_intent = "unknown"
        best_score = 0
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, normalized_input, re.IGNORECASE):
                    score += 1
            
            if score > best_score:
                best_score = score
                best_intent = intent
        
        return best_intent
    
    def _extract_entities(self, normalized_input: str) -> List[Dict[str, Any]]:
        """Extract entities from normalized input
        
        Args:
            normalized_input: Normalized user input
            
        Returns:
            List of extracted entities
        """
        entities = []
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, normalized_input, re.IGNORECASE)
                for match in matches:
                    entities.append({
                        "type": entity_type,
                        "value": match.group(),
                        "position": match.span()
                    })
        
        return entities
    
    def _extract_parameters(self, user_input: str, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract parameters from user input and entities
        
        Args:
            user_input: Original user input
            entities: Extracted entities
            
        Returns:
            Dictionary of parameters
        """
        parameters = {}
        
        # Extract file names
        file_entities = [e for e in entities if e["type"] == "file"]
        if file_entities:
            parameters["files"] = [e["value"] for e in file_entities]
        
        # Extract code references
        code_entities = [e for e in entities if e["type"] == "code"]
        if code_entities:
            parameters["code_references"] = [e["value"] for e in code_entities]
        
        # Extract numbers
        numbers = re.findall(r'\d+', user_input)
        if numbers:
            parameters["numbers"] = [int(n) for n in numbers]
        
        # Extract quoted strings
        quoted_strings = re.findall(r'"([^"]*)"', user_input)
        if quoted_strings:
            parameters["quoted_strings"] = quoted_strings
        
        return parameters
    
    def _calculate_confidence(self, intent: str, entities: List[Dict[str, Any]], normalized_input: str) -> float:
        """Calculate confidence score for intent detection
        
        Args:
            intent: Detected intent
            entities: Extracted entities
            normalized_input: Normalized user input
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.0
        
        # Base confidence based on intent
        if intent != "unknown":
            confidence += 0.5
        
        # Add confidence based on entities
        if entities:
            confidence += 0.3 * min(len(entities) / 3, 1.0)
        
        # Add confidence based on input length
        if len(normalized_input) > 10:
            confidence += 0.2
        
        # Cap at 1.0
        return min(confidence, 1.0)
    
    async def get_intent_suggestions(self, partial_input: str) -> List[Dict[str, Any]]:
        """Get intent suggestions based on partial input
        
        Args:
            partial_input: Partial user input
            
        Returns:
            List of intent suggestions
        """
        suggestions = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if partial_input.lower().startswith(pattern[:len(partial_input)]):
                    suggestions.append({
                        "intent": intent,
                        "pattern": pattern,
                        "completion": pattern[len(partial_input):]
                    })
        
        return suggestions
