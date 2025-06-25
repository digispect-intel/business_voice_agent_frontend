from fasthtml.common import *
from monsterui.all import *
import os
from dotenv import load_dotenv
import httpx
import json
import time 
from agent_state import get_state

# Create FastHTML app with WebSocket extension
app, rt = fast_app(exts='ws', hdrs=Theme.yellow.headers())

@app.get("/{fname:path}.{ext:static}")
def static(fname: str, ext: str):
    return FileResponse(f'{fname}.{ext}')

# Load environment variables
load_dotenv()

# Restack configuration
restack_api_endpoint = os.environ.get("RESTACK_API_ENDPOINT", "http://localhost:6233")

def create_navbar():
    return NavBar(
        A("Digispect Intelligence", href="https://digispectintelligence.com", target="_blank", rel="noopener noreferrer",
        cls="uk-visible@m hover:text-primary transition-colors duration-1000"),
        brand=H3(
            Img(src="/static/DI_logo_white.svg", alt="DI Logo", cls="w-6 h-6 mr-1 sm:mr-2"),
            "Business Voice Agent",
            cls="hover:text-primary transition-colors duration-1000 flex items-center"
        ),
        sticky=True,
        cls="px-6 py-3 shadow-sm bg-background z-50"
    )


def create_center_pane():
    return Container(
        Div(
            Div(id="speaker-status", cls="text-center mb-4 text-lg font-medium"),
            Section(
                DivCentered(
                    H3("Ready for your own AI agent?", cls="md:text-4xl"),
                        P("Contact David to create custom AI Solutions", Br(), "that ",
                        Span("transform your business", cls="color-pulse"), ".",
                        cls=(TextPresets.muted_sm, "py-2 md:text-xl")),
                    cls="text-center"
                ),
                DivCentered(
                    H5(A("david.mcgrath@digispectintelligence.com", 
                      href="mailto:david.mcgrath@digispectintelligence.com",
                      cls="text-primary hover:text-yellow-600 md:text-2xl")),
                    Div(
                        A(Button("Show Interest →", cls=(ButtonT.secondary, "mt-4")), 
                            href="https://forms.digispectintelligence.solutions/r4RzLd", 
                            target="_blank", rel="noopener noreferrer"),
                        A(Button("Visit Website →", cls=(ButtonT.secondary, "mt-4")), 
                            href="https://digispectintelligence.com/contact#overview", 
                            target="_blank", rel="noopener noreferrer"),
                        cls="flex flex-row gap-4 justify-center mt-4"
                    ),
                    cls="space-y-5"
                ),
                cls=(SectionT.muted, "p-6 rounded-lg")
            ),
            cls="space-y-2 md:space-y-6"
        ),
        cls="md:py-2 lg:py-8"
    )

def handle_api_error(endpoint_name, exception, status_code=None):
    """Centralized error handling for API calls"""
    error_message = f"Error in {endpoint_name}: {str(exception)}"
    
    # Log the error with appropriate detail level
    if status_code:
        print(f"{endpoint_name} failed with status {status_code}: {str(exception)}")
    else:
        print(error_message)
    
    # Categorize common errors for better user feedback
    if status_code == 404:
        user_message = f"The {endpoint_name} endpoint was not found"
    elif status_code == 400:
        user_message = f"Invalid request to {endpoint_name}"
    elif status_code == 401:
        user_message = "Authentication failed"
    elif status_code == 500:
        user_message = "Server error occurred"
    else:
        user_message = f"Error during {endpoint_name}"
    
    return Div(user_message, id="connection-status", cls="text-center mb-2 text-red-500")


@rt('/')
def homepage():
    # Get LiveKit credentials for direct connection
    from livekit import api

    state = get_state()
    if not state.room_name: state.update_room()

    # Get API key and secret from environment variables
    api_key = os.environ.get("LIVEKIT_API_KEY")
    api_secret = os.environ.get("LIVEKIT_API_SECRET")
    livekit_url = os.environ.get("LIVEKIT_URL")
    
    # Create the token
    token = api.AccessToken(api_key, api_secret) \
        .with_identity("user") \
        .with_name("User") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room=state.room_name,
        ))
    
    jwt = token.to_jwt()

    return Title("Business Voice Agent - Digispect Intelligence"), Container(
        create_navbar(),
        # Div(
        #     create_chat_ui(), 
        #     id="chat-container",
        #     hx_ext="ws",
        #     ws_connect="/ws"
        # ),
        Div(
            create_center_pane(),
            cls="flex items-center justify-center min-h-[calc(60vh)]"  # Center vertically
        ),
        Div(
            Div(id="connection-status", cls="text-center mb-2"),
            DivHStacked(
                Button("Start Voice Chat", id="start-chat-button", cls=ButtonT.primary, onclick="startVoiceChat()"),
                Button("End Chat", id="end-chat-button", cls=ButtonT.destructive, onclick="endVoiceChat()", style="display: none;"),
                cls="flex justify-center gap-4"
            ),
            cls="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t p-4 flex flex-col justify-center"
        ),
        Style("""
            .color-pulse {
                animation: colorPulse 10s infinite;
            }
            @keyframes colorPulse {
                0%, 30%, 100% { color: hsl(var(--text-primary)); }
                60% { color: hsl(var(--primary)); }
                90% { color: hsl(var(--primary)); }
            }
            """),
        Style("""
            #connect-button, #disconnect-button, #cleanup-button {
                transition: all 0.3s ease;
            }
            
            #disconnect-button, #cleanup-button {
                display: none;
            }
        """),

        # Add LiveKit client library
        Script(src="https://cdn.jsdelivr.net/npm/livekit-client/dist/livekit-client.umd.min.js"),
        # Add direct connection script
        Script(f"""
        let currentRoom;

        async function startVoiceChat() {{
            document.getElementById('start-chat-button').disabled = true;
            document.getElementById('connection-status').innerHTML = '<div class="text-primary">Starting agent...</div>';
            
            try {{
                const response = await fetch('/start_agent', {{method: 'POST'}});
                if (!response.ok) throw new Error('Failed to start agent');
                
                document.getElementById('connection-status').innerHTML = '<div class="text-green-500">Connecting to voice chat...</div>';
                await connectToLiveKit();
                
                document.getElementById('start-chat-button').style.display = 'none';
                document.getElementById('end-chat-button').style.display = 'block';
            }} catch (error) {{
                document.getElementById('connection-status').innerHTML = `<div class="text-red-500">Error: ${{error.message}}</div>`;
                document.getElementById('start-chat-button').disabled = false;
            }}
        }}

        async function endVoiceChat() {{
            document.getElementById('end-chat-button').disabled = true;
            document.getElementById('connection-status').innerHTML = '<div class="text-yellow-500">Ending chat...</div>';
            
            if (currentRoom) {{
                currentRoom.localParticipant.setMicrophoneEnabled(false);
                currentRoom.disconnect();
                currentRoom = null;
            }}
            
            await fetch('/cleanup_agent', {{method: 'POST'}});
            
            document.getElementById('connection-status').innerHTML = '<div class="text-gray-500">Chat ended</div>';
            document.getElementById('speaker-status').innerHTML = '';
            document.getElementById('start-chat-button').style.display = 'block';
            document.getElementById('end-chat-button').style.display = 'none';
            document.getElementById('start-chat-button').disabled = false;
            document.getElementById('end-chat-button').disabled = false;
        }}

        async function connectToLiveKit() {{
            if (!window.LivekitClient) throw new Error('LiveKit client not available');
            
            const room = new LivekitClient.Room();
            let speakerTimeout;
            
            function updateSpeakerState() {{
                const aiSpeaking = room.activeSpeakers.some(p => p.identity !== 'user');
                const userSpeaking = room.localParticipant.isSpeaking;
                if (speakerTimeout) clearTimeout(speakerTimeout);
                
                if (aiSpeaking || userSpeaking) {{
                    let state = aiSpeaking ? 'Agent Dave is speaking...' : 'Listening...';
                    document.getElementById('speaker-status').innerHTML = `<div class="text-primary">${{state}}</div>`;
                }} else {{
                    speakerTimeout = setTimeout(() => {{
                        document.getElementById('speaker-status').innerHTML = '<div class="text-gray-500">Waiting...</div>';
                    }}, 500);
                }}
            }}
            
            room.on('connected', () => {{
                document.getElementById('connection-status').innerHTML = '<div class="text-green-500">Connected to voice chat</div>';
            }});
            
            room.on('trackSubscribed', (track, publication, participant) => {{
                if (track.kind === 'audio') {{
                    const audioEl = new Audio();
                    track.attach(audioEl);
                    audioEl.volume = 1.0;
                    document.body.appendChild(audioEl);
                }}
            }});
            
            room.on('activeSpeakersChanged', updateSpeakerState);
            room.on('localTrackPublished', updateSpeakerState);
            
            await room.connect('{livekit_url}', '{jwt}');
            currentRoom = room;
            await room.localParticipant.setMicrophoneEnabled(true);
            updateSpeakerState();
        }}
        """)
    )

@rt('/start_agent', methods=['POST'])
async def start_agent():
    try:
        state = get_state()
        if not state.room_name: state.update_room()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{restack_api_endpoint}/api/agents/AgentVoice", 
                json={"input": {"room_id": state.room_name}, "action": "", "schedule": None, "taskQueue": "restack"}
            )
            
            if response.status_code != 200: return {"error": "Failed to start agent"}, 500
                
            agent_data = response.json()
            agent_id = agent_data.get('agentId')
            run_id = agent_data.get('runId')
            
            if not agent_id or not run_id: return {"error": "Agent started but returned incomplete identification"}, 500
            
            state.update_agent(agent_id, run_id)
            return {"success": True, "agent_id": agent_id, "run_id": run_id}
    except Exception as e:
        return {"error": str(e)}, 500

@rt('/cleanup_agent', methods=['POST'])
async def cleanup_agent():
    try:
        from agent_state import get_state
        state = get_state()
        
        if not state.agent_id or not state.run_id: return {"error": "No agent to clean up"}, 400
        
        async with httpx.AsyncClient() as client:
            terminate_url = f"{restack_api_endpoint}/api/engine/workflow/terminate"
            terminate_payload = {
                "workflowExecution": {"workflowId": state.agent_id, "runId": state.run_id},
                "reason": "Terminated from the frontend"
            }
            
            response = await client.post(terminate_url, json=terminate_payload)
            if response.status_code == 200:
                delete_url = f"{restack_api_endpoint}/api/engine/workflow/delete"
                delete_payload = {"workflowExecution": {"workflowId": state.agent_id, "runId": state.run_id}}
                await client.post(delete_url, json=delete_payload)
                state.reset()
                return {"success": True}
            
        return {"error": "Cleanup failed"}, 500
    except Exception as e:
        return {"error": str(e)}, 500

@app.ws('/ws')
async def ws(msg:str, send):
    print(f"WebSocket message received: {msg}")
    
    try:
        # Try to parse as JSON for structured messages
        data = json.loads(msg)
        
        # Centralized message type handler
        if "type" in data:
            message_type = data["type"]
            
            if message_type == "transcript":
                # Handle user transcript
                await send(create_chat_ui([dict(role="user", content=data["transcript"])]))
            
            elif message_type == "response":
                # Handle assistant response
                await send(create_chat_ui([dict(role="assistant", content=data["response"])]))
            
            elif message_type == "agent_status":
                # Handle agent status updates
                status_message = f"Agent {data.get('status', 'updated')}"
                await send(Div(status_message, id="connection-status", cls="text-center mb-2 text-primary"))
            
            elif message_type == "error":
                # Handle error messages
                await send(Div(f"Error: {data.get('error', 'Unknown error')}", 
                               id="connection-status", cls="text-center mb-2 text-red-500"))
        
        # Handle messages with specific fields
        elif "transcript" in data:
            await send(create_chat_ui([dict(role="user", content=data["transcript"])]))
        
        elif "response" in data:
            await send(create_chat_ui([dict(role="assistant", content=data["response"])]))
        
    except json.JSONDecodeError:
        # Handle plain text messages
        if msg == "agent_started":
            await send(Div("Connected to voice agent", id="connection-status", cls="text-green-500"))
        elif msg == "agent_ended" or msg == "connection_closed":
            await send(Div("Session ended", id="connection-status", cls="text-red-500"))
        elif msg.startswith("transcript:"):
            transcript = msg.split(":", 1)[1]
            await send(create_chat_ui([dict(role="user", content=transcript)]))
        elif msg.startswith("response:"):
            response = msg.split(":", 1)[1]
            await send(create_chat_ui([dict(role="assistant", content=response)]))


# Run the app
serve()
