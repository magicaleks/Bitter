from http.client import NOT_FOUND
from bitter.api.validation.oneway import CreateOneWay, DeleteOneWay, UpdateOneWay
from bitter.oneway.manager import OneWayManager
from bitter.oneway.model import OneWay
from fastapi import APIRouter, Request, Response
import starlette.status as status

router = APIRouter(prefix="/oneways", tags=["oneways"])


@router.get("/get/uid/{uid}", response_model=OneWay, response_description="Get oneway by it's uid")
def get_oneway(uid: str):
    """Get oneway"""

    way = OneWayManager.get(uid=uid)

    return way if way else Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/create", response_model=OneWay, response_description="Create oneway")
def create_oneway(schema: CreateOneWay):
    """Create oneway"""

    way = OneWayManager.create(
        target=schema.target,
        is_temporary=schema.is_temporary,
        lifetime=schema.lifetime,
        user_uid=schema.user_uid,
        only_numbers=schema.only_numbers,
    )

    return way


@router.post("/update", response_description="Update oneway")
def update_oneway(schema: UpdateOneWay):
    """Update oneway"""

    OneWayManager.update(schema.uid, schema.update)

    return {}


@router.post("/delete", response_description="Delete oneway")
def delete_oneway(schema: DeleteOneWay):
    """Delete oneway"""

    OneWayManager.delete(schema.uid)

    return {}


@router.get("/{alias}", response_description="Get redirect link by alias")
def redirect(alias: str, request: Request):
    """Get redirect link"""

    link = OneWayManager.redirect(alias, ip=request.client.host)

    return {"redirect": link} if link else Response(status_code=status.HTTP_404_NOT_FOUND)
