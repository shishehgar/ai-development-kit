"""Assistant API routes."""

from __future__ import annotations


from fastapi import (
    APIRouter,
)


from studio.backend.schemas.assistant import (
    AssistantAskRequest,
    AssistantAskResponse,
)


from studio.backend.core.dependencies import (
    get_ai_assistant_service,
)



router = APIRouter(
    prefix="/assistant",
    tags=["assistant"],
)



@router.post(
    "/ask",
    response_model=AssistantAskResponse,
)
def ask_assistant(
    payload: AssistantAskRequest,
):

    service = get_ai_assistant_service(
        payload.project
    )


    result = service.ask(
        payload.question
    )


    return AssistantAskResponse(

        answer=result.answer,

        provider=result.provider,

        question=payload.question,

        project=payload.project,

    )
