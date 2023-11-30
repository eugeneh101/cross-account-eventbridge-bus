import aws_cdk as cdk

from cross_account_eventbridge_bus import CrossAccountEventbridgeBusStack


app = cdk.App()
environment = app.node.try_get_context("environment")
CrossAccountEventbridgeBusStack(
    app,
    "CrossAccountEventbridgeBusStack",
    env=cdk.Environment(region=environment["AWS_REGION"]),
    environment=environment,
)
app.synth()
