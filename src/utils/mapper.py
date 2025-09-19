from isodate import parse_duration

from src.models import Error, ErrorType, Activity, ActivityType, ActivityEvent, ActivityEventStatus, BeReal, \
    BeRealStatus


def parse_error(json: dict) -> Error:
    return Error(
        error_type=ErrorType[json["errorType"]],
        message=json["message"],
    )

def parse_activity(json: dict) -> Activity:
    return Activity(
        id=json["id"],
        name=json["name"],
        description=json["description"],
        activity_type=ActivityType[json["activityType"]],
        has_event=json["hasEvent"],
        location=json["location"],
        start_time=json["startTime"],
        end_time=json["endTime"],
    )

def parse_activity_event(json: dict) -> ActivityEvent:
    return ActivityEvent(
        name=json["name"],
        status=ActivityEventStatus[json["status"]] if json["status"] else None,
        duration=parse_duration(json["duration"]),
    )

def parse_be_real(json: dict) -> BeReal:
    return BeReal(
        id=json["id"],
        name=json["name"],
        description=json["description"],
        status=BeRealStatus[json["status"]],
        duration=parse_duration(json["duration"]),
    )