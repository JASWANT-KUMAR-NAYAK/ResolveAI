from sqlalchemy.orm import Session

from app.models.issue import Issue
from app.schemas.conversation import ConversationResponse, ProposedChange


class ConversationService:
    def __init__(self, db: Session):
        self.db = db

    def propose_change(
        self,
        issue: Issue,
        message: str,
    ) -> ConversationResponse:
        changes: list[ProposedChange] = []

        normalized_message = message.lower()

        if "priority" in normalized_message:
            if "high" in normalized_message:
                changes.append(
                    ProposedChange(
                        field="priority",
                        old_value=issue.priority,
                        new_value="HIGH",
                        reason="The user requested high priority.",
                    )
                )
            elif "medium" in normalized_message:
                changes.append(
                    ProposedChange(
                        field="priority",
                        old_value=issue.priority,
                        new_value="MEDIUM",
                        reason="The user requested medium priority.",
                    )
                )
            elif "low" in normalized_message:
                changes.append(
                    ProposedChange(
                        field="priority",
                        old_value=issue.priority,
                        new_value="LOW",
                        reason="The user requested low priority.",
                    )
                )

        return ConversationResponse(
            message="I prepared the requested change for review.",
            changes=changes,
            requires_confirmation=True,
        )