from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from ..config import settings
from typing import Dict

class AIService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
    
    async def chat_completion(self, prompt: str) -> Dict[str, any]:
        """General chat - 1 credit"""
        try:
            response = await self.llm.ainvoke(prompt)
            return {
                "output": response.content,
                "credits": 1
            }
        except Exception as e:
            raise Exception(f"AI execution failed: {str(e)}")
    
    async def text_summarizer(self, text: str) -> Dict[str, any]:
        """Summarize text - 2 credits"""
        try:
            prompt_template = ChatPromptTemplate.from_template(
                "Summarize the following text concisely:\n\n{text}\n\nSummary:"
            )
            chain = prompt_template | self.llm
            response = await chain.ainvoke({"text": text})
            return {
                "output": response.content,
                "credits": 2
            }
        except Exception as e:
            raise Exception(f"AI execution failed: {str(e)}")
    
    async def content_generator(self, topic: str) -> Dict[str, any]:
        """Generate content - 3 credits"""
        try:
            prompt_template = ChatPromptTemplate.from_template(
                "Write a comprehensive article about: {topic}\n\nArticle:"
            )
            chain = prompt_template | self.llm
            response = await chain.ainvoke({"topic": topic})
            return {
                "output": response.content,
                "credits": 3
            }
        except Exception as e:
            raise Exception(f"AI execution failed: {str(e)}")
    
    async def code_helper(self, question: str) -> Dict[str, any]:
        """Help with code - 2 credits"""
        try:
            prompt_template = ChatPromptTemplate.from_template(
                "You are a coding assistant. Answer this programming question:\n\n{question}\n\nAnswer:"
            )
            chain = prompt_template | self.llm
            response = await chain.ainvoke({"question": question})
            return {
                "output": response.content,
                "credits": 2
            }
        except Exception as e:
            raise Exception(f"AI execution failed: {str(e)}")
    
    async def text_analyzer(self, text: str) -> Dict[str, any]:
        """Analyze sentiment and key points - 2 credits"""
        try:
            prompt_template = ChatPromptTemplate.from_template(
                "Analyze the following text for sentiment and key points:\n\n{text}\n\nAnalysis:"
            )
            chain = prompt_template | self.llm
            response = await chain.ainvoke({"text": text})
            return {
                "output": response.content,
                "credits": 2
            }
        except Exception as e:
            raise Exception(f"AI execution failed: {str(e)}")

ai_service = AIService()