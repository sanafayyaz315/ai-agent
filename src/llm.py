from openai import OpenAI

### For Later: Create an LLM class to intialize llm, and methods to invoke and stream

class LLM:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """Initialize with required API key and model name. 
        Args:
            api_key (str): OpenAI API key
            model (str): Default model to use (e.g., "gpt-4", "gpt-3.5-turbo"). Default set to gpt-3.5-turbo
        """  
        self.llm = OpenAI(api_key=api_key)
        self.model = model

    def invoke(self, prompt: str) -> str:
        """Get complete response."""
        response = self.llm.chat.completions.create( 
        model=self.model,
        messages=[{"role": "user", "content": prompt}],
        seed=42
    )
        return response.choices[0].message.content

    def stream(self, prompt: str):
        """Stream response token by token."""
        stream = self.llm.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            if content := chunk.choices[0].delta.content:
                yield content

    # def __call__(self, prompt: str, model: str = None, stream: bool = False):
    #     if stream:
    #         return self.stream(prompt, model)
    #     return self.invoke(prompt, model)

# def llm(api_key):
#     llm = OpenAI(api_key=api_key)
#     return llm

# def invoke_llm(llm, prompt, model="gpt-3.5-turbo"):
#     response = llm.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content


# def invoke_llm_stream(llm, prompt, model="gpt-3.5-turbo"):
#     yield llm.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}]
#     ).choices[0].message.content

if __name__ == "__main__":
    api_key = "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"
    # llm = llm(api_key=api_key)
    # #--for SIMPLE response--#
    # response = invoke_llm(llm, "hi")
    # print(response)
    #  #--for STREAMING response--#
    # response = ""
    # for chunk in invoke_llm_stream(llm, "what is photosynthesis? explain in detail"):
    #     response += chunk
    #     print(chunk, end= "", flush=True)

    llm = LLM(api_key=api_key)
    # Regular invocation
    # print("\nRegular response:")
    # response = llm.invoke("Explain quantum computing simply")
    # print(response)

    # Streaming
    print("\nStreaming response:")
    for chunk in llm.stream("Explain photosynthesis in detail"):
        print(chunk, end="", flush=True)
    
    # Invokes __call__ where invoke is default
    # print(llm("What is AI?"))

    # # Invokes __call__ with stream
    # for chunk in llm("What is machine learning?", stream=True):
    #     print(chunk, end="", flush=True)

