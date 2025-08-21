# Azure Setup (AI Foundry + Container Apps)

This guide helps you configure:
- Azure AI Foundry (Azure OpenAI) as your LLM provider
- Deploy this project to Azure Container Apps via GitHub Actions

Prerequisites:
- Azure subscription with permissions to create ACR and Container Apps
- GitHub repository with Actions enabled
- Node/npm if you want to use the Claude Code CLI locally

## 1) Azure AI Foundry (Azure OpenAI)

1. Create or select an Azure AI Foundry Hub and Project.
2. In the Project, deploy a model (e.g., gpt-4o-mini) and note the Deployment Name.
3. Find your Endpoint and API Key in Azure AI Foundry > Project > Deployments or Keys.
4. Update your `.env`:
   - AZURE_OPENAI_ENDPOINT
   - AZURE_OPENAI_API_KEY
   - AZURE_OPENAI_DEPLOYMENT
   - AZURE_OPENAI_API_VERSION (optional, default 2024-05-01-preview)

Optional: switch your app to prefer Azure in code paths by setting LLM_PROVIDER=azure or by directly calling the helper in `src/agent_factory/llm/azure_openai.py`.

Quick example usage:

```python
from agent_factory.llm.azure_openai import chat_completion

reply = chat_completion([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Say hello from Azure!"},
])
print(reply)
```

Ensure you have `openai>=1.0` installed (already in pyproject).

## 2) Containerizing and Deploying to Azure Container Apps

We ship a Dockerfile and a Bicep template.

- Dockerfile runs a minimal FastAPI app available at `/healthz`.
- Bicep (`infra/azure/main.bicep`) provisions:
  - Azure Container Registry (ACR)
  - Container Apps Environment
  - Container App with your image

### GitHub Actions CI/CD

Workflow: `.github/workflows/azure-deploy.yml`

Set these repository secrets:
- AZURE_CREDENTIALS: output of `az ad sp create-for-rbac --name <name> --role contributor --scopes /subscriptions/<SUBSCRIPTION_ID> --sdk-auth` (JSON)
- AZURE_SUBSCRIPTION_ID
- AZURE_RESOURCE_GROUP
- AZURE_LOCATION (e.g., eastus)
- AZURE_CONTAINERAPPS_ENVIRONMENT (name for your Container Apps env)
- ACR_NAME (globally unique)
- APP_NAME (container app name)

On push to `main` the workflow will:
- Login to Azure
- Build and push the Docker image to ACR
- Deploy/update infra using Bicep
- Output your container app FQDN

### Local test

```bash
uv run uvicorn api.rest.app:app --host 0.0.0.0 --port 8000
curl http://localhost:8000/healthz
```

### Notes
- Modify `infra/azure/main.bicep` to add secrets/env for production.
- For Redis or other dependencies, add corresponding Azure resources and env vars.
