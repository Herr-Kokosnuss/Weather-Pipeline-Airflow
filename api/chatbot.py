from typing import Dict, Any
import os
import aiohttp
from openai import AsyncOpenAI
from fastapi import HTTPException

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def fetch_weather_from_api(location: str) -> Dict[str, Any]:
    """Fetch current weather data for a given location using OpenWeatherMap API."""
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={location}&appid={os.getenv('OPENWEATHERMAP_API_KEY')}"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise HTTPException(status_code=resp.status, detail="Failed to fetch weather data")
                data = await resp.json()

        temp_k = data["main"]["temp"]
        temp = temp_k - 273.15  

        conditions = data["weather"][0]["description"]
        return {"conditions": conditions, "temperature": round(temp, 1)}
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {str(e)}")

async def get_chat_response(user_message: str) -> str:
    """Process user message and return chatbot response with weather information."""
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful weather assistant. When users ask about weather, extract the location from their message and respond with weather information in Celsius. If the question is not weather-related, politely explain that you're designed to help with weather-related questions only."
            },
            {"role": "user", "content": user_message}
        ]
        
        response = await client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 for better understanding
            messages=messages,
            functions=[{
                "name": "fetch_weather_from_api",
                "description": "Get the current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city e.g. 'Berlin, Germany' or 'Barcelona, Spain'"
                        }
                    },
                    "required": ["location"]
                }
            }],
            function_call="auto"
        )
        
        assistant_message = response.choices[0].message
        
        if assistant_message.function_call:
            function_args = eval(assistant_message.function_call.arguments)
            weather_data = await fetch_weather_from_api(**function_args)
            
            messages.append({
                "role": "function",
                "name": "fetch_weather_from_api",
                "content": str(weather_data)
            })
            
            second_response = await client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            
            return second_response.choices[0].message.content
        else:
            return assistant_message.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}") 