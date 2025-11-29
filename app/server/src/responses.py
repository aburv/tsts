"""
Api Exception with appropriate response
"""
import time

from flask import jsonify, make_response, Response, g

from src.logger import LoggerAPI


def get_turnaround_in_ms(request_time: float) -> float:
    """
    :param request_time:
    :return:
    """
    return (time.perf_counter() - request_time) * 1e4


class APIResponse:
    """
    API Response model
    """
    logger = LoggerAPI()
    status_code = 200

    def __init__(self, data: list | dict | str | bool):
        self.content = data

    def get_response_json(self) -> Response:
        """
        :return:
        :rtype:
        """
        response = make_response(jsonify({'data': self.content}), APIResponse.status_code)
        return response


class ValidResponse(APIResponse):
    """
    Response
    """

    def __init__(self, domain: str, data: list | dict | str | bool, detail=None) -> None:
        super().__init__(data)
        request_time = g.get('start_time', None)
        if request_time is not None:
            turnaround = get_turnaround_in_ms(request_time)
            msg = f"{g.request_id} - {turnaround:.4f} - {APIResponse.status_code} - Success {domain} {detail} : {data}"
        else:
            msg = f"{g.request_id} - 0 - {self.status_code} - Success {domain} {detail} : {data}"
        APIResponse.logger.info_entry(msg)

    def get_data(self) -> list | dict | str | bool:
        """
        Get the data
        """
        return self.content


class CachedResponse(APIResponse):
    """
    Cached Response
    """

    def __init__(self, key: str, data: list | dict | str | bool) -> None:
        APIResponse.logger.info_entry(f'Cached {key} : {data}')
        super().__init__(data)


class APIException(Exception):
    """
    Api exception class
    """
    logger = LoggerAPI()

    def __init__(
            self,
            msg: str,
            content: str,
            error_type: str,
            status_code: int,
            is_error: bool = True
    ) -> None:
        super().__init__(msg)
        try:
            request_time = g.get('start_time', None)
            if request_time is not None:
                turnaround = get_turnaround_in_ms(request_time)
                log_msg = f"{g.request_id} - {turnaround:.4f} - {status_code} {error_type} {msg} : {content}"
            else:
                log_msg = f"{g.request_id} - 0 - {status_code} {error_type} {msg} : {content}"
        except Exception as _:
            log_msg = f"{error_type} {msg} : {content}"
        if is_error:
            APIException.logger.error_entry(log_msg)
        else:
            APIException.logger.warning_entry(log_msg)
        self.msg = msg
        self.content = content
        self.error_type = error_type
        self.status_code = status_code

    def get_response_json(self) -> Response:
        """
        :return:
        :rtype:
        """
        error_response = {
            'error': {
                'type': self.error_type,
                'message': self.msg,
            }
        }
        response = make_response(
            jsonify(error_response),
            500 if (self.status_code in [0, 1, 2]) else self.status_code)
        response.headers["Content-Type"] = "application/json"
        return response


class RuntimeException(APIException):
    """
    500 AuthenticationException
    """

    def __init__(self, domain: str, message: str) -> None:
        super().__init__(domain, message, error_type='RuntimeException', status_code=500)


class SecurityException(APIException):
    """
    401 AuthenticationException
    """

    def __init__(self, msg: str, content: str) -> None:
        super().__init__(msg, content, error_type='SecurityException', status_code=401, is_error=False)


class DataValidationException(APIException):
    """
    400 DataValidationException
    """

    def __init__(self, msg: str, content: str) -> None:
        super().__init__(msg, content, error_type='DataValidationException', status_code=400, is_error=False)


class DBConnectionException(APIException):
    """
    0 DBConnectionException
    """

    def __init__(self, connection_details: str) -> None:
        super().__init__("", connection_details, error_type='DBConnectionException', status_code=0)


class DBExecutionException(APIException):
    """
    1 DBExecutionException
    """

    def __init__(self, operation: str, details: str) -> None:
        super().__init__(operation, details, error_type='DBExecutionException', status_code=1)


class TableNotFoundException(APIException):
    """
    2 TableNotFoundException
    """

    def __init__(self, table_name: str) -> None:
        super().__init__("", table_name, error_type='TableNotFoundException', status_code=2)


class RecordNotFoundException(APIException):
    """
    404 RecordNotFoundException
    """

    def __init__(self, domain: str, record_id: str) -> None:
        super().__init__(record_id, domain, error_type='RecordNotFoundException', status_code=404)
