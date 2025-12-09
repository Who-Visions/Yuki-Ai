from vertexai.preview import reasoning_engines
import vertexai
import logging
from agent import YukiAgent
from tools import get_current_time, add_numbers

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
STAGING_BUCKET = "gs://gifted-cooler-479623-r7-yuki-staging"
LOCATION = "us-central1"

def deploy():
    vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

    print(f"Deploying Yuki Agent to {LOCATION}...")

    # Instantiate the local agent
    agent = YukiAgent(
        model="gemini-2.0-flash-exp",
        tools=[get_current_time, add_numbers],
        project=PROJECT_ID,
        location=LOCATION,
    )
    
    # Initialize the agent
    agent.set_up()
    
    # Deploy the agent
    remote_agent = reasoning_engines.ReasoningEngine.create(
        agent,
        requirements=[
            "cloudpickle",
            "langchain-core",
            "langchain",
            "langchain-google-vertexai>=2.0.0",
            "langgraph",
            "google-cloud-aiplatform>=1.70.0",
            "google-auth",
            "google-cloud-secret-manager",
            "google-cloud-vertexai"
        ],
        display_name="Yuki V.005",
        description="Custom agent Yuki V.005 with Nano Banana capabilities.",
    )

    print("Deployment complete!")
    print(f"Resource Name: {remote_agent.resource_name}")
    return remote_agent

if __name__ == "__main__":
    deploy()
