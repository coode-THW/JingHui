from fastapi import APIRouter, Query
from sqlalchemy import select

from ..errors import not_found, ok
from ..models import Artist, Product
from ..security import DbSession
from ..serializers import artist_data, product_data

router = APIRouter(prefix="/api", tags=["载体与画师"])


@router.get("/products")
def list_products(db: DbSession, category: str | None = Query(default=None, max_length=60)):
    query = select(Product).where(Product.status == "ON_SALE")
    if category:
        query = query.where(Product.category == category)
    products = db.scalars(query.order_by(Product.sort_order, Product.id)).all()
    return ok([product_data(product) for product in products])


@router.get("/artists")
def list_artists(db: DbSession):
    artists = db.scalars(
        select(Artist).where(Artist.status == "ACTIVE").order_by(Artist.rating.desc(), Artist.id)
    ).all()
    return ok([artist_data(artist) for artist in artists])


@router.get("/artists/{artist_id}")
def get_artist(artist_id: int, db: DbSession):
    artist = db.get(Artist, artist_id)
    if artist is None or artist.status != "ACTIVE":
        raise not_found("画师")
    return ok(artist_data(artist))
