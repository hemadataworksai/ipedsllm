import ollama
from langchain_openai import ChatOpenAI


class LLMProvider:
     def __init__(self,provider:str):       
         self.provider = provider  
        # Select the appropriate LLM based on the provider
         self.llm = self.get_llm_chat(provider)   

     def get_llm_chat(self, provider:str):   
        # If the provider is 'ollama', return None (No LLM) 
        if provider == "ollama":
            ollama.pull("llama3.1")
            return None 
         # Raise error for unsupported 'google' provider
        elif provider == "google":            
             raise NotImplementedError()  
        # If the provider is 'openai', return the OpenAI model (gpt-3.5-turbo)
        elif provider == "openai":
            return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        else:
            raise NotImplementedError()

     def invoke(self,prompt:str) -> str:       
         if self.provider == "ollama":          
             return self.invoke_ollama(prompt)       
         elif self.provider == "openai":            
             return self.invoke_openai(prompt)  

     def invoke_ollama(self, prompt):   
        # Call the Ollama API with the provided model and prompt
         response = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': prompt}])   
        # Extract the message content from the response and return it
         return response["message"]["content"]  

     def invoke_openai(self, prompt) -> str:
        # Call the OpenAI model using the llm object and return the response
         response =  self.llm.invoke(prompt).content
         return response

#Usage example
if __name__ == "__main__":    
     custom_llm = LLMProvider(provider="ollama")
     
     
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