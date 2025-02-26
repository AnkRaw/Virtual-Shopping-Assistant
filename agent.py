import re
import json
import requests
from tools import search_products, estimate_shipping, apply_discount, compare_prices, get_return_policy

class ShoppingAgent:
    def __init__(self):
        self.api_url = "http://localhost:1234/v1/chat/completions"  # LM Studio API endpoint
        self.model_name = "mistral-7b-instruct-v0.3"  # Model name (update if different)
        self.prompt_file = "./prompts/system_prompt.txt"  # Path to the prompt file
        self.response_prompt_file = "./prompts/response_prompt.txt"
    
    def parse_query_with_base_model(self, user_query):
        """Uses LM Studio's hosted API to parse the query into structured JSON."""
        
        # Read the predefined prompt template
        with open(self.prompt_file, "r") as file:
            prompt_template = file.read()
        
        # Inject user query into the prompt
        prompt = prompt_template.replace("{user_query}", user_query)
        
        # Prepare the API request payload (NO "system" ROLE)
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 2084,
            "stream": False
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()  # Raise an error for HTTP issues
            
            parsed_response = response.json()

            # Ensuring that we are extracting only the JSON content
            structured_data = parsed_response.get("choices", [{}])[0].get("message", {}).get("content", "")

            # Strip non-JSON parts (if any) and parse it
            json_start = structured_data.find("[")
            json_end = structured_data.rfind("]") + 1
            if json_start != -1 and json_end != -1:
                structured_data = structured_data[json_start:json_end]

            return json.loads(structured_data)

        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error Query Parsing: {e}")
            return None  # Handling error
    
    def generate_human_response(self, structured_results, user_query):
        """Formats structured tool results into a human-friendly response using LM Studio."""
        with open(self.response_prompt_file, "r") as file:
            response_prompt_template = file.read()
        
        response_prompt_template = response_prompt_template.replace("{user_query}", user_query)
        prompt = response_prompt_template.replace("{results}", json.dumps(structured_results, indent=2))

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 300,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=15)
            response.raise_for_status()
            parsed_response = response.json()

            return parsed_response.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error generating response with LM Studio: {e}")
            return "Sorry, I encountered an issue generating your response."
    
    def process_query(self, user_query):
        """Determines tools to invoke based on LLM-generated JSON and returns a structured response."""
        
        response = {"thoughts": [], "actions": [], "final_response": ""}

        # Step 1: Use LM Studio API to parse the query
        structured_query = self.parse_query_with_base_model(user_query)
        
        if not structured_query:
            response["final_response"] = "Error processing query. Please try again."
            return response

        response["thoughts"].append(f"Extracted structured query: {structured_query}")
        
        # Step 2: Determine appropriate tool calls
        results = {}

        for query_part in structured_query:
            query_type = query_part["type"]
            item = query_part["item"]
            attributes = query_part.get("attributes", [])
            budget = ''.join(re.findall(r'\d', query_part.get("budget", "")))
            discount_code = query_part.get("discount_code", "")
            delivery = query_part.get("delivery", "")

            if query_type == "find":
                response["thoughts"].append(f"Searching for {item} with attributes {attributes} under ${budget}.")
                results["search"] = search_products(query=item, max_price=int(budget) if budget else None)

            if query_type == "discount":
                response["thoughts"].append(f"Applying discount code {discount_code} for {item}.")
                results["discount"] = apply_discount(base_price=35, promo_code=discount_code)

            if query_type == "shipping":
                response["thoughts"].append(f"Estimating shipping for {item} with deadline {delivery}.")
                results["shipping"] = estimate_shipping(location="New York", delivery_deadline=3)

            if query_type == "prices":
                response["thoughts"].append(f"Comparing prices for {item}.")
                results["comparison"] = compare_prices(product_name=item)

            if query_type == "return_policy":
                response["thoughts"].append(f"Checking return policy for {item}.")
                results["return_policy"] = get_return_policy(store_name="SiteB")

        response["actions"].append(f"Executed tools: {list(results.keys())}")
        response["final_response"] = self.generate_human_response(results, user_query)

        return response
