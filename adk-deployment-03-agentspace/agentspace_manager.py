import json
import requests
from google import auth as google_auth
from google.auth.transport import requests as google_requests
from urllib.parse import urlencode

class AgentspaceManager:
    """
    A class to manage Agentspace agents and authorizations via the Discovery Engine API,
    using the 'requests' library for HTTP communication.
    """

    def __init__(self, project_id: str, app_id: str):
        """
        Initializes the AgentspaceManager.

        Args:
            project_id: The ID of your Google Cloud project. 
            app_id: The ID of the Agentspace app. 
        """
        self.project_id = project_id
        self.app_id = app_id
        self.base_url = "https://discoveryengine.googleapis.com/v1alpha"

    def _get_access_token(self) -> str:
        try:
            credentials, _ = google_auth.default()
            auth_request = google_requests.Request()
            credentials.refresh(auth_request)
            print("Successfully refreshed identity token.")
            return credentials.token
        except Exception as e:
            print(f"FATAL: Could not get Google credentials. "
                f"Ensure you have run 'gcloud auth application-default login'. Error: {e}")
            # In a real test, you might want to exit if auth fails globally.
            return None

    def _execute_request(self, method: str, url: str, data: dict = None) -> dict:
        """
        Executes an HTTP request using the requests library.

        Args:
            method: The HTTP method (e.g., 'POST', 'GET', 'DELETE', 'PATCH').
            url: The API endpoint URL.
            data: The JSON payload for the request.

        Returns:
            The JSON response from the API.
        """
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json",
            "X-Goog-User-Project": self.project_id,
        }
        print(self._get_access_token())

        try:
            response = requests.request(method, url, headers=headers, json=data)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            if response.text:
                return response.json()
            return {}
        except requests.exceptions.RequestException as e:
            print(f"Error executing request: {e}")
            raise

    def create_authorization(self, auth_id: str, client_id: str, client_secret: str, auth_uri: str, token_uri: str) -> dict:
        """
        Creates an authorization resource in Agentspace. 

        Args:
            auth_id: The ID of the authorization resource. 
            client_id: The OAuth 2.0 client ID. 
            client_secret: The OAuth 2.0 client secret. 
            auth_uri: The endpoint for obtaining an authorization code. 
            token_uri: The endpoint for exchanging an authorization code for an access token. 

        Returns:
            The created authorization resource.
        """
        url = f"{self.base_url}/projects/{self.project_id}/locations/global/authorizations?authorizationId={auth_id}"
        payload = {
            "name": f"projects/{self.project_id}/locations/global/authorizations/{auth_id}", # 
            "serverSideOauth2": {
                "clientId": client_id, # 
                "clientSecret": client_secret, # 
                "authorizationUri": auth_uri, # 
                "tokenUri": token_uri # 
            }
        }
        return self._execute_request('POST', url, data=payload)

    def generate_auth_uri(self, base_auth_uri: str, client_id: str, scopes: list[str]) -> str:
        """
        Generates the complete authorization URI with the necessary parameters.

        This function constructs the URI based on the example provided in the document,
        which includes static parameters for the OAuth 2.0 flow like response_type,
        access_type, and prompt.

        Args:
            base_auth_uri: The base endpoint for the authorization server,
                        e.g., 'https://accounts.google.com/o/oauth2/v2/auth'.
            client_id: The OAuth 2.0 client identifier issued to the client.
            scopes: A list of strings representing the access scopes required by the application.

        Returns:
            A fully constructed authorization URI string.
        """
        # The example URI specifies multiple scopes separated by a space.
        encoded_scopes = " ".join(scopes)

        params = {
            'client_id': client_id,
            'scope': encoded_scopes,
            'include_granted_scopes': 'true',
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent'
        }

        # The final URI is constructed by appending the URL-encoded parameters.
        return f"{base_auth_uri}?{urlencode(params)}"

    def delete_authorization(self, auth_id: str) -> dict:
        """
        Deletes an existing authorization resource. 

        Args:
            auth_id: The ID of the authorization resource to delete. 

        Returns:
            The response from the API.
        """
        url = f"{self.base_url}/projects/{self.project_id}/locations/global/authorizations?authorizationId={auth_id}" # 
        return self._execute_request('DELETE', url)

    def register_agent(self, display_name: str, description: str, tool_description: str, adk_deployment_id: str, icon_uri: str = None, auth_ids: list = None) -> dict:
        """
        Registers a new agent with Agentspace. 

        Args:
            display_name: The display name of the agent. 
            description: The description of the agent for the user. 
            tool_description: The description of the agent for the LLM. 
            adk_deployment_id: The ID of the reasoning engine endpoint. 
            icon_uri: The public URI of the agent's icon. 
            auth_ids: A list of authorization resource IDs. 

        Returns:
            The created agent resource. 
        """
        url = f"{self.base_url}/projects/{self.project_id}/locations/global/collections/default_collection/engines/{self.app_id}/assistants/default_assistant/agents"

        # Define the core structure of adk_agent_definition
        adk_definition = {
            "tool_settings": {
                "tool_description": tool_description
            },
            "provisioned_reasoning_engine": {
                "reasoning_engine": f"projects/{self.project_id}/locations/global/reasoningEngines/{adk_deployment_id}"
            }
        }

        # Add optional authorizations directly to the adk_agent_definition
        if auth_ids:
            adk_definition["authorizations"] = [f"projects/{self.project_id}/locations/global/authorizations/{auth_id}" for auth_id in auth_ids]

        # Assemble the final top-level payload
        payload = {
            "displayName": display_name,
            "description": description,
            "adk_agent_definition": adk_definition
        }

        # Add optional icon to the top-level payload
        if icon_uri:
            payload["icon"] = {"uri": icon_uri}
        print(payload)
        return self._execute_request('POST', url, data=payload)

    def update_agent(self, agent_resource_name: str, display_name: str, description: str, tool_description: str, adk_deployment_id: str) -> dict:
        """
        Updates the registration of an existing agent. 

        Args:
            agent_resource_name: The resource name of the agent to update. 
            display_name: The display name of the agent. 
            description: The description of the agent. 
            tool_description: The description/prompt for the LLM. 
            adk_deployment_id: The ID of the reasoning engine endpoint. 

        Returns:
            The updated agent resource.
        """
        url = f"{self.base_url}/{agent_resource_name}" # 
        payload = {
            "displayName": display_name, # 
            "description": description, # 
            "adk_agent_definition": {
                "tool_settings": {
                    "tool_description": tool_description # 
                },
                "reasoning_engine": f"projects/{self.project_id}/locations/global/reasoningEngines/{adk_deployment_id}" # 
            }
        }
        return self._execute_request('PATCH', url, data=payload)

    def get_agent(self, agent_resource_name: str) -> dict:
        """
        Views a registered agent. 

        Args:
            agent_resource_name: The resource name of the agent to view. 

        Returns:
            The agent resource.
        """
        url = f"{self.base_url}/{agent_resource_name}" # 
        return self._execute_request('GET', url)

    def list_agents(self) -> dict:
        """
        Lists all registered agents. 

        Returns:
            A list of agent resources.
        """
        url = f"{self.base_url}/projects/{self.project_id}/locations/global/collections/default_collection/engines/{self.app_id}/assistants/default_assistant/agents" # 
        return self._execute_request('GET', url)

    def delete_agent(self, agent_resource_name: str) -> dict:
        """
        Deletes the registration of an agent. 

        Args:
            agent_resource_name: The resource name of the agent to delete. 

        Returns:
            The response from the API.
        """
        url = f"{self.base_url}/{agent_resource_name}" # 
        return self._execute_request('DELETE', url)

    def get_answers_from_agent(self, query: str, agent_resource_name: str) -> dict:
        """
        Gets answers from an agent using the assistant API. 

        Args:
            query: The user's query. 
            agent_resource_name: The resource name of the registered agent. 

        Returns:
            The response from the agent.
        """
        url = f"{self.base_url}/projects/{self.project_id}/locations/global/collections/default_collection/engines/{self.app_id}/assistants/default_assistant:streamAssist" # 
        payload = {
            "name": f"projects/{self.project_id}/locations/global/collections/default_collection/engines/{self.app_id}/assistants/default_assistant", # 
            "query": {
                "text": query # 
            },
            "session": f"projects/{self.project_id}/locations/global/collections/default_collection/engines/{self.app_id}/sessions/-", # 
            "assistSkippingMode": "REQUEST_ASSIST", # 
            "answerGenerationMode": "AGENT", # 
            "agentsConfig": {
                "agent": agent_resource_name # 
            }
        }
        return self._execute_request('POST', url, data=payload)