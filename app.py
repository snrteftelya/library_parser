from fastapi import FastAPI, Query, HTTPException
from typing import List
from parser import NlbCatalogScraper
from models import BookData, SearchType


app = FastAPI()

scraper = NlbCatalogScraper()

@app.get("/books", response_model=List[BookData])
async def get_books(
    query: str = Query(..., description="Поисковый запрос"),
    type: str = Query(
        default=SearchType.AllFields,
        description="Выберите тип поиска",
        enum=list(SearchType),
    ),
    limit: int = Query(5, ge=1, le=50, description="Ограничение количества результатов")
):
    """
    API для поиска книг в каталоге.
    """
    if not type:
        raise HTTPException(status_code=400, detail="Некорректный тип поиска")
    links = scraper.get_links(search_query=query, search_type=type, limit=limit)
    results = scraper.process_links(links)
    return results