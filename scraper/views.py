from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re

def scrape_wikipedia(request):
    search_term = request.GET.get('query', '')
    context = {}

    if search_term:
        try:
            url = f"https://en.wikipedia.org/wiki/{search_term.replace(' ', '_')}"
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-200 status codes

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract a more comprehensive summary (example)
            summary_paragraphs = soup.find_all('p', limit=3)  # Find first 3 paragraphs
            summary_text = '\n'.join([re.sub(r'\[\d+\]', '', p.get_text()) for p in summary_paragraphs])

            context['result'] = summary_text if summary_text else "No information found for this query."
            
            # Extract image URLs and filter to large images only (e.g., width > 200px)
            image_tags = soup.find_all('img')
            image_urls = []
            
            for tag in image_tags:
                if tag.has_attr('src'):
                    width = tag.get('width')
                    if width and int(width) > 200:
                        image_url = tag['src']
                        if image_url.startswith('//'):
                            image_url = 'https:' + image_url
                        elif image_url.startswith('/'):
                            image_url = 'https://en.wikipedia.org' + image_url
                        
                        image_urls.append(image_url)
                
                # Stop after getting 3 valid large images
                if len(image_urls) == 3:
                    break

            context['image_urls'] = image_urls
        except requests.exceptions.RequestException as e:
            context['error'] = f"Error fetching Wikipedia data: {e}"

    return render(request, 'scraper/results.html', context)
