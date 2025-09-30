from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
import requests
import time

# 1. Pydantic Models 

class ChatMessage(BaseModel):
    role: str
    parts: List[str]

class ChatRequest(BaseModel):
    code: str
    compiler_logs: str = Field(..., alias="compilerLogs")
    history: List[ChatMessage]
    user_prompt: str = Field(..., alias="userPrompt")

class ChatResponse(BaseModel):
    chat_response: str
    corrected_code: str

class TestCodeRequest(BaseModel):
    code: str

class TestCodeResponse(BaseModel):
    output: str

# 2. Initialize Router and API Clients 
router = APIRouter()
model = None

# judge0_api_key = None 

try:
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("Gemini 1.5 Flash model initialized successfully.")

except Exception as e:
    print(f" FATAL: Error during API setup: {e}")

# 3. Test Code Endpoint (using Paiza.IO) 

@router.post("/test-code", response_model=TestCodeResponse, tags=["Code Execution"])
async def test_code_endpoint(request: TestCodeRequest):
    # Paiza.IO API endpoint for creating submissions
    create_url = "https://api.paiza.io/runners/create"
    # Paiza.IO API endpoint for getting submission status/details
    details_url = "https://api.paiza.io/runners/get_details"
    
    # Payload for the API request. 'cpp' is the language identifier.
    create_payload = {
        "source_code": request.code,
        "language": "cpp",
        "api_key": "guest" # guest access for simple use cases
    }

    try:
        # 1. Create the submission to Paiza.IO
        create_response = requests.post(create_url, json=create_payload)
        create_response.raise_for_status()
        submission_data = create_response.json()
        submission_id = submission_data.get("id")
        if not submission_id:
            raise HTTPException(status_code=400, detail=f"Failed to create a submission with Paiza.IO: {submission_data.get('error')}")

        # 2. Poll Paiza.IO for the result using the submission ID
        final_result = None
        details_params = {"id": submission_id, "api_key": "guest"}
        
        for _ in range(5): # Poll for 10 seconds max
            time.sleep(2)
            details_response = requests.get(details_url, params=details_params)
            details_response.raise_for_status()
            result_data = details_response.json()
            
            if result_data.get("status") == "completed":
                final_result = result_data
                break
        
        if final_result is None:
            raise HTTPException(status_code=408, detail="Compiler took too long to respond.")

        # 3. Formatted output 
        build_stderr = final_result.get('build_stderr') or ""
        stdout = final_result.get('stdout') or ""
        stderr = final_result.get('stderr') or ""
        build_result = final_result.get('build_result') 
        
        status = "Compilation Error" if build_result == 'failure' else "Accepted"
        if status == "Accepted" and stderr:
            status = "Runtime Error"

        output = f"Status: {status}\n\n"
        if stdout:
            output += f"--- Output ---\n{stdout}\n"
        if stderr:
            output += f"--- Runtime Error ---\n{stderr}\n"
        if build_stderr:
            output += f"--- Compile Log ---\n{build_stderr}\n"
        
        if status == "Accepted" and not any([stdout, stderr, build_stderr]):
            output += "Execution finished successfully with no output."

        return TestCodeResponse(output=output)

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Paiza.IO API: {e}")

# 4. Conversational Correction Endpoint 

@router.post("/correct-code-chat", response_model=ChatResponse, tags=["Conversational Code Correction"])
async def correct_code_chat_endpoint(request: ChatRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Gemini model is not initialized.")
    
    gemini_history = [{"role": msg.role, "parts": msg.parts} for msg in request.history]
    chat = model.start_chat(history=gemini_history)

    full_prompt = f"""
    You are an expert C++ code assistant.
    A user's code has failed to compile or run correctly. Your task is to fix it based on their instructions and the provided compiler logs.

    Here are the compiler/runtime logs:
    --- COMPILER LOGS ---
    {request.compiler_logs}
    --- END LOGS ---

    Here is the original C++ code that produced these logs:
    --- ORIGINAL CODE ---
    {request.code}
    --- END CODE ---

    The user's latest instruction is: "{request.user_prompt}"

    Based on the user's instruction, the compiler logs, and our conversation history, provide a conversational response explaining the fix, and then provide the complete, updated C++ code.
    Your response MUST include the full code block inside ```cpp ... ```.
    """
    try:
        response = chat.send_message(full_prompt)
        full_response_text = response.text
        code_match = re.search(r'```cpp\n(.*?)```', full_response_text, re.DOTALL)
        if code_match:
            corrected_code = code_match.group(1).strip()
        else:
            corrected_code = "Could not extract code from the AI's response."
        return ChatResponse(chat_response=full_response_text, corrected_code=corrected_code)
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        raise HTTPException(status_code=500, detail=str(e))

