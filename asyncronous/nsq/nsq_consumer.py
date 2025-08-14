import json
import os
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable
from nsqworker import nsqworker
from nsqworker.helpers import register_nsq_topics
from typing import Dict, Any
from pydantic import BaseModel
from raven import Client as RavenClient

from ctx.app_context import AppContext
from asyncronous.nsq.base_consumer import BaseConsumer
from ctx.context import get_default_context


class Payload(BaseModel):
    name: str
    timestamp: int
    data: dict

    @staticmethod
    def from_dict(payload: Dict[str, Any]) -> 'Payload':
        return Payload(
            name=payload.get("name"),
            time=payload.get("time"),
            data=payload.get("data", {})
        )

    def __repr__(self):
        return f"Payload(name={self.name}, time={self.time}, data={self.data})"


class NSQConsumer(BaseConsumer):
    def __init__(self, topic: str, channel: str, ctx: AppContext, backend_nsqd_http_addresses: list,
                 backend_lookupd_http_addresses: list, service_name: str):
        super().__init__(raven_client=RavenClient(), topic=topic, channel=channel)
        register_nsq_topics(backend_nsqd_http_addresses, [topic])
        self.backend_nsqd_http_addresses = backend_nsqd_http_addresses
        self.backend_lookupd_http_addresses = backend_lookupd_http_addresses
        self.ctx = ctx
        self.service_name = service_name

    @staticmethod
    def parse_message(message):
        decoded_body = json.loads(message.body.decode())
        return message.id, decoded_body

    def run(self):
        def handle_exc(message, e):
            self.logger.error("Failed processing message", tags={"error": str(e)}, exc_info=True)
            self.monitor.report_message_process_failure(service_topic_override=self.topic,
                                                        service_channel_override=self.channel)
            w.io_loop.add_callback(message.requeue, backoff=True, delay=-1)

        w = nsqworker.ThreadWorker(service_name=self.service_name,
                                   message_handler=self.process_message,
                                   exception_handler=handle_exc,
                                   concurrency=1,
                                   topic=self.topic,
                                   channel=self.channel,
                                   lookupd_http_addresses=self.backend_lookupd_http_addresses)
        w.subscribe_worker()

    def process_message(self, message):
        print("")


def run_consumers(ctx: AppContext, service_name: str) -> None:
    lookupd_addresses = os.getenv("LOOKUPD_HTTP_ADDRESSES").split(',')
    backend_nsqd_http_addresses = os.getenv("NSQD_TCP_ADDRESSES").split(',')
    consumers = [
        NSQConsumer(topic="topic1", channel="channel1", ctx=ctx,
                    backend_nsqd_http_addresses=backend_nsqd_http_addresses,
                    backend_lookupd_http_addresses=lookupd_addresses,
                    service_name=service_name),
    ]
    for consumer_instance in consumers:
        consumer_instance.run()


if __name__ == '__main__':
    run_consumers(ctx=get_default_context(), service_name="microservice-genai-template")
