from ._base import BaseRequestUseCase
from modules.request.domain.commands import (
    AddComment as AddCommentCommand,
)
from modules.request.domain.ports.inbound import IAddComment
from modules.request.application.errors import RequestNotFoundError, NoRightsError
from modules.request.domain.value_objects import Comment, CommentAuthor


class AddComment(BaseRequestUseCase, IAddComment):
    async def __call__(self, command: AddCommentCommand) -> None:
        request = await self._request_repository.find_by_id(command.request_id)

        if request is None:
            raise RequestNotFoundError(
                f"Request with id {command.request_id} not found"
            )

        if (
            request.queue.owner_id != command.requester
            and request.user_id != command.requester
        ):
            raise NoRightsError(
                f"User {command.requester.value} has no rights to reject request {command.request_id}"
            )

        request.add_comment(
            Comment(
                text=command.text,
                author=CommentAuthor.QUEUE_OWNER
                if request.queue.owner_id == command.requester
                else CommentAuthor.VISITER,
            )
        )

        await self._request_repository.save(request)
        await self._publish_events(request)
