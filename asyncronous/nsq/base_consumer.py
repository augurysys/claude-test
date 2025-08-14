import os
import logging
from abc import ABC
import signal
import requests
from raven import Client as RavenClient

from asyncronous.nsq.nsq_utils import retry_with_timeout_wrapper
from utils.log_wrapper import LogWrapper
from utils.logger import get_logger


class BaseConsumer(ABC):

    def __init__(self, raven_client, topic: str, channel: str):
        self.logger = LogWrapper(get_logger(name=self.__class__.__name__, log_level=logging.INFO), raven_client)
        self.continue_running_flag = True
        self.topic = topic
        self.channel = channel
        self.raven_client = RavenClient()
        self.monitor = None

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, signum=None, frame=None):
        self.logger.info("Caught interrupt signal, shutting down gracefully.", tags={"signum": signum, "frame": frame})
        self.continue_running_flag = False

    def report_metric(self, metric_name="default_metric",
                      metric_value=1,
                      unique_identifier="default_identifier",
                      **kwargs):
        pass

    @staticmethod
    def get_err_info(e):
        err_name = type(e).__name__
        err_text = str(e)
        return err_name, err_text

    def remove_sdm_channels(self, nsqs, topic, channle):
        for nsq in nsqs:
            try:
                post_url = f"http://{nsq}/channel/delete?topic={topic}&channel={channle}-sdm"
                result = retry_with_timeout_wrapper(requests.post, url=post_url)
                self.logger.info(f"removed channel: {channle}-sdm from NSQ: {nsq}")
            except Exception as e:
                self.logger.info(f"failed to remove channel: {channle}-sdm from NSQ: {nsq}")
                raise e

    def give_up_and_report(self, message, tags=None, sentry=True):
        if not tags:
            tags = {}
        try:
            message_id = message.id
        except AttributeError:
            message_id = "unknown_id"
        tags["message_id"] = message_id
        self.logger.error(f"Giving up on message after {message.attempts} attempts",
                          tags=tags, sentry=sentry)
