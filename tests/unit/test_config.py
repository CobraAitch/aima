from aima.config import Settings

def test_default_settings():
    s = Settings()
    assert s.llm_provider == "ollama"
    assert s.llm_model == "llama3.1:8b"

def test_custom_settings():
    s = Settings(llm_provider="openai", llm_model="gpt-4o")
    assert s.llm_provider == "openai"
    assert s.llm_model == "gpt-4o"

