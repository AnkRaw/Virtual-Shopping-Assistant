from agent import ShoppingAgent

def run_assistant():
    agent = ShoppingAgent()
    
    test_queries = [
        "Find me a leather jacket in black, size L, for under $150.",
        "Are there any discounts on running shoes in size 10?",
        "I need sunglasses for under $100 with free shipping.",
        "Check if there’s a better deal on a Casual Denim Jacket than $80.",
        "Does SiteB allow returns for leather jackets?",
        "Can I apply both 'SAVE10' and 'FASHION20' to my purchase?",
        "Find a winter coat in size XL under $120.",
        "Compare prices of white sneakers on different sites.",
        "What’s the return policy for SiteD on backpacks?",
        "Are there any size M yellow graphic t-shirts in stock?",
        "Locate the cheapest pair of formal trousers in size 32.",
        "Do SiteC and SiteE offer exchanges for winter coats?",
        "Is the green backpack available in any store right now?",
        "Show me the best deal on sunglasses under $100.",
        "Find a stylish black leather jacket under $150 with fast shipping.",
        "Do I get free shipping if I use the 'FREESHIP' code?",
        "Can I return running shoes from SiteA if I don’t like them?",
        "I found leather jackets on SiteA and SiteC. Which one is cheaper?",
        "Apply the best discount code to a Casual Denim Jacket.",
        "Which store has the best price on a navy formal trouser size 32?",
    ]

    task_queries = [
        "Find a floral skirt under $40 in size S. Is it in stock, and can I apply a discount code ‘SAVE10’?",
        "I need white sneakers (size 8) for under $70 that can arrive by Friday.",
        "I found a ‘casual denim jacket’ at $80 on SiteA. Any better deals?",
        "I want to buy a cocktail dress from SiteB, but only if returns are hassle-free. Do they accept returns?",
        "Find me a black leather jacket in size L under $150. Check if there are any discounts available. Compare its price across different stores. If I order today, can it arrive within 3 days? Also, what’s the return policy for SiteB?"
    ]

    for query in task_queries:
        try:
            print(f"\n**User:** {query}")
            response = agent.process_query(query)
            # print(f"**Agent Thought Process:** {response['thoughts']}")
            # print(f"**Agent Actions:** {response['actions']}")
            print(f"**Final Response:** {response['final_response']}")
        except:
            print("Error occured while solving query.")

if __name__ == "__main__":
    run_assistant()
