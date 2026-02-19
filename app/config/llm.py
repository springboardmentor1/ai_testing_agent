"""
Hybrid LLM Configuration
Primary: Groq API (faster, more powerful)
Fallback: Ollama (local, always available)
"""

import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


# ==================== GROQ CONFIGURATION ====================
try:
    from groq import Groq
    
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Preferred models (priority order)
    PRIMARY_MODEL = "llama-3.3-70b-versatile"
    FALLBACK_MODEL = "gemma2-9b-it"
    
    GROQ_AVAILABLE = True
    print("✅ Groq API available")
    
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️  Groq not installed. Install with: pip install groq")
except Exception as e:
    GROQ_AVAILABLE = False
    print(f"⚠️  Groq initialization failed: {e}")


# ==================== OLLAMA CONFIGURATION ====================
try:
    import ollama
    
    OLLAMA_MODEL = "gemma:2b"
    OLLAMA_AVAILABLE = True
    print("✅ Ollama available")
    
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️  Ollama not installed. Install with: pip install ollama")


class LLMError(Exception):
    """Custom exception for LLM failures"""
    pass


# ==================== GROQ FUNCTIONS ====================
def call_groq(
    prompt: str,
    model: str,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> str:
    """
    Call Groq API
    
    Args:
        prompt: The user prompt
        model: Model name (llama-3.3-70b or gemma2-9b)
        temperature: Creativity (0.0-1.0)
        max_tokens: Maximum response length
        
    Returns:
        Model response text
    """
    if not GROQ_AVAILABLE:
        raise LLMError("Groq not available")
    
    try:
        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a strict JSON generator for test automation. Output ONLY valid JSON, no markdown, no explanations."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise LLMError(f"Groq API error: {str(e)}")


# ==================== OLLAMA FUNCTIONS ====================
def call_ollama(
    prompt: str,
    model: str = OLLAMA_MODEL,
    temperature: float = 0.2,
) -> str:
    """
    Call local Ollama
    
    Args:
        prompt: The user prompt
        model: Model name (default: gemma:2b)
        temperature: Creativity (0.0-1.0)
        
    Returns:
        Model response text
    """
    if not OLLAMA_AVAILABLE:
        raise LLMError("Ollama not available")
    
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "You are a strict JSON generator for test automation. Output ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            format="json"
        )
        return response["message"]["content"]
    
    except Exception as e:
        raise LLMError(f"Ollama error: {str(e)}")


# ==================== UNIFIED LLM FUNCTION ====================
def call_llm(prompt: str, temperature: float = 0.2) -> str:
    """
    Unified LLM function with automatic fallback
    
    Priority:
    1. Groq (llama-3.3-70b) - Fast, powerful
    2. Groq (gemma2-9b) - Fast, smaller
    3. Ollama (gemma:2b) - Local, always works
    
    Args:
        prompt: User prompt
        temperature: Creativity level
        
    Returns:
        LLM response text
        
    Raises:
        LLMError: If all LLMs fail
    """
    
    # 1️ Try Groq Primary (llama-3.3-70b)
    if GROQ_AVAILABLE:
        try:
            print(" Using Groq (llama-3.3-70b)...")
            response = call_groq(
                prompt=prompt,
                model=PRIMARY_MODEL,
                temperature=temperature,
                max_tokens=1024
            )
            print(" Groq primary succeeded")
            return response
        
        except Exception as e:
            print(f"  Groq primary failed: {e}")
    
    # 2️ Try Groq Fallback (gemma2-9b)
    if GROQ_AVAILABLE:
        try:
            print(" Trying Groq fallback (gemma2-9b)...")
            response = call_groq(
                prompt=prompt,
                model=FALLBACK_MODEL,
                temperature=temperature,
                max_tokens=1024
            )
            print(" Groq fallback succeeded")
            return response
        
        except Exception as e:
            print(f"  Groq fallback failed: {e}")
    
    # 3️ Try Ollama (gemma:2b)
    if OLLAMA_AVAILABLE:
        try:
            print(" Trying Ollama (gemma:2b)...")
            response = call_ollama(
                prompt=prompt,
                model=OLLAMA_MODEL,
                temperature=temperature
            )
            print(" Ollama succeeded")
            return response
        
        except Exception as e:
            print(f"  Ollama failed: {e}")
    
    #  All methods failed
    raise LLMError(
        "All LLM methods failed. Please check:\n"
        "1. GROQ_API_KEY in .env file\n"
        "2. Ollama is running (ollama serve)\n"
        "3. Internet connection"
    )


# ==================== LEGACY COMPATIBILITY ====================
# For backwards compatibility with existing code
def llm_generate(prompt: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
    """
    Legacy function name - redirects to call_llm
    """
    return call_llm(prompt, temperature)


# ==================== DIAGNOSTICS ====================
def check_llm_availability() -> dict:
    """
    Check which LLM services are available
    
    Returns:
        Dictionary with availability status
    """
    return {
        "groq": {
            "available": GROQ_AVAILABLE,
            "primary_model": PRIMARY_MODEL if GROQ_AVAILABLE else None,
            "fallback_model": FALLBACK_MODEL if GROQ_AVAILABLE else None
        },
        "ollama": {
            "available": OLLAMA_AVAILABLE,
            "model": OLLAMA_MODEL if OLLAMA_AVAILABLE else None
        }
    }


# ==================== TEST ====================
if __name__ == "__main__":
    print("\n Testing LLM Configuration\n")
    
    # Check availability
    status = check_llm_availability()
    print("📊 Availability Status:")
    print(f"  Groq: {'✅' if status['groq']['available'] else '❌'}")
    print(f"  Ollama: {'✅' if status['ollama']['available'] else '❌'}")
    
    # Test generation
    test_prompt = "Explain what an AI web testing agent is in 3 lines."
    
    try:
        print(f"\n📝 Test Prompt: {test_prompt}\n")
        output = call_llm(test_prompt)
        print(f"✅ Response:\n{output}")
    
    except LLMError as e:
        print(f"❌ Error: {e}")