from dataclasses import dataclass
from datetime import datetime

from typing import List, Literal


@dataclass
class SecretValue:
    ARN: str
    Name: str
    VersionId: str
    SecretString: str
    VersionStages: List[Literal["AWSCURRENT"]]
    CreatedDate: datetime
    ResponseMetadata: "ResponseMetadatum"


@dataclass
class ResponseMetadatum:
    RequestId: str
    HttpStatusCode: int
    HTTPHeader: "HttpHeader"
    RetryAttempts: int


@dataclass
class HttpHeader:
    date_: str
    contenttype: str
    contentlength: str
    connection: Literal["keep-alive"]
    xamznrequestid: str
