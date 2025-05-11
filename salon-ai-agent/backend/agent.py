import logging
from datetime import datetime
import requests
import random
import time
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("salon-agent")

class SalonAgent:
    def __init__(self):
        # Basic knowledge about the fake salon
        self.knowledge_base = {
            "what are your hours": "We're open from 9 AM to 7 PM, Tuesday through Saturday.",
            "do you take walk-ins": "Yes, we accept walk-ins based on availability, but appointments are recommended.",
            "how much is a haircut": "Our haircuts start at $45 for women and $35 for men.",
        }
        
        # Simulated customer questions
        self.sample_questions = [
            "what are your hours",
            "do you take walk-ins",
            "how much is a haircut",
            "do you do beard trims",  # Unknown question
            "what's your address",    # Unknown question
        ]
        
    async def start(self):
        logger.info("Starting salon agent in simulation mode...")
        
        while True:
            # Simulate receiving a call every 30 seconds
            logger.info("\n" + "="*50)
            logger.info("Simulating new customer call...")
            await self._simulate_call()
            logger.info("Call simulation complete.")
            logger.info("="*50 + "\n")
            
            # Wait before next call
            time.sleep(30)
        
    async def _simulate_call(self):
        # Randomly select a question
        question = random.choice(self.sample_questions)
        logger.info(f"Customer asks: {question}")
        
        # Check knowledge base
        answer = self._get_answer(question)
        if answer:
            logger.info(f"AI answers: {answer}")
        else:
            # Escalate to human
            logger.info("AI doesn't know the answer - escalating to human supervisor")
            await self._escalate_to_human(question)
            logger.info("AI tells customer: 'Let me check with my supervisor and get back to you.'")
            
    def _get_answer(self, question: str) -> Optional[str]:
        # Simple keyword matching for demo
        question_lower = question.lower()
        for known_q, answer in self.knowledge_base.items():
            if known_q in question_lower:
                return answer
        return None
        
    async def _escalate_to_human(self, question: str):
        # Create a help request via the API
        logger.info(f"Escalating question to human: {question}")
        try:
            response = requests.post(
                "http://localhost:8000/api/help-requests/",
                json={
                    "customer_phone": self._generate_phone_number(),  # Simulated phone number
                    "question": question
                }
            )
            response.raise_for_status()
            logger.info(f"Created help request: {response.json()}")
        except Exception as e:
            logger.error(f"Failed to create help request: {e}")
    
    def _generate_phone_number(self):
        return f"+1{random.randint(200, 999)}{random.randint(200, 999)}{random.randint(1000, 9999)}"

if __name__ == "__main__":
    agent = SalonAgent()
    
    # For Python 3.7+ we can use asyncio.run(), but this works for all versions
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(agent.start())