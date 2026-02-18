docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

#### Open web UI 
-->     It is an ui layer for ollama 

docker pull ghcr.io/open-webui/open-webui:main

docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main



docker stop open-webui ollama
docker start open-webui

------------------------------------------------------------------------------

docker pull ollama/ollama

docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

docker exec -it ollama ollama run llama3.2

docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main-slim
