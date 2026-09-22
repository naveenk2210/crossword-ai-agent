import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("NEBIUS_API_KEY")
base_url = os.getenv(
    "NEBIUS_BASE_URL",
    "https://api.tokenfactory.nebius.com/v1",
)

if not api_key:
    raise RuntimeError("NEBIUS_API_KEY is missing from the .env file.")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


def main():
    print("Available Nebius models:\n")

    models = client.models.list()

    for model in models.data:
        print(model.id)


if __name__ == "__main__":
    main()
