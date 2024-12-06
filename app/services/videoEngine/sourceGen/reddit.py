import requests
from bs4 import BeautifulSoup

# Function to scrape data from the provided URL
def get_content(url):
    headers = {
        "Host": "www.reddit.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://www.reddit.com/r/shortscarystories/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Connection": "keep-alive",
        "Cookie": "edgebucket=FNercImo374MRhJbqD; loid=000000000000091nmd.2.1347950984967.Z0FBQUFBQmx1OWFkY2cxTjhQTGhoS2U5VHMtckZocmZGUEVEZC16THdMWWptYm9JS09fSTdTdTllZXhMLTFrRTVNNTFoVnU5YUhJUGxtNnNXdXZ6Ui1CWlBUVFFld3QwR2xwNWFVYUFUZkdHUnlXNjZxcHNxVWFmMW5EUWxvNGRXeERobHk5ZTlveXk; csv=2; g_state={\"i_l\":0}; reddit_session=\"15193813,2024-08-01T09:20:23,812b37a1c6eaa445859842cace27ba2e0005896d\"; theme=2; recent_srs=t5_2qh1q%2C; t2_91nmd_recentclicks3=t3_1fy6xw3%2Ct3_1fy5ftx%2Ct3_1fy2uhm%2Ct3_fosqhb%2Ct3_k28hhq%2Ct3_19a70su%2Ct3_1ft8a4i%2Ct3_1ftbuh5%2Ct3_1ftbzvd%2Ct3_1fsphbe; pc=hg; __stripe_mid=71b5e356-8936-4738-b258-f74d5ecc17c4d971a7; session_tracker=eqhqblikmgbrpdhlld.0.1728322136580.Z0FBQUFBQm5CQnBZQlZ1ZlIyM2J5RV9tS1dkMTd3eUoxLV9MbFVBdEY0cG5uVkFxbUdqaG51TjdudC11QjEtVHg3SkNLTE1EVzVBZndHazlPbE5rZHVnYk5uRWtNMEtQQlMtWEdUS29nQ2IwS1VFYmpnbzJLNXBCRG5rMGtyY0pxbGp5NmhycWFweko; csrf_token=88b41a92104c55a895540ed3ae41d61e; token_v2=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzI4MzkwNzMyLjQ4ODA5LCJpYXQiOjE3MjgzMDQzMzIuNDg4MDksImp0aSI6InNqRTZ4NDl5cUxPLU0zNzZaRXVXS196Qno4aDB6USIsImNpZCI6IjBSLVdBTWh1b28tTXlRIiwibGlkIjoidDJfOTFubWQiLCJhaWQiOiJ0Ml85MW5tZCIsImxjYSI6MTM0Nzk1MDk4NDk2Nywic2NwIjoiZUp4a2tkR090REFJaGQtbDF6N0JfeXBfTmh0c2NZYXNMUWFvazNuN0RWb2NrNzA3Y0w0aUhQOG5LSXFGTEUydUJLR2tLV0VGV3RPVU5pTHY1OHk5T1pFRlN5RlRSODQzeXdva2FVcFBVbU41cHlsUndXWmtMbGZhc1VLREI2WXBWUzZaMjBLUFM1dlEzSTFGejA2TXFseFdIdFRZbzNKcGJHTUsyeFBqemNacVF5cXV5NmxNWUZrb244V0xmdnlHLXRZLWY3YmZoSFl3cktnS0RfVE91Rnh3WV9IREZIYl9ucHIwYkYyd3FMM1hnOVEtMS1OMjdiTm1vZG01X1Z6UHZ6YVNjVG1HNWlmWXY3dC1DUjE0NUhtWlVRY3dZZzBfeXJBajZfQ3ZPb0RLQlFXTUpZaFBJNUFybDJfX0pkaXVUZjhhdHlkLS1HYkVUV180clJtbzV4TEVvVV9qNnpjQUFQX19YRF9lNHciLCJyY2lkIjoidHp0VXdjQmd0NGhVUGNBUWtFRjJ5Q2hES1Z6MGc2MnJYYzNmeFk1Wm83WSIsImZsbyI6Mn0.f4qkphS47eGftbGtfYEkkjaZ7T4xjT3yTW_SkVyypkq7Jr_QdtYJOWfMfIQ2liT_WgWXBDJOL7XLPgY8LVvFniVNhtVV8i5lzJ_BND_qPqmhQ0dRmswhms2XFywm-fSz70x618ZM6TECISHIEZOMKktFulNp8NOjXaHtjunMlIN6ooxubUyancTWNeWlJA_PKpF6zOh9F5qZR9PwXPMZ-n0svqpUiav4zzF5vn6DUiWUg6q9r8bPiTLdvfXzMhpRT9bZaUYGPXi7lUyI1KDMWxychPr8alUxZid41wSxETcxQ-6UTMMS4sI-Ve2eJ245K4CHz4ixntiUROCxdtXu5w",
        "Priority": "u=0, i",
        "TE": "trailers"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract the title using the specific identifier
            title = soup.find('h1', slot='title').get_text(strip=True) if soup.find('h1', slot='title') else 'Title not found'
            
            # Extract the body text using the specific identifier
            body_div = soup.find('div', slot='text-body')
            body = body_div.get_text(separator='\n', strip=True) if body_div else 'Body text not found'
            
            return {'title': title, 'body': body}
        else:
            return {'title': 'Error', 'body': f'Failed to retrieve content. Status code: {response.status_code}'}
    except Exception as e:
        return {'title': 'Error', 'body': f'An error occurred: {str(e)}'}
