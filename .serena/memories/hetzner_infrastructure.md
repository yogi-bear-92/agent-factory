# Hetzner Infrastructure Setup

## Account Information
- **API Token**: Available in external context
- **SSH Key**: v.jankovic992@gmail.com (ID: 101044941)
- **Account Status**: Valid and active

## Current Servers

### 1. feeder-hetzner (Existing)
- **Server ID**: 42992671
- **Type**: CCX23 (Dedicated CPU server - very powerful)
- **Status**: Running
- **Location**: Falkenstein (fsn1)
- **Created**: 2024-02-05
- **Monthly Cost**: €0 (likely prepaid or special pricing)

### 2. archon-supabase-dev (New)
- **Server ID**: 107124016
- **Type**: CPX31 (4 vCPU, 8GB RAM, 160GB Disk)
- **Status**: Running
- **Location**: Falkenstein (fsn1)
- **Purpose**: Self-hosted Archon + Supabase stack
- **Monthly Cost**: ~€13-15
- **Created**: 2025-08-21

## Server Setup Details

### archon-supabase-dev Configuration
- **OS**: Ubuntu 22.04
- **Pre-installed Software**:
  - Docker & Docker Compose
  - Git, PostgreSQL client
  - Development tools (vim, htop, etc.)
  - UFW firewall (pre-configured)
- **Swap**: 4GB swap file for memory flexibility
- **Repositories Cloned**:
  - `/root/archon` - Archon application
  - `/root/supabase` - Supabase self-hosted setup

### Firewall Rules
- SSH (22)
- HTTP (80) & HTTPS (443)
- Archon UI (3737)
- Archon Server (8181)
- Archon MCP (8051)
- Archon Agents (8052)
- Supabase Studio (54321)
- Supabase Kong (54322)

## Available Resources
- **Data Centers**: 6 locations (Germany, Finland, USA, Singapore)
- **Server Types**: Multiple options from €4/month upwards
- **OS Images**: 25+ options including Ubuntu, Debian, Rocky Linux

## Key Files Created
- `check-hetzner-account.py` - Account status checker
- `create-archon-server-v2.py` - Server creation script
- `archon-setup-guide.md` - Complete setup instructions
- `archon-server-info.json` - Server connection details
- `hetzner-dev-setup.md` - General Hetzner development guide