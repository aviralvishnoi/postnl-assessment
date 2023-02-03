from aws_cdk import aws_sqs as _sqs
from constructs import Construct
from dataclasses import dataclass

@dataclass
class SQSProps:
    queue_name: str
    dead_letter_queue_name: str


class SQS(Construct):

    def __init__(self, scope: "Construct", id: str, props: SQSProps) -> None:
        super().__init__(scope, id)
        SQS.__eb_sqs = self.create_sqs(props)

    @property
    def get_queue_object(self):
        return SQS.__eb_sqs
        
    @property
    def get_queue_url(self):
        return SQS.__eb_sqs.queue_url

    @property
    def get_queue_arn(self):
        return SQS.__eb_sqs.queue_arn

    def create_sqs(self, props):
        sqs_queue = _sqs.Queue(
            self,
            id="EBProducerFifoQueue",
            queue_name=f"{props.queue_name}",
            fifo=True,
            content_based_deduplication = True,
            dead_letter_queue = _sqs.DeadLetterQueue(
                max_receive_count=3,
                queue= self.create_dlq(props)
            )

        )
        return sqs_queue

    def create_dlq(self, props):
        dlq = _sqs.Queue(
            self,
            id="EBProducerDeadLetterQueue",
            queue_name=f"{props.dead_letter_queue_name}",
            fifo=True,
            content_based_deduplication = True,
        )
        return dlq