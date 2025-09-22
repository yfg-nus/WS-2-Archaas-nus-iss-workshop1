import wikipedia

def get_article(search_term):
    """
    Enhanced Wikipedia function that returns content, title, and description 
    for the top 3 search results.
    
    Args:
        search_term (str): The term to search for on Wikipedia
        
    Returns:
        list: A list of dictionaries containing 'title', 'content', and 'description' 
              for up to 3 Wikipedia articles
    """
    try:
        # Get search results
        results = wikipedia.search(search_term, results=3)
        
        if not results:
            return []
        
        articles = []
        
        # Process up to 3 results
        for result in results[:3]:
            try:
                # Get the Wikipedia page
                page = wikipedia.page(result, auto_suggest=False)
                
                # Extract information
                article_info = {
                    'title': page.title,
                    'content': page.content,
                    'description': page.summary  # Using summary as description
                }
                
                articles.append(article_info)
                
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle disambiguation pages by taking the first option
                try:
                    page = wikipedia.page(e.options[0], auto_suggest=False)
                    article_info = {
                        'title': page.title,
                        'content': page.content,
                        'description': page.summary
                    }
                    articles.append(article_info)
                except:
                    # Skip this result if it still fails
                    continue
                    
            except wikipedia.exceptions.PageError:
                # Skip results that don't have valid pages
                continue
            except Exception as e:
                # Skip any other errors and continue with next result
                print(f"Error processing result '{result}': {e}")
                continue
        
        return articles
        
    except Exception as e:
        print(f"Error searching Wikipedia: {e}")
        return []


def get_article_compact(search_term):
    """
    Compact version that returns essential info for top 3 results.
    
    Args:
        search_term (str): The term to search for on Wikipedia
        
    Returns:
        list: A list of dictionaries with 'title', 'content', and 'description'
    """
    try:
        results = wikipedia.search(search_term, results=3)
        articles = []
        
        for result in results[:3]:
            try:
                page = wikipedia.page(result, auto_suggest=False)
                articles.append({
                    'title': page.title,
                    'content': page.content,
                    'description': page.summary
                })
            except:
                continue
                
        return articles
    except:
        return []


# Example usage and testing
if __name__ == "__main__":
    # Test the function
    search_term = "artificial intelligence"
    print(f"Searching for: {search_term}")
    print("=" * 50)
    
    articles = get_article(search_term)
    
    for i, article in enumerate(articles, 1):
        print(f"\n--- Article {i} ---")
        print(f"Title: {article['title']}")
        print(f"Description: {article['description'][:200]}...")  # First 200 chars
        print(f"Content length: {len(article['content'])} characters")
        print(f"Content preview: {article['content'][:300]}...")  # First 300 chars
