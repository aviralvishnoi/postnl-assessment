#!/usr/bin/env python3
import os

import aws_cdk as cdk

from postnl_event_broker_poc.postnl_event_broker_poc_stack import (
    PostnlEventBrokerPocStack,
)


app = cdk.App()
PostnlEventBrokerPocStack(
    app,
    "PostnlEventBrokerPocStack",
    synthesizer=cdk.DefaultStackSynthesizer(
        # synthesizer properties
        file_assets_bucket_name="cdk-aviral-bootstrap"
    ),
)

app.synth()
