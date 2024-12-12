# import random
# import requests
# import os
#
#
# urls = [
#     "https://www.pokemon.com/us/pokedex/Annihilape",
#    "https://www.pokemon.com/us/pokedex/Altaria",
#     "https://www.pokemon.com/us/pokedex/Amaura",
#     "https://www.pokemon.com/us/pokedex/Ambipom",
#     "https://www.pokemon.com/us/pokedex/Amoonguss",
#     'https://www.pokemon.com/us/pokedex/Ampharos',
#     'https://www.pokemon.com/us/pokedex/Annihilape'
# ]
#
# user_agents = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
# ]
#
# cookies = [
#     "django_language=en; visid_incap_2832311=qkXqUexERCe3Vo0+4UAGlJjhz2YAAAAAQUIPAAAAAAAcqQs94bSjN26Fpq3GvHG2; visid_incap_2884021=DfMLtwqARZez7Vy8FiGu6pzhz2YAAAAAQUIPAAAAAAAcKFiQ4PeuCkqAmGOdRrtT; OptanonAlertBoxClosed=2024-08-29T02:49:11.376Z; _ga_7WFP1SND5G=GS1.1.1724899758.1.1.1724899904.0.0.0; __td_signed=true; _ga=GA1.1.1667229379.1692060145; _ga_0HYF2R3MBH=GS1.1.1733450646.3.1.1733452285.0.0.0; nlbi_2884021=FDADCbV7HFTZq07AgQq3qwAAAAC5JsRIYQKvdiWN1sixFxJS; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Dec+06+2024+11%3A31%3A38+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.33.0&isIABGlobal=false&hosts=&consentId=4194fedc-38f0-49fa-81f1-4cf65d509833&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A1%2CC0001%3A1%2CC0004%3A1%2CC0003%3A1&geolocation=HK%3B&AwaitingReconsent=false; _td=990443ad-302a-4c22-8fda-81cac3de3238; crafterSite=pcom-main; incap_ses_335_2884021=85G4KDkfijGIrcPw0CimBM97UmcAAAAAJ/hPYjgQF/scCZZSDMbZWA==; incap_ses_577_2884021=FrCwGbHh9wtnpRawj+oBCAudUmcAAAAAH3rHZ9cHedsRCcwHBLEjuA==; incap_ses_266_2884021=YZmgKz6kGjERU2CAwwWxA8udUmcAAAAAD8jI6guLiVkY1AIW3I9aXA==; incap_ses_627_2884021=J28lXTA5bFTpKDLfS42zCJqfUmcAAAAAl5tFChw7VEDXpN8pIQfYwQ==; AWSALB=mTJEQjbf28OwNKlBXrH1YQ6p21lrQF/HKCX4VNG9JSnSxOJVoT7LBBvGrHBjHJNwj7TC9rZWn6MwQxmzlFHuJLbUGeZH8QSyHBcaX0mZqa8t+Q/Lda4OAfBGlUBz; AWSALBCORS=mTJEQjbf28OwNKlBXrH1YQ6p21lrQF/HKCX4VNG9JSnSxOJVoT7LBBvGrHBjHJNwj7TC9rZWn6MwQxmzlFHuJLbUGeZH8QSyHBcaX0mZqa8t+Q/Lda4OAfBGlUBz; nlbi_2884021_2147483392=VPyxLhz7n0PaTx4bgQq3qwAAAABxTBrGdb6zIndLtcptcr0N; incap_ses_576_2884021=gV79QzR0mibehugPEV3+B3ugUmcAAAAACxo74UOkcUj+5wlm3Pq2bQ==; reese84=3:6+S/U0mORb1iOGCSBH6mWw==:AYGfzvCSGfI7iJleBerzGgrVaGAFZNkkNdbDSFBHyRoMAi2JZlH1rtryWOoWAQdnfSx3vxD7+59a9XvnTUxoWsU2u8kAbdgNHqOChhwdrwjWAbdnahsuZX5ZGf2xfaByt/sLeta0ZvXruFI0p+1NUTZ0DF3SAOZeSj9kD4S7PxfeG9On0oW/reAmAZhqp99T8VawOXT+hRfq5B6LrHYptQIxZh23vvvGTWDwnMCRmXJpLtWjnML0FD3bIJyjmHvixdicFLwRrBFDYwinxwdPGVh3g2Nhlbq0XnpL+ZaBzrGFmVlTTLMlNqbF34eFo+gO7vCLabWaDkOoWIMltOQL26ihBjmd3eaDq4H7yWUvi7Akyo+goCcdFngoplQ32lAG8c6wGm3j4pgbcBe8lQcjKYEJdIY9HnjBrChlGwNEPjEFZJf9ikX4dV0D91m5fdaPpx7aiH0AwAPDmB9lVAmfyw==:jIrbDNiTYX9aWVg7LiwLfURb176baKD8gRFQEKvsRnU="
#     "visid_incap_2884021=EOg34mE4RgmjZdsB6wZ3JftmUWcAAAAAQUIPAAAAAACVjyJRyt569slZhIP1i4bw; django_language=en; nlbi_2884021=zfYzWJr0J1dgjmXEgQq3qwAAAADDku1TjrQlurcez/UJcEnC; incap_ses_576_2884021=d8U+RpLGQHPhwu8PEV3+B8+pUmcAAAAA92fkFUSWtrioXTrjed7XkQ==; nlbi_2884021_2147483392=OjZYTHl96kTNuZfegQq3qwAAAABvczFmW/AMTkpfOBmekO8N; reese84=3:REANpY+mH7+IUj0ocIxf2A==:Igd2xlWZPkQL8NkRUW0s6jMA1W9fzCDwLilERITBVpgzCa8JVH6cY8onYEUC/rtn1vUbuaog0oSD3MIHM5PRy+IwJyJEGv77mz0UQQ5COsCX4qM1VlGNlD4nj16juUL78sPxpFxCTUKQ0AYsV5lx6p0DMkdVGgEedtt2K4ie81apv8OA8bfCBlJkipDqOfHUGOig9YHUIPKOdpXIAzVOkOxv1NfogCLVdNtXAVHwTxbVJg0KgwAa+3UHTOTTk5axHnK7axfaCPOoEKzTdUjCewoPLsJ7ZKZU+d+d/W7i6XMp+n9hFwN8lYo90D775uwM7GK9MWje/q5rtnsZEnzForF73CsJbziULlquYrpThTe6zwSANYX/4zkyq1qMxGwrnbBTDvGvUamgcbfN8RbZdy9Q/de1mXR0vkGCcL+OqMOmhHJ5W4sl+eBI9GG31P00qMbrQjDAd/axNiYThPesSrFwtwx52zrCJXkmda14ZEA=:+vS2F+I2lPR6sDhZuFFjcyAvmijTn3V8sz3FwBWwgAg=; AWSALB=cXeVQCYU/j2YA2Wdf3JiIOPqWD5cgVSro+m3GUYTSbyCp9xCZwKrYZjU9JNxHwEqnCvdjtiUpdEMl0n6/sbQfE4UMoK+uSbzE6S5nrAXyneD/AFfQtjTbG/S6Nct; AWSALBCORS=cXeVQCYU/j2YA2Wdf3JiIOPqWD5cgVSro+m3GUYTSbyCp9xCZwKrYZjU9JNxHwEqnCvdjtiUpdEMl0n6/sbQfE4UMoK+uSbzE6S5nrAXyneD/AFfQtjTbG/S6Nct"
#     "django_language=en; visid_incap_2832311=qkXqUexERCe3Vo0+4UAGlJjhz2YAAAAAQUIPAAAAAAAcqQs94bSjN26Fpq3GvHG2; visid_incap_2884021=DfMLtwqARZez7Vy8FiGu6pzhz2YAAAAAQUIPAAAAAAAcKFiQ4PeuCkqAmGOdRrtT; OptanonAlertBoxClosed=2024-08-29T02:49:11.376Z; _ga_7WFP1SND5G=GS1.1.1724899758.1.1.1724899904.0.0.0; __td_signed=true; _ga=GA1.1.1667229379.1692060145; _ga_0HYF2R3MBH=GS1.1.1733450646.3.1.1733452285.0.0.0; nlbi_2884021=FDADCbV7HFTZq07AgQq3qwAAAAC5JsRIYQKvdiWN1sixFxJS; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Dec+06+2024+11%3A31%3A38+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.33.0&isIABGlobal=false&hosts=&consentId=4194fedc-38f0-49fa-81f1-4cf65d509833&interactionCount=2&landingPath=NotLandingPage&groups=C0002%3A1%2CC0001%3A1%2CC0004%3A1%2CC0003%3A1&geolocation=HK%3B&AwaitingReconsent=false; _td=990443ad-302a-4c22-8fda-81cac3de3238; crafterSite=pcom-main; incap_ses_335_2884021=85G4KDkfijGIrcPw0CimBM97UmcAAAAAJ/hPYjgQF/scCZZSDMbZWA==; incap_ses_577_2884021=FrCwGbHh9wtnpRawj+oBCAudUmcAAAAAH3rHZ9cHedsRCcwHBLEjuA==; incap_ses_266_2884021=YZmgKz6kGjERU2CAwwWxA8udUmcAAAAAD8jI6guLiVkY1AIW3I9aXA==; incap_ses_627_2884021=J28lXTA5bFTpKDLfS42zCJqfUmcAAAAAl5tFChw7VEDXpN8pIQfYwQ==; AWSALB=mTJEQjbf28OwNKlBXrH1YQ6p21lrQF/HKCX4VNG9JSnSxOJVoT7LBBvGrHBjHJNwj7TC9rZWn6MwQxmzlFHuJLbUGeZH8QSyHBcaX0mZqa8t+Q/Lda4OAfBGlUBz; AWSALBCORS=mTJEQjbf28OwNKlBXrH1YQ6p21lrQF/HKCX4VNG9JSnSxOJVoT7LBBvGrHBjHJNwj7TC9rZWn6MwQxmzlFHuJLbUGeZH8QSyHBcaX0mZqa8t+Q/Lda4OAfBGlUBz; nlbi_2884021_2147483392=VPyxLhz7n0PaTx4bgQq3qwAAAABxTBrGdb6zIndLtcptcr0N; incap_ses_576_2884021=gV79QzR0mibehugPEV3+B3ugUmcAAAAACxo74UOkcUj+5wlm3Pq2bQ==; reese84=3:6+S/U0mORb1iOGCSBH6mWw==:AYGfzvCSGfI7iJleBerzGgrVaGAFZNkkNdbDSFBHyRoMAi2JZlH1rtryWOoWAQdnfSx3vxD7+59a9XvnTUxoWsU2u8kAbdgNHqOChhwdrwjWAbdnahsuZX5ZGf2xfaByt/sLeta0ZvXruFI0p+1NUTZ0DF3SAOZeSj9kD4S7PxfeG9On0oW/reAmAZhqp99T8VawOXT+hRfq5B6LrHYptQIxZh23vvvGTWDwnMCRmXJpLtWjnML0FD3bIJyjmHvixdicFLwRrBFDYwinxwdPGVh3g2Nhlbq0XnpL+ZaBzrGFmVlTTLMlNqbF34eFo+gO7vCLabWaDkOoWIMltOQL26ihBjmd3eaDq4H7yWUvi7Akyo+goCcdFngoplQ32lAG8c6wGm3j4pgbcBe8lQcjKYEJdIY9HnjBrChlGwNEPjEFZJf9ikX4dV0D91m5fdaPpx7aiH0AwAPDmB9lVAmfyw==:jIrbDNiTYX9aWVg7LiwLfURb176baKD8gRFQEKvsRnU="
# ]
#
# # 随机选择一个User-Agent
# random_user_agent = random.choice(user_agents)
# random_cookies = random.choice(cookies)
#
# headers = {
#     "User-Agent": f"{random_user_agent}",
#     "cookies": f"{random_cookies}",
# }
#
#
# for url in urls:
#     name = url.split("/")[-1]
#     resp = requests.get(url=url, headers=headers)
#     print(resp.text)
#     with open(f"./test/page/{name}.html", "w", encoding="utf-8") as f:
#         f.write(resp.text)
#         print("写入成功")
#
