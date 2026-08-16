"""Data models generated from the metablock OpenAPI spec.

Do not edit this module by hand: change ./.dev/models and run `make models`.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import AnyUrl, AwareDatetime, BaseModel, Field, RootModel


class AccountStatus(StrEnum):
    unspecified = "unspecified"
    created = "created"
    active = "active"
    inactive = "inactive"
    closed = "closed"
    waiting_list = "waiting_list"


class ApiToken(BaseModel):
    id: str = Field(..., title="Id")
    """
    Token unique ID - not the key
    """
    key: str = Field(..., title="Key")
    """
    Token key
    """
    created_at: AwareDatetime = Field(..., title="Created At")
    """
    Token creation date
    """
    access_count: int | None = Field(0, title="Access Count")
    """
    Token usage count
    """
    expires_at: AwareDatetime | None = Field(None, title="Expires At")
    """
    Token expiration date
    """
    tags: list[str] | None = Field(None, title="Tags")
    """
    List of tags associated with the token
    """
    last_access: AwareDatetime | None = Field(None, title="Last Access")
    """
    Last access timestamp
    """


class ApiTokenCreate(BaseModel):
    tags: list[str] | None = Field(None, title="Tags")
    """
    List of tags associated with the token
    """
    ttl: int | None = Field(None, title="Ttl")
    """
    Token expiration time in seconds
    """


class Upstream(RootModel[AnyUrl]):
    root: AnyUrl = Field(..., title="Upstream")
    """
    Upstream URL
    """


class Certificate(BaseModel):
    serial_number: int = Field(..., title="Serial Number")
    version: str = Field(..., title="Version")
    issued_on: AwareDatetime = Field(..., title="Issued On")
    expires_on: AwareDatetime = Field(..., title="Expires On")
    issuer: dict[str, Any] = Field(..., title="Issuer")
    created: AwareDatetime = Field(..., title="Created")
    """
    created
    """
    cert: str = Field(..., title="Cert")
    """
    public certificate
    """
    tags: list[str] | None = Field(None, title="Tags")
    """
    An optional set of strings
    """


class Country(BaseModel):
    alpha_2: str = Field(..., max_length=2, min_length=2, title="Alpha 2")
    """
    Country alpha 2 letter code
    """
    alpha_3: str = Field(..., max_length=3, min_length=3, title="Alpha 3")
    """
    Country alpha 3 letter code
    """
    numeric: str = Field(..., max_length=3, min_length=3, title="Numeric")
    """
    Country numeric code
    """
    name: str = Field(..., title="Name")
    """
    Country name
    """
    official_name: str = Field(..., title="Official Name")
    """
    Country official name
    """


class CreateExtension(BaseModel):
    name: str = Field(..., title="Name")
    """
    Extension name
    """
    schema_: dict[str, Any] = Field(..., alias="schema", title="Schema")
    """
    Extension JSON schema
    """
    webhook_active: bool | None = Field(False, title="Webhook Active")
    """
    Is the webhook active
    """
    webhook_url: str | None = Field("", title="Webhook Url")
    """
    Webhook URL
    """


class CreateOrg(BaseModel):
    email: str = Field(..., title="Email")
    """
    Email address of the organization
    """
    short_name: str = Field(..., title="Short Name")
    """
    Org unique short name - must be a slug
    """
    full_name: str | None = Field("", title="Full Name")
    """
    Full name of the organization
    """
    registered_name: str | None = Field("", title="Registered Name")
    """
    Registered name of the organization
    """
    registration_number: str | None = Field("", title="Registration Number")
    """
    Registration number of the organization
    """
    status: AccountStatus | None = AccountStatus.created
    country: str | None = Field("", title="Country")
    """
    Country of the organization
    """
    address: str | None = Field("", title="Address")
    """
    Address of the organization
    """


class CreateSpaceExtension(BaseModel):
    name: str = Field(..., title="Name")
    """
    Extension name
    """
    config: dict[str, Any] = Field(..., title="Config")
    """
    Extension configuration
    """


class Dashboard(BaseModel):
    id: int = Field(..., title="Id")
    """
    Dashboard id
    """
    name: str = Field(..., title="Name")
    """
    Dashboard name
    """
    config: dict[str, Any] = Field(..., title="Config")
    """
    Dashboard json data
    """
    last_modified: AwareDatetime | None = Field(None, title="Last Modified")
    """
    Dashboard last modified
    """
    default: bool | None = Field(False, title="Default")
    """
    Default dashboard
    """
    user_id: str | None = Field("", title="User Id")
    """
    User ID
    """


class DashboardCreate(BaseModel):
    """
    Update an existing dashboard
    """

    name: str = Field(..., title="Name")
    """
    Dashboard name
    """
    config: dict[str, Any] = Field(..., title="Config")
    """
    Dashboard json data
    """
    default: bool | None = Field(False, title="Default")
    """
    Default dashboard
    """


class DashboardUpdate(BaseModel):
    """
    Update an existing dashboard
    """

    name: str | None = Field(None, title="Name")
    """
    Dashboard name
    """
    config: dict[str, Any] | None = Field(None, title="Config")
    """
    Dashboard json data
    """
    default: bool | None = Field(None, title="Default")
    """
    Default dashboard
    """


class Env(StrEnum):
    unspecified = "unspecified"
    dev = "dev"
    stage = "stage"
    prod = "prod"


class Extension(BaseModel):
    id: str = Field(..., title="Id")
    """
    Extension ID
    """
    name: str = Field(..., title="Name")
    """
    Extension name
    """
    org_id: str = Field(..., title="Org Id")
    """
    Organization ID
    """
    org_name: str = Field(..., title="Org Name")
    """
    Extension Organization name
    """
    schema_: dict[str, Any] = Field(..., alias="schema", title="Schema")
    """
    Extension JSON schema
    """
    webhook_active: bool | None = Field(False, title="Webhook Active")
    """
    Is the webhook active
    """
    webhook_url: str | None = Field("", title="Webhook Url")
    """
    Webhook URL
    """
    docs: str | None = Field("", title="Docs")
    """
    Extension documentation
    """


class HttpMethod(StrEnum):
    get = "get"
    post = "post"
    put = "put"
    delete = "delete"
    patch = "patch"
    head = "head"


class InstanceType(StrEnum):
    """
    Size and shape of the machines running in a server

    The `general` family is balanced, `compute` gives more processing power
    per unit of memory and `memory` more memory per unit of processing power.

    | instance type | vCPU | memory |
    |---|---|---|
    | `general-small` | 2 | 8 GB |
    | `general-medium` | 4 | 16 GB |
    | `general-large` | 8 | 32 GB |
    | `compute-small` | 2 | 4 GB |
    | `compute-medium` | 4 | 8 GB |
    | `compute-large` | 8 | 16 GB |
    | `memory-medium` | 4 | 32 GB |
    | `memory-large` | 8 | 64 GB |
    """

    general_small = "general-small"
    general_medium = "general-medium"
    general_large = "general-large"
    compute_small = "compute-small"
    compute_medium = "compute-medium"
    compute_large = "compute-large"
    memory_medium = "memory-medium"
    memory_large = "memory-large"


class Org(BaseModel):
    email: str = Field(..., title="Email")
    """
    Email address of the organization
    """
    short_name: str = Field(..., title="Short Name")
    """
    Org unique short name - must be a slug
    """
    full_name: str | None = Field("", title="Full Name")
    """
    Full name of the organization
    """
    registered_name: str | None = Field("", title="Registered Name")
    """
    Registered name of the organization
    """
    registration_number: str | None = Field("", title="Registration Number")
    """
    Registration number of the organization
    """
    status: AccountStatus | None = AccountStatus.created
    country: str | None = Field("", title="Country")
    """
    Country of the organization
    """
    address: str | None = Field("", title="Address")
    """
    Address of the organization
    """
    id: str = Field(..., title="Id")
    created: AwareDatetime = Field(..., title="Created")
    additional_info: dict[str, Any] | None = Field(None, title="Additional Info")


class OrgMember(BaseModel):
    user_id: str = Field(..., title="User Id")
    """
    User ID
    """
    email: str = Field(..., title="Email")
    """
    User email
    """
    first_name: str | None = Field("", title="First Name")
    """
    User first name
    """
    last_name: str | None = Field("", title="Last Name")
    """
    User last name
    """
    space_id: str | None = Field("", title="Space Id")
    """
    Space ID
    """
    org_id: str | None = Field("", title="Org Id")
    """
    Organization ID
    """
    org_name: str | None = Field("", title="Org Name")
    """
    Organization short name
    """
    org_full_name: str | None = Field("", title="Org Full Name")
    """
    Organization full name
    """
    org_email: str | None = Field("", title="Org Email")
    """
    Organization email address
    """
    roles: list[str] | None = Field(None, title="Roles")
    """
    List of roles
    """


class OrgPermission(StrEnum):
    """
    Permissions granted by the organization endpoints

    The default namespace of the orgs extension, for applications which do not
    declare one of their own.
    """

    full_permission = "full_permission"
    org_update = "org_update"
    org_roles_create = "org_roles_create"
    org_roles_read = "org_roles_read"
    org_roles_update = "org_roles_update"
    org_roles_delete = "org_roles_delete"


class OrgRoleNamedPermissionsOrgPermission(BaseModel):
    description: str | None = Field("", max_length=256, title="Description")
    """
    Role description
    """
    permissions: list[OrgPermission] | None = Field(None, title="Permissions")
    """
    List of permissions for this role
    """
    name: str = Field(..., max_length=32, title="Name")
    """
    Role name - must be a slug, unique within the organization
    """
    id: str = Field(..., title="Id")
    """
    Role unique ID
    """
    org_id: str = Field(..., title="Org Id")
    """
    Organization ID
    """
    members: int | None = Field(0, title="Members")
    """
    Number of organization members with this role
    """


class PeeringCreate(BaseModel):
    server1: str = Field(..., title="Server1")
    """
    First server ID or name
    """
    server2: str = Field(..., title="Server2")
    """
    Second server ID or name
    """


class PeeringState(StrEnum):
    """
    Lifecycle state of a connection between two servers
    """

    unspecified = "unspecified"
    pending = "pending"
    active = "active"
    failed = "failed"
    deleted = "deleted"


class PhotoProvider(StrEnum):
    unsplash = "unsplash"
    pixabay = "pixabay"


class RoleNamedPermissionsOrgPermission(BaseModel):
    description: str | None = Field("", max_length=256, title="Description")
    """
    Role description
    """
    permissions: list[OrgPermission] | None = Field(None, title="Permissions")
    """
    List of permissions for this role
    """
    name: str = Field(..., max_length=32, title="Name")
    """
    Role name - must be a slug, unique within the organization
    """


class Route(BaseModel):
    name: str = Field(..., title="Name")
    """
    Route name
    """
    paths: list[str] | None = Field(None, title="Paths")
    """
    List of paths for the route
    """
    methods: list[HttpMethod] | None = Field(None, title="Methods")
    """
    List of methods for the route
    """
    hosts: list[str] | None = Field(None, title="Hosts")
    """
    List of hosts for the route
    """
    protocols: list[str] | None = Field(None, title="Protocols")
    """
    List of protocols for the route
    """
    plugins: list[dict[str, Any]] | None = Field(None, title="Plugins")
    """
    List of plugins for the route
    """
    tags: list[str] | None = Field(None, title="Tags")
    """
    An optional set of strings
    """
    strip_path: bool | None = Field(False, title="Strip Path")
    """
    Should the path be stripped from the request
    """
    preserve_host: bool | None = Field(True, title="Preserve Host")
    """
    Should the host be preserved from the request
    """
    https_redirect_status_code: int | None = Field(
        301, title="Https Redirect Status Code"
    )
    """
    HTTP status code for redirecting to HTTPS
    """


class RouteDetails(BaseModel):
    name: str = Field(..., title="Name")
    """
    Route name
    """
    paths: list[str] | None = Field(None, title="Paths")
    """
    List of paths for the route
    """
    methods: list[HttpMethod] | None = Field(None, title="Methods")
    """
    List of methods for the route
    """
    hosts: list[str] | None = Field(None, title="Hosts")
    """
    List of hosts for the route
    """
    protocols: list[str] | None = Field(None, title="Protocols")
    """
    List of protocols for the route
    """
    plugins: list[dict[str, Any]] | None = Field(None, title="Plugins")
    """
    List of plugins for the route
    """
    tags: list[str] | None = Field(None, title="Tags")
    """
    An optional set of strings
    """
    strip_path: bool | None = Field(False, title="Strip Path")
    """
    Should the path be stripped from the request
    """
    preserve_host: bool | None = Field(True, title="Preserve Host")
    """
    Should the host be preserved from the request
    """
    https_redirect_status_code: int | None = Field(
        301, title="Https Redirect Status Code"
    )
    """
    HTTP status code for redirecting to HTTPS
    """
    id: str = Field(..., title="Id")
    """
    Route ID
    """


class ServerState(StrEnum):
    """
    Lifecycle state of a server or one of its instances
    """

    unspecified = "unspecified"
    pending = "pending"
    running = "running"
    stopping = "stopping"
    stopped = "stopped"
    terminated = "terminated"


class ServerUpdate(BaseModel):
    instance_type: InstanceType | None = None
    """
    Instance type of the server machines
    """
    cidr: str | None = Field("", title="Cidr")
    """
    CIDR block of the server private network
    """
    spot: bool | None = Field(False, title="Spot")
    """
    Use interruptible instances rather than dedicated ones
    """
    size: int | None = Field(1, ge=0, title="Size")
    """
    Desired number of instances in the server
    """


class Space(BaseModel):
    cdn: str | None = Field("", title="Cdn")
    """
    CDN domain
    """
    cdn_id: str | None = Field("", title="Cdn Id")
    """
    CDN ID
    """
    hosted: bool | None = Field(False, title="Hosted")
    """
    Is the space hosted in metablock cloud?
    """
    name: str = Field(..., title="Name")
    """
    Space unique name - must be a slug
    """
    domain: str = Field(..., title="Domain")
    """
    Domain name
    """
    id: str = Field(..., title="Id")
    """
    Space unique ID
    """
    org_id: str = Field(..., title="Org Id")
    """
    Organization ID
    """
    org_name: str = Field(..., title="Org Name")
    """
    Organization name
    """


class SpaceCreate(BaseModel):
    cdn: str | None = Field("", title="Cdn")
    """
    CDN domain
    """
    cdn_id: str | None = Field("", title="Cdn Id")
    """
    CDN ID
    """
    hosted: bool | None = Field(False, title="Hosted")
    """
    Is the space hosted in metablock cloud?
    """
    name: str = Field(..., title="Name")
    """
    Space unique name - must be a slug
    """
    domain: str = Field(..., title="Domain")
    """
    Domain name
    """


class SpaceExtension(BaseModel):
    id: str = Field(..., title="Id")
    """
    Space Extension ID
    """
    space_id: str = Field(..., title="Space Id")
    """
    Space ID
    """
    space_name: str = Field(..., title="Space Name")
    """
    Space name
    """
    extension_id: str = Field(..., title="Extension Id")
    """
    Extension ID
    """
    config: dict[str, Any] = Field(..., title="Config")
    """
    Extension configuration
    """
    name: str = Field(..., title="Name")
    """
    Extension name
    """


class SpaceNameServers(BaseModel):
    domain: str = Field(..., title="Domain")
    """
    Domain name of the space
    """
    name_servers: list[str] | None = Field(None, title="Name Servers")
    """
    Route53 delegation-set nameservers to configure at the domain registrar. Empty when the space has no hosted zone.
    """


class SpaceUpdate(BaseModel):
    cdn: str | None = Field("", title="Cdn")
    """
    CDN domain
    """
    cdn_id: str | None = Field("", title="Cdn Id")
    """
    CDN ID
    """
    hosted: bool | None = Field(False, title="Hosted")
    """
    Is the space hosted in metablock cloud?
    """


class UpdateOrg(BaseModel):
    """
    Fields of an organization which can be changed after creation

    The short name is left out on purpose: it is the slug organizations are
    addressed by. The status is a account lifecycle field, managed by the admin
    API rather than by the members of the organization.
    """

    email: str | None = Field("", title="Email")
    """
    Email address of the organization
    """
    full_name: str | None = Field("", title="Full Name")
    """
    Full name of the organization
    """
    registered_name: str | None = Field("", title="Registered Name")
    """
    Registered name of the organization
    """
    registration_number: str | None = Field("", title="Registration Number")
    """
    Registration number of the organization
    """
    country: str | None = Field("", title="Country")
    """
    Country of the organization
    """
    address: str | None = Field("", title="Address")
    """
    Address of the organization
    """


class UpdateRoleNamedPermissionsOrgPermission(BaseModel):
    description: str | None = Field("", max_length=256, title="Description")
    """
    Role description
    """
    permissions: list[OrgPermission] | None = Field(None, title="Permissions")
    """
    List of permissions for this role
    """


class User(BaseModel):
    id: str = Field(..., title="Id")
    """
    User unique ID
    """
    country: str | None = Field("", title="Country")
    """
    User country
    """
    twofactor: bool | None = Field(False, title="Twofactor")
    """
    User two factor authentication
    """
    first_name: str | None = Field("", title="First Name")
    """
    User first name
    """
    last_name: str | None = Field("", title="Last Name")
    """
    User last name
    """
    email: str = Field(..., title="Email")
    """
    User email
    """
    mobile_phone: str | None = Field("", title="Mobile Phone")
    """
    User mobile phone
    """
    additional_info: dict[str, Any] | None = Field(None, title="Additional Info")
    created: AwareDatetime = Field(..., title="Created")
    """
    User creation date
    """
    status: AccountStatus
    """
    User account status
    """


class UserUpdate(BaseModel):
    first_name: str | None = Field(None, title="First Name")
    """
    User first name
    """
    last_name: str | None = Field(None, title="Last Name")
    """
    User last name
    """
    country: str | None = Field(None, title="Country")
    """
    User country
    """
    status: AccountStatus | None = None
    """
    Account status
    """
    mobile_phone: str | None = Field(None, title="Mobile Phone")
    """
    User mobile phone
    """
    additional_info: dict[str, Any] | None = Field(None, title="Additional Info")
    """
    Additional user information
    """


class ValidationError(BaseModel):
    loc: list[str | int] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")
    input: Any | None = Field(None, title="Input")
    ctx: dict[str, Any] | None = Field(None, title="Context")


class Zone(StrEnum):
    """
    Geographic location where a server runs

    | zone | location |
    |---|---|
    | `virginia` | United States, East |
    | `oregon` | United States, West |
    | `ireland` | Europe, Ireland |
    | `london` | Europe, United Kingdom |
    | `frankfurt` | Europe, Germany |
    | `tokyo` | Asia Pacific, Japan |
    | `singapore` | Asia Pacific, Singapore |
    | `sydney` | Asia Pacific, Australia |
    """

    virginia = "virginia"
    oregon = "oregon"
    ireland = "ireland"
    london = "london"
    frankfurt = "frankfurt"
    tokyo = "tokyo"
    singapore = "singapore"
    sydney = "sydney"


class Block(BaseModel):
    id: str = Field(..., title="Id")
    """
    Block ID
    """
    service_id: str = Field(..., title="Service Id")
    """
    Service ID
    """
    name: str = Field(..., title="Name")
    """
    Block name
    """
    space: Space
    """
    Space object
    """
    api_url: str | None = Field(None, title="Api Url")
    """
    API URL of the block
    """
    full_name: str = Field(..., title="Full Name")
    """
    Full name of the block
    """
    html: bool = Field(..., title="Html")
    """
    Is the block an HTML block?
    """
    root: bool = Field(..., title="Root")
    """
    Is the block a root block?
    """
    use_cdn: bool = Field(..., title="Use Cdn")
    """
    Should the block use CDN?
    """
    acme: bool | None = Field(False, title="Acme")
    """
    Is the SSL certificate managed by the acme plugin?
    """
    domain: str = Field(..., title="Domain")
    """
    Domain of the block
    """
    upstream: str | None = Field("", title="Upstream")
    """
    Upstream URL
    """
    internal: dict[str, Any] | None = Field(None, title="Internal")
    """
    Internal data
    """
    routes: list[RouteDetails] | None = Field(None, title="Routes")
    """
    List of routes for the service
    """
    url: str = Field(..., title="Url")
    """
    The URL for the block
    """


class BlockCreate(BaseModel):
    html: bool | None = Field(False, title="Html")
    """
    Is the block an HTML block?
    """
    upstream: Upstream | None = Field(None, title="Upstream")
    """
    Upstream URL
    """
    root: bool | None = Field(False, title="Root")
    """
    Is the block a root block?
    """
    use_cdn: bool | None = Field(False, title="Use Cdn")
    """
    Should the block use CDN?
    """
    acme: bool | None = Field(False, title="Acme")
    """
    Is the SSL certificate managed by the acme plugin?
    """
    routes: list[Route] | None = Field(None, title="Routes")
    """
    List of routes for the block
    """
    tags: list[str] | None = Field(None, title="Tags")
    """
    An optional set of strings
    """
    name: str = Field(..., title="Name")
    """
    Block unique name - must be a slug
    """


class BlockEntry(BaseModel):
    id: str = Field(..., title="Id")
    """
    Block ID
    """
    service_id: str = Field(..., title="Service Id")
    """
    Service ID
    """
    name: str = Field(..., title="Name")
    """
    Block name
    """
    space: Space
    """
    Space object
    """
    api_url: str | None = Field(None, title="Api Url")
    """
    API URL of the block
    """
    full_name: str = Field(..., title="Full Name")
    """
    Full name of the block
    """
    html: bool = Field(..., title="Html")
    """
    Is the block an HTML block?
    """
    root: bool = Field(..., title="Root")
    """
    Is the block a root block?
    """
    use_cdn: bool = Field(..., title="Use Cdn")
    """
    Should the block use CDN?
    """
    acme: bool | None = Field(False, title="Acme")
    """
    Is the SSL certificate managed by the acme plugin?
    """
    domain: str = Field(..., title="Domain")
    """
    Domain of the block
    """
    url: str = Field(..., title="Url")
    """
    The URL for the block
    """


class BlockUpdate(BaseModel):
    html: bool | None = Field(False, title="Html")
    """
    Is the block an HTML block?
    """
    upstream: Upstream | None = Field(None, title="Upstream")
    """
    Upstream URL
    """
    root: bool | None = Field(False, title="Root")
    """
    Is the block a root block?
    """
    use_cdn: bool | None = Field(False, title="Use Cdn")
    """
    Should the block use CDN?
    """
    acme: bool | None = Field(False, title="Acme")
    """
    Is the SSL certificate managed by the acme plugin?
    """
    routes: list[Route] | None = Field(None, title="Routes")
    """
    List of routes for the block
    """
    tags: list[str] | None = Field(None, title="Tags")
    """
    An optional set of strings
    """


class BodyCreateDeployment(BaseModel):
    bundle: str = Field(
        ...,
        json_schema_extra={"contentMediaType": "application/octet-stream"},
        title="Bundle",
    )
    env: Env
    name: str | None = Field("", title="Name")


class Deployment(BaseModel):
    id: str = Field(..., title="Id")
    """
    Deployment ID
    """
    block_id: str = Field(..., title="Block Id")
    """
    Block ID
    """
    env: Env
    """
    Environment
    """
    created: AwareDatetime = Field(..., title="Created")
    """
    Deployment creation date
    """
    name: str | None = Field("", title="Name")
    """
    Deployment name
    """
    url: str = Field(..., title="Url")
    """
    The URL for the deployment
    """


class HTTPValidationError(BaseModel):
    detail: list[ValidationError] | None = Field(None, title="Detail")


class Peering(BaseModel):
    id: str = Field(..., title="Id")
    """
    Peering unique ID
    """
    server1_id: str = Field(..., title="Server1 Id")
    """
    First server ID
    """
    server1_name: str = Field(..., title="Server1 Name")
    """
    First server name
    """
    server2_id: str = Field(..., title="Server2 Id")
    """
    Second server ID
    """
    server2_name: str = Field(..., title="Server2 Name")
    """
    Second server name
    """
    connection_id: str | None = Field("", title="Connection Id")
    """
    ID of the network connection - available once established
    """
    state: PeeringState | None = PeeringState.unspecified
    """
    Peering connection state
    """
    created: AwareDatetime = Field(..., title="Created")
    """
    Peering creation timestamp
    """


class Server(BaseModel):
    instance_type: InstanceType
    """
    Instance type of the server machines
    """
    cidr: str | None = Field("", title="Cidr")
    """
    CIDR block of the server private network
    """
    spot: bool | None = Field(False, title="Spot")
    """
    Use interruptible instances rather than dedicated ones
    """
    size: int | None = Field(1, ge=0, title="Size")
    """
    Desired number of instances in the server
    """
    name: str = Field(..., title="Name")
    """
    Server name - must be a slug, unique within the organization
    """
    zone: Zone
    """
    Geographic location of the server
    """
    id: str = Field(..., title="Id")
    """
    Server unique ID
    """
    org_id: str = Field(..., title="Org Id")
    """
    Organization ID
    """
    org_name: str = Field(..., title="Org Name")
    """
    Organization name
    """
    network_id: str | None = Field("", title="Network Id")
    """
    ID of the private network of the server - available once provisioned
    """
    instance_group: str | None = Field("", title="Instance Group")
    """
    Name of the group managing the server instances - available once provisioned
    """
    state: ServerState | None = ServerState.unspecified
    """
    Server state
    """
    created: AwareDatetime = Field(..., title="Created")
    """
    Server creation timestamp
    """


class ServerCreate(BaseModel):
    instance_type: InstanceType
    """
    Instance type of the server machines
    """
    cidr: str | None = Field("", title="Cidr")
    """
    CIDR block of the server private network
    """
    spot: bool | None = Field(False, title="Spot")
    """
    Use interruptible instances rather than dedicated ones
    """
    size: int | None = Field(1, ge=0, title="Size")
    """
    Desired number of instances in the server
    """
    name: str = Field(..., title="Name")
    """
    Server name - must be a slug, unique within the organization
    """
    zone: Zone
    """
    Geographic location of the server
    """


class ServerInstance(BaseModel):
    id: str = Field(..., title="Id")
    """
    Server instance unique ID
    """
    server_id: str = Field(..., title="Server Id")
    """
    Server the instance belongs to
    """
    instance_id: str = Field(..., title="Instance Id")
    """
    ID of the machine running the instance
    """
    state: ServerState | None = ServerState.unspecified
    """
    Instance state
    """
    created: AwareDatetime = Field(..., title="Created")
    """
    Instance registration timestamp
    """
