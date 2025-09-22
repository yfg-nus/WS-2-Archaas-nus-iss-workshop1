# ARCHAAS NUS-ISS Workshop 1: Prompt Engineering & AI Agents

## Overview

This repository contains the materials for **Day 1** of the **Architecting Agentic AI Systems (ARCHAAS)** workshop series at NUS-ISS. The workshop focuses on prompt engineering fundamentals, AI agents development, and practical applications using various AI platforms.

## Workshop Structure

###  Learning Modules

1. **`prompt_engineering_day1_workshop.ipynb`** - Core prompt engineering concepts
   - Basic principles of prompt engineering
   - Message format and role understanding
   - Model parameters (temperature, max_tokens, stop_sequences)
   - System prompts and best practices
   - API integration with OpenAI and Anthropic

2. **`agents101_openAI_day1_workshop.ipynb`** - AI Agents with OpenAI Agents SDK
   - Introduction to AI agents
   - OpenAI Agents SDK setup and configuration
   - Agent creation and deployment
   - WebSearchTool integration
   - Structured outputs with Pydantic models
   - Agent tracing and monitoring

3. **`prompt_engineering_amazon_bedrock_day1_workshop.ipynb`** - Amazon Bedrock Integration
   - Amazon Bedrock API fundamentals
   - Multi-model inference capabilities
   - Converse API vs Invoke API
   - Function calling with Bedrock
   - Cross-regional inference
   - Streaming responses

4. **`prompt_engineering_reasoning_models_day1_workshop.ipynb`** - Reasoning Models (o1/gpt-5)
   - Introduction to reasoning models
   - 4 principles of prompting with o1 models
   - Structured formats and few-shot learning
   - Domain-specific reasoning tasks
   - Performance optimization techniques

5. **`individual_assignment_day1.ipynb`** - Individual Assignment
   - Comprehensive assignment covering all workshop topics
   - Tool use with Wikipedia integration
   - AI agent development
   - Advanced prompt engineering techniques
   - Integration challenges

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (recommended: Python 3.9 or 3.10)
- **Jupyter Notebook** or **JupyterLab**
- **Git** for cloning the repository

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd archaas-nus-iss-workshop1
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Using venv
   python -m venv archaas_env
   
   # Activate virtual environment
   # On Windows:
   archaas_env\Scripts\activate
   # On macOS/Linux:
   source archaas_env/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

   Or install packages individually:
   ```bash
   pip install openai anthropic python-dotenv jupyter
   pip install agents pydantic requests wikipedia-api
   pip install boto3 botocore IPython
   ```

### Configuration

1. **Create environment file**
   ```bash
   # Create .env file in the project root
   touch .env
   ```

2. **Add your API keys** to the `.env` file:
   ```env
   # Required API Keys
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   
   # Optional: AWS Bedrock (if you have access)
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_DEFAULT_REGION=us-east-1
   ```

3. **Get API Keys**
   - **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - **Anthropic**: [https://console.anthropic.com/](https://console.anthropic.com/)
   - **AWS Bedrock**: [https://aws.amazon.com/bedrock/](https://aws.amazon.com/bedrock/)

### Running the Workshop

1. **Start Jupyter**
   ```bash
   jupyter notebook
   # or
   jupyter lab
   ```

2. **Open notebooks in order**:
   - Start with `prompt_engineering_day1_workshop.ipynb`
   - Continue with `agents101_openAI_day1_workshop.ipynb`
   - Explore `prompt_engineering_amazon_bedrock_day1_workshop.ipynb`
   - Practice with `prompt_engineering_reasoning_models_day1_workshop.ipynb`
   - Complete the `individual_assignment_day1.ipynb`

##  Required Libraries

### Core Libraries
- **`openai`** - OpenAI API client for GPT models
- **`anthropic`** - Anthropic API client for Claude models
- **`python-dotenv`** - Environment variable management
- **`jupyter`** - Jupyter notebook environment

### AI Agents & Tools
- **`agents`** - OpenAI Agents SDK for AI agent development
- **`pydantic`** - Data validation and settings management
- **`requests`** - HTTP library for API calls
- **`wikipedia-api`** - Wikipedia API integration

### AWS & Cloud Services
- **`boto3`** - AWS SDK for Python
- **`botocore`** - Low-level AWS service access

### Display & Utilities
- **`IPython`** - Enhanced interactive Python shell
- **`matplotlib`** - Plotting library (optional)
- **`pandas`** - Data manipulation (optional)

##  Setup Instructions by Module

### Module 1: Prompt Engineering Fundamentals
```python
# Required imports
import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

### Module 2: AI Agents
```python
# Required imports
from agents import Agent, WebSearchTool, trace, Runner
from pydantic import BaseModel, Field

# Note: WebSearchTool has associated costs (~2.5 cents per call)
```

### Module 3: Amazon Bedrock
```python
# Required imports
import boto3
import json

# Initialize Bedrock client
bedrock = boto3.client(service_name='bedrock-runtime')
```

### Module 4: Reasoning Models
```python
# Required imports
from openai import OpenAI
from IPython.display import display, Markdown, HTML

# Access reasoning models (o1, gpt-5)
```

## 💰 Cost Considerations

### OpenAI API Costs
- **GPT-4o**: ~$0.005 per 1K input tokens, ~$0.015 per 1K output tokens
- **GPT-4o-mini**: ~$0.00015 per 1K input tokens, ~$0.0006 per 1K output tokens
- **WebSearchTool**: ~$0.025 per search call

### Anthropic API Costs
- **Claude 3.5 Sonnet**: ~$0.003 per 1K input tokens, ~$0.015 per 1K output tokens
- **Claude 3.5 Haiku**: ~$0.00025 per 1K input tokens, ~$0.00125 per 1K output tokens

### AWS Bedrock Costs
- Varies by model and region
- Check [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) for details

## ️ Troubleshooting

### Common Issues

1. **API Key Errors**
   ```bash
   # Verify your .env file exists and contains valid keys
   cat .env
   ```

2. **Import Errors**
   ```bash
   # Reinstall packages
   pip install --upgrade openai anthropic python-dotenv
   ```

3. **Jupyter Kernel Issues**
   ```bash
   # Restart kernel or reinstall jupyter
   pip install --upgrade jupyter
   ```

4. **AWS Bedrock Access**
   - Ensure you have proper AWS credentials
   - Verify Bedrock service is enabled in your region
   - Check IAM permissions for Bedrock access

### Environment Verification
```python
# Test script to verify setup
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Test OpenAI
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello!"}],
        max_tokens=10
    )
    print("✅ OpenAI API working")
except Exception as e:
    print(f"❌ OpenAI API error: {e}")

# Test Anthropic
try:
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    print("✅ Anthropic API configured")
except Exception as e:
    print(f"❌ Anthropic API error: {e}")
```

## 📋 Workshop Agenda

### Day 1 Schedule
- **Morning Session**: Prompt Engineering Fundamentals
- **Afternoon Session**: AI Agents & Tools
- **Evening Session**: Advanced Topics & Assignment

### Learning Objectives
- Master prompt engineering techniques
- Build and deploy AI agents
- Integrate multiple AI platforms
- Apply concepts to real-world scenarios

## 📚 Additional Resources

### Documentation
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [OpenAI Agents SDK](https://github.com/openai/agents)

### Community & Support
- [NUS-ISS Learning Hub](https://www.iss.nus.edu.sg/)
- [OpenAI Community Forum](https://community.openai.com/)
- [Anthropic Discord](https://discord.gg/anthropic)

## 📄 License

This workshop material is provided for educational purposes. Please respect the terms of service for all APIs used.

## 🤝 Contributing

For questions or issues related to this workshop, please contact the NUS-ISS team.

---

**Happy Learning! 🚀**

*Last updated: 28 August 2025
