# ymzk_agent


https://ollama.com/ 

```bash


mkdir .venv
python3 -m venv .venv

source .venv/bin/activate

pip install git+https://github.com/geekan/MetaGPT


metagpt "Create a 2048 game"




```



`/Users/qi/.metagpt/config2.yaml` 
```yaml
llm:
  api_type: "ollama"  # or azure / ollama / open_llm etc. Check LLMType for more options
  model: "codellama"  # or gpt-3.5-turbo-1106 / gpt-4-1106-preview
  base_url: "http://127.0.0.1:11434/api"  # or forward url / other llm url
  api_key: "test"
repair_llm_output: true
```


