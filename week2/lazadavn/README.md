# Using Scrapy to collect products from Lazada.vn

## API Endpoint - Review Retrieval 

E.g.:
```
https://my.lazada.vn/pdp/review/getReviewList?itemId=1040858590&pageSize=5&filter=0&sort=0&pageNo=3
```

Generalized form:
```
https://my.lazada.vn/pdp/review/getReviewList?itemId={ITEM_ID}&pageSize={PAGE_SIZE}&filter={FILTER_STAR_COUNT}&sort={SORT_ENUM}&pageNo={PAGE_NO}

Where:
ITEM_ID:
    integer
    get from request url

PAGE_SIZE:
    integer
    default: 5

FILTER_STAR_COUNT: filter reviews by star count
    integer
    [1, 5]

SORT_ENUM:
    0 = revelance
    1 = recent
    2 = rating: high to low
    3 = rating: low to high

PAGE_NO:
    page number
```

Response schema (OpenAPI 3):
```yaml
# OpenAPI https://swagger.io/specification/
```

## API Endpoint - Related Items

```
https://pdpdesc-m.lazada.vn/recommend?seller_sub_id=1000001033&shop_id=7272&category_id=9034&item_id=1040858590&anonymous_id=2e229c65-0604-471a-c60c-fd058b3858b9&regional_key=020102000000&is_ab=false&sku=1040858590_VNAMZ-3520978989&seller_id=100101649&is_tbc=0&_=1641373849244&brand_id=69
```

