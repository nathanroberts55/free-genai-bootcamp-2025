# OPEA Comps

## Ollama

Using the [Ollama Third Party Deployment Compose](https://github.com/opea-project/GenAIComps/blob/main/comps/third_parties/ollama/deployment/docker_compose/compose.yaml):

```yml
# Copyright (C) 2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

services:
  ollama-server:
    image: ollama/ollama
    container_name: ollama-server
    ports:
      - ${LLM_ENDPOINT_PORT:-8008}:11434
    environment:
      no_proxy: ${no_proxy}
      http_proxy: ${http_proxy}
      https_proxy: ${https_proxy}
      LLM_MODEL_ID: ${LLM_MODEL_ID}
      host_ip: ${host_ip}

networks:
  default:
    driver: bridge
```

### Changes made to the Compose

Went to the [Ollama site](https://ollama.com/) and went to model to get the [ollama 3.21b](https://ollama.com/library/llama3.2:1b) that Andrew mentioned from the video.

Also I updated the `host_ip` to use `localhost`, which I beleieve 

### Pulling a Model

```powershell
$body = @{
    model = "llama3.2:1b"
} | ConvertTo-Json -Compress

Invoke-RestMethod -Method Post -Uri "http://localhost:8008/api/pull" -Body $body -ContentType "application/json"
```

### Testing the LLM locally

```powershell
$body = @{
    model = 'llama3.2:1b'
    prompt = "Why is the sky blue?"
} | ConvertTo-Json -Compress  

Invoke-RestMethod -Method Post -Uri "http://localhost:8008/api/generate" -Body $body -ContentType "application/json"
```

## Technical Uncertainty

Q. Can I do this on windows? Andrew said that it's not supported, and I have WSL, but to me the point of containerization is that it doesn't matter the system that I am developing on. Am I asking for a world of pain, probably... but we'll see.

Q. I know I saw in the video that Andrew used the IP of machine (I believe the public IP address), but I want to know if I can just use localhost to run the container on the port. I think I will be able to access the API on `localhost:8008`.

A. That all seems to work fine!

Q. Do we need to pull the model to the container before we can generate a request? I thought I had set the container up correctly the first time learning from Andrew's mistake in the videos, but maybe pulling the model from the container first is an important first step.

A. So running the pull command does seem to be a necessary first step in the deployment process, might be cool to add that step into the docker compose so that the container is ready once it is deployed to accept the request that we were trying to send.
