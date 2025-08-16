import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env if present
load_dotenv()


class Settings(BaseModel):
	openai_api_key: str | None = None
	brave_search_api_key: str | None = None
	bing_search_api_key: str | None = None
	serpapi_api_key: str | None = None
	tavily_api_key: str | None = None

	model: str = os.getenv("GTM_AGENT_MODEL", "gpt-4o-mini")
	data_dir: Path = Path(os.getenv("GTM_AGENT_DATA_DIR", str(Path.home() / ".gtm_agent")))

	user_agent: str = "eand-gtm-agent/0.1 (+https://eand.com)"


settings = Settings(
	openai_api_key=os.getenv("OPENAI_API_KEY"),
	brave_search_api_key=os.getenv("BRAVE_SEARCH_API_KEY"),
	bing_search_api_key=os.getenv("BING_SEARCH_API_KEY"),
	serpapi_api_key=os.getenv("SERPAPI_API_KEY"),
	tavily_api_key=os.getenv("TAVILY_API_KEY"),
)

settings.data_dir.mkdir(parents=True, exist_ok=True)