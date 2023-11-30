from aws_cdk import (
    Stack,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_iam as iam,
    aws_sqs as sqs,
)
from constructs import Construct


class CrossAccountEventbridgeBusStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, environment: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.event_bus = events.EventBus(
            self, "CustomEventBus", event_bus_name=environment["EVENT_BUS_NAME"]
        )
        if environment.get("CROSS_ACCOUNT_EVENTBRIDGE_RULE_ROLE"):
            statement = iam.PolicyStatement(
                sid="CrossAccountPutEvents",
                actions=["events:PutEvents"],
                resources=[self.event_bus.event_bus_arn],
                principals=[
                    iam.ArnPrincipal(
                        arn=environment["CROSS_ACCOUNT_EVENTBRIDGE_RULE_ROLE"]
                    )
                ],
            )
            self.event_bus.add_to_resource_policy(statement=statement)
        self.event_rule = events.Rule(
            self,
            "EventRule",
            rule_name="match-everything",  # hard coded
            event_bus=self.event_bus,
            event_pattern=events.EventPattern(source=events.Match.prefix("")),
        )

        self.queue = sqs.Queue(
            self,
            "Queue",
            queue_name="cross-account-target-queue",  # hard coded
        )

        # connect AWS resources together
        self.event_rule.add_target(target=events_targets.SqsQueue(queue=self.queue))
