

run ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh

sudo nano /etc/systemd/system/ollama.service

"OLLAMA_HOST=0.0.0.0" in environment


sudo systemctl daemon-reload
sudo systemctl restart ollama

```



对于每个环境变量，在[Service]部分下添加一行Environment：

[Service]
Environment="OLLAMA_HOST=0.0.0.0"