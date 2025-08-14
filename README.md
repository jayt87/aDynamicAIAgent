# aDynamicAIAgent

Multi-agent AI system using LangGraph's supervisor-worker pattern for dynamic task planning and execution.

## Overview

A **Supervisor Agent** creates execution plans and delegates tasks to a **Worker Agent**. The supervisor monitors progress and synthesizes responses while the worker executes steps without memory between iterations.

## Features

- Dynamic planning with step-by-step execution
- Supervisor-worker collaboration pattern
- Memory management with conversation checkpointing
- Multiple Azure OpenAI models (GPT-5, GPT-4.1, O1-Mini, O3-Pro, Grok)
- Conditional routing and termination logic

## Architecture

**Supervisor**: Creates plans, monitors progress, provides context, synthesizes final answers
**Worker**: Executes assigned tasks statelessly with supervisor-provided context

## Setup

**Requirements**: Python 3.8+, Azure OpenAI API access

1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` file:
```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

## Usage

Run: `python main.py`

### Available Models
- `llm5`: GPT-5 (primary)
- `llm5mini`: GPT-5 Mini  
- `llm41`: GPT-4.1
- `llm_reasoning04mini`: O1-Mini
- `llm_reasoning03pro`: O3-Pro
- `grokllm`: Grok-3

### Customization
- Edit `SUPERVISOR_PROMPT` in `prompts.py` for planning strategy
- Modify routing logic in `main.py` for termination conditions

## How It Works

1. User submits query
2. Supervisor creates numbered execution plan (max 5 steps) 
3. Supervisor assigns tasks to worker with context
4. Worker executes and returns results
5. Process repeats until completion
6. Supervisor synthesizes final answer

## Safety Features

- Auto-termination after 90 messages
- Explicit "END WORKER NOW" signal
- "PLAN GENERATED" confirmation tracking