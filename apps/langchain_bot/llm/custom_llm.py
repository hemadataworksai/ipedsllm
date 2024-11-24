import ollama
from langchain_openai import ChatOpenAI


class CustomLLM:   
     def __init__(self,provider:str):       
         self.provider = provider        
         self.llm = self.get_llm_chat(provider)   

     def get_llm_chat(self, provider:str):        
        if provider == "ollama":
            ollama.pull("llama3.1")
            return None       
        elif provider == "google":            
             raise NotImplementedError()        
        elif provider == "openai":           
             return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        raise NotImplementedError()
     
     def invoke(self,prompt:str) -> str:       
         if self.provider == "ollama":          
             return self.invoke_ollama(prompt)       
         elif self.provider == "openai":            
             return self.invoke_openai(prompt)  

     def invoke_ollama(self, prompt):       
         response = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': prompt}])
         content:str = response["message"]["content"]
         return content

     def invoke_openai(self, prompt:str):
         response =  self.llm.invoke(prompt)        
         return response.message.content
         

if __name__ == "__main__":    
     custom_llm = CustomLLM(provider="ollama")   
     
     
     instruction = """       
        Generate SQL query from the question, return ONLY SQL query.    
     """    
     
     question = """       
          How many student learning on Boston ?      
     """    
     
     context = """       
         table description: Table that describe student data        
         table name: Students       
          columns: Name     
     """    
     
     
     final_prompt = f"""       
         Instruction: {instruction}        
         Context: {context}        
         Question: {question}        
         Answer:     
     """    
    
     print(custom_llm.invoke(final_prompt))