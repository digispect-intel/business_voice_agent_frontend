# Agent_Dave_Frontend

**Live Example:** [AI Agent Dave](https://agent-dave.pla.sh)
**Backend Repository:** [Agent_Dave_Backend](https://github.com/digispect-intel/Agent_Dave_Backend)

A FastHTML-based frontend for Agent Dave, an AI assistant for David McGrath's business website (digispectintelligence.com). This frontend provides the user interface for interacting with Agent Dave.

## Overview

This frontend allows visitors to interact with Agent Dave, an AI assistant that can provide information about David McGrath's profile, expertise, and services at Digispect Intelligence. The application is built using FastHTML and provides voice-enabled interaction capabilities.

## Features

- Interactive UI for communicating with Agent Dave
- Voice-enabled interaction capabilities
- Information about David's profile and past experiences
- Exploration of Data Science and AI business applications
- Responsive design for all devices

## Prerequisites

- Python 3.8 or higher
- [Agent_Dave_Backend](https://github.com/digispect-intel/Agent_Dave_Backend) running locally

## Configuration

1. Copy the `.env.example` file and rename it to `.env`:

```bash
cp .env.example .env
```

2. Update the `.env` file with your LiveKit and Restack configuration:
   - `RESTACK_API_ENDPOINT`: Your Restack backend endpoint (default: http://localhost:6233)
   - `LIVEKIT_API_KEY`: Your LiveKit API key
   - `LIVEKIT_API_SECRET`: Your LiveKit API secret
   - `LIVEKIT_URL`: Your LiveKit WebSocket URL

## Installation and Setup

**Note:** Make sure to also set up and run the [Agent_Dave_Backend](https://github.com/digispect-intel/Agent_Dave_Backend) repository for the complete system.

### 1. Clone the repository

```bash
git clone https://github.com/digispect-intel/Agent_Dave_Frontend.git
cd Agent_Dave_Frontend
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the frontend

```bash
python main.py
```

The application will be available at http://localhost:5001 (or the port specified in your FastHTML configuration).

## Usage

1. Ensure the [Agent_Dave_Backend](https://github.com/digispect-intel/Agent_Dave_Backend) is running
2. Start the frontend application using the steps above
3. Open your browser to the local URL
4. Click "Start Voice Chat" to begin interacting with Agent Dave
5. Speak naturally to ask questions about David's expertise and services
6. Click "End Chat" when you're finished

## Integration with Backend

This frontend connects with the [Agent_Dave_Backend](https://github.com/digispect-intel/Agent_Dave_Backend) repository to provide a complete AI assistant experience. The backend handles the voice processing pipeline and AI model integration.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, contact david.mcgrath@digispectintelligence.com

## References

This repo is based on the examples here:
- https://github.com/AnswerDotAI/fasthtml-example
- https://github.com/restackio/examples-python/tree/main/agent_voice/livekit
- https://github.com/livekit/agents/tree/main/examples/voice_agents
- https://github.com/livekit/client-sdk-js/tree/main/examples