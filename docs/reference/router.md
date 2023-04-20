## Endpoint
    class jija.router.Endpoint(
        *,
        path: str,
        view: Type[jija.views._ViewBase]
    )

#### Parameters
`path`
    The path to the endpoint.

`view`
    The view to use for the endpoint.


## Include
    class jija.router.Include(
        *,
        path: str,
        endpoints: list[jija.router.Endpoint],
    )

#### Parameters
`path`
    The path to the endpoint.

`endpoints`
    The endpoints to include in this path.
