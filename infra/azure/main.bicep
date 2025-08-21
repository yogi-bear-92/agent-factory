@description('Name of the Azure Container Apps environment')
param envName string

@description('Azure region')
param location string = resourceGroup().location

@description('Container Registry name (must be globally unique)')
param acrName string

@description('Container App name')
param appName string

@description('Container image tag (e.g., latest or sha)')
param imageTag string = 'latest'

@description('Container image repository (e.g., agent-factory)')
param imageRepo string = 'agent-factory'

@description('CPU cores for the container')
param cpu double = 0.5

@description('Memory for the container (Gi)')
param memory string = '1Gi'

@description('Min replicas')
param minReplicas int = 0

@description('Max replicas')
param maxReplicas int = 2

@description('App environment variables')
param appEnv object = {
  API_HOST: '0.0.0.0'
  API_PORT: '8000'
  ENVIRONMENT: 'production'
  DEBUG: 'false'
}

var registryServer = format('{0}.azurecr.io', acrName)
var imageName = format('{0}:{1}', format('{0}/{1}', registryServer, imageRepo), imageTag)

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

resource managedEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: envName
  location: location
}

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: appName
  location: location
  properties: {
    managedEnvironmentId: managedEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
      }
      registries: [
        {
          server: registryServer
          username: acr.listCredentials().username
          passwordSecretRef: 'acr-pwd'
        }
      ]
      secrets: [
        {
          name: 'acr-pwd'
          value: acr.listCredentials().passwords[0].value
        }
      ]
      activeRevisionsMode: 'single'
      runtime: {
        secrets: []
      }
    }
    template: {
      containers: [
        {
          name: 'app'
          image: imageName
          resources: {
            cpu: cpu
            memory: memory
          }
          env: [for k in union([], [for k2 in keys(appEnv): k2]): {
            name: k
            value: appEnv[k]
          }]
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
      }
    }
  }
}

output containerAppUrl string = containerApp.properties.configuration.ingress.fqdn
