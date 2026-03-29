import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions 
import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Env variable not found")
    
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )
        if response.candidates:
            for item in response.candidates:
                messages.append(item.content)
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
        if not response.function_calls:
            print(f'Response:')
            print(response.text)
            return
        else:
            function_responses = []
            for function_call in response.function_calls:
                function_call_result = call_function.call_function(function_call,args.verbose)
                if function_call_result.parts == None:
                    raise Exception   
                if function_call_result.parts[0].function_response == None:
                    raise Exception
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception
                function_responses.append(function_call_result.parts[0])
                if args.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_responses))
    if not response.text:
        print(f"Maximum number of iterations reached")
        sys.exit(1)

if __name__ == "__main__":
    main()
