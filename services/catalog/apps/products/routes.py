from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination
from .models import Product
from .schemas import ProductRead, ProductFilter

router = Router(tags=["Products"])


@router.get("/", response=list[ProductRead])
@paginate(PageNumberPagination, page_size=12)
def list_products(request, filter: Query[ProductFilter]):
    products = Product.objects.with_variant_main()

    if filter.ordering:
        products = products.order_by(filter.ordering.value)
    if filter.min_price:
        products = products.filter(variant__price__gte=filter.min_price).distinct()
    return products


@router.post("/", response=ProductRead)
def product_create(request): ...
