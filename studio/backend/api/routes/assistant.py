"""Assistant API routes."""

from fastapi import APIRouter


from studio.backend.schemas.assistant import (
    AssistantRequest,
    AssistantResponse,
)


from studio.backend.services.assistant.service import (
    assistant_service,
)



router = APIRouter(
    prefix="/assistant",
    tags=[
        "assistant"
    ],
)



@router.post(
    "/ask",
    response_model=AssistantResponse,
)
def ask(
    request: AssistantRequest,
):

    return assistant_service.ask(
        request.question
    )
