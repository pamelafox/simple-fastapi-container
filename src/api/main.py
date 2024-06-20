import random

import fastapi

from .data import names

app = fastapi.FastAPI()


@app.get("/generate_name")
async def generate_name(starts_with: str = None):
    name_choices = names
    if starts_with:
        name_choices = [name for name in name_choices if name.lower().startswith(starts_with.lower())]
    random_name = random.choice(name_choices)
    return {"name": random_name}
