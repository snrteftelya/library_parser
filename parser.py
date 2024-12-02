import requests
from bs4 import BeautifulSoup


class NlbCatalogScraper:
    def __init__(self, base_url="https://e-catalog.nlb.by"):
        self.base_url = base_url

    def get_links(self, search_query, search_type, limit):
        """
        Получает ссылки на книги по запросу.
        """
        search_query = search_query.replace(" ", "+")
        url = f"{self.base_url}/Search/Results?lookfor={search_query}&type={search_type}&limit={limit}&sort=relevance"
        response = requests.get(url)
        print(f"Fetching links from: {url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        hrefs = soup.find_all(class_="title getFull")
        links = [self.base_url + href.get("href") if href.get("href") else None for href in hrefs if href.get("href")]
        return links

    def process_links(self, links):
        """
        Обрабатывает ссылки, извлекая информацию о книгах.
        """
        results = []
        for link in links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')

            title_tag = soup.find("h3")
            title = title_tag.text.strip() if title_tag else "Unknown Title"

            picture_tag = soup.find(class_="recordcover")
            picture = self.base_url + picture_tag.get("src").strip() if picture_tag else "No Picture"

            table = soup.find(class_="table table-striped")
            rows = table.find_all('tr') if table else []
            row_data = []
            for row in rows:
                cells = row.find_all('td')
                if cells:
                    key = row.text.split(":")[0].strip()
                    value = cells[-1].text.replace("\n", " ").replace("  ", "").strip()
                    row_data.append({key: value})

            result = {
                "title": title,
                "picture": picture,
                "rows": row_data
            }
            results.append(result)
        return results