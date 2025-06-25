import uuid

def generate_room_id(): return f"agent-dave-{uuid.uuid4().hex[:12]}"

class AgentState:
    """Singleton class to manage agent state"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentState, cls).__new__(cls)
            cls._instance.agent_id = None
            cls._instance.run_id = None
            cls._instance.room_name = None
            cls._instance.is_connected = False
            cls._instance.is_agent_active = False
        return cls._instance
    
    def update_agent(self, agent_id, run_id):
        """Update agent identification"""
        self.agent_id = agent_id
        self.run_id = run_id
        self.is_agent_active = True
    
    def update_room(self, room_name=None, connected=True):
        """Update room connection status"""
        self.room_name = room_name or generate_room_id()
        self.is_connected = connected
    
    def reset(self):
        """Reset all state"""
        self.agent_id = None
        self.run_id = None
        self.is_connected = False
        self.is_agent_active = False
        self.room_name = None
    
    def get_connection_state(self):
        """Get the current connection state"""
        if not self.is_agent_active:
            return "disconnected"
        elif self.is_agent_active and not self.is_connected:
            return "agent_started" if not self.is_connected else "disconnected_with_agent"
        else:
            return "connected"

# Create a global instance
state = AgentState()

# Export for use in other files
def get_state():
    return state
