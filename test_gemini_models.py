"""
Test script to list available Gemini models
"""
import os
import google.generativeai as genai

# Configure API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not set!")
    exit(1)

genai.configure(api_key=api_key)

print("🔍 Listing available Gemini models:\n")

# List all available models
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Description: {model.description}")
        print(f"   Supported methods: {model.supported_generation_methods}")
        print()

print("\n📝 Try using one of the model names above (without 'models/' prefix)")
