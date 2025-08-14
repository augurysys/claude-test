import base64
import json
from binascii import Error as binasciiError
from datetime import datetime
import logging
import requests
import urllib3
from raven import Client as RavenClient
import time
import random
from utils.log_wrapper import LogWrapper
from utils.logger import get_logger


logger = LogWrapper(get_logger(name="Main", log_level=logging.INFO), RavenClient())

import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable


def get_nsq_payload(detection, nsq_publish_topic="detection.created") -> str:
    detection_payload = {
        "name": nsq_publish_topic,
        "time": datetime.now().timestamp(),
        "data": {
            "detection": detection.to_dict() if hasattr(detection, 'to_dict') else detection
        }
    }
    return json.dumps(detection_payload, default=str)


def parse_nsq_message_timestamp(message, string_format="%Y-%m-%d %H:%M:%S"):
    message_timestamp = datetime.utcfromtimestamp(message.timestamp // 10e8)
    ts_as_string = message_timestamp.strftime(string_format)
    return ts_as_string


def decode_message_bytes(message_bytes):
    try:
        decoded = base64.decodebytes(message_bytes)
    except binasciiError:
        # Data is not in Base64
        if isinstance(message_bytes, bytes):
            decoded = message_bytes.decode()
        else:
            decoded = message_bytes
    except TypeError:
        # Data is a string
        decoded = message_bytes
    return decoded


def retry_with_timeout_wrapper(method, attempts=5, back_off_seconds=5, back_off_variance_range=(5, 10),
                               allow_empty_response=True, **arguments):
    back_off_variance_start = back_off_variance_range[0]
    back_off_variance_end = back_off_variance_range[1]
    empty_response_counter = 0
    attempts_counter = 1
    while attempts_counter <= attempts:
        try:
            response = method(**arguments)
        except (urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout, requests.exceptions.Timeout):
            logger.warning(
                f"Request timed out while calling {method.__name__} - will retry. {attempts_counter}/{attempts} attempts",
                exc_info=False)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.RequestException) as e:
            logger.warning(
                f"Exception {e}: while calling {method.__name__} - will retry. {attempts_counter}/{attempts} attempts",
                exc_info=False)
        except Exception as e:
            logger.error(
                f"Got exception {e} while calling {method.__name__} - will retry. {attempts_counter}/{attempts} attempts",
                exc_info=True)
        else:
            if allow_empty_response:
                return response
            else:
                if response:
                    return response
                else:
                    # Retry when calling an API where an empty response could be indicative of an issue
                    empty_response_counter += 1
        iteration_back_off_seconds = back_off_seconds + random.randrange(back_off_variance_start, back_off_variance_end)
        attempts_counter += 1
        logger.debug(f"Backing off calling {method.__name__} for {iteration_back_off_seconds} seconds.")
        time.sleep(iteration_back_off_seconds)
    exhausted_attempts_error = f"Exhausted all attempts trying to call {method.__name__} - giving up."
    if empty_response_counter:
        logger.warning(f"Got empty responses. {exhausted_attempts_error}")
    else:
        logger.warning(exhausted_attempts_error)
    return None
