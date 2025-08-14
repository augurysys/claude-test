from fastapi import Request

from utils.log_wrapper import LogWrapper


def get_request_logger(request: Request) -> LogWrapper:
    return request.state.logger
