from openai import OpenAI
from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncChromiumLoader


def is_sublist(main_list, sublist):
    return any(sublist == sub for sub in main_list)




def extract_text_from_url(url, class_combinations, element_ids=[], elements=['div', 'main'], page_element=False, clean_element_attrs=['href', 'class']):
    """
    Extracts text from a given URL based on specified class combinations and HTML elements.
    
    Args:
        url (str): The URL from which to extract text.
        class_combinations (list): A list of class combinations to filter elements by.
        element_ids (list): A list of element IDs to filter elements by.
        elements (list): List of HTML elements to search for, defaults to ['div', 'main'].
        
    Returns:
        str: The extracted text from the URL based on the provided class combinations and elements.
        
    Example usage
        url = "https://harbourbridge.gov.gy/retraction-schedule"
        class_combinations = [['page-content', 'group'], ['today', 'col'], ['col', 'status', 'upcoming'], ['col', 'schedule', 'upcoming']]
        element_ids = ["page", "content"]
    """


    def clean_element(elements, element_attrs=['href', 'class']):
        # Parse the HTML with BeautifulSoup
        # soup = BeautifulSoup(html, 'html.parser')

        # Find all elements (in this case, we assume a single div with class 'featured')
        # Iterate through each element
        for element in elements:
            # Get current attributes
            attributes = element.attrs

            # Retain only 'href' and 'class'
            element.attrs = {key: attributes[key] for key in attributes if key in element_attrs}

        # Return the modified HTML
        return elements
    
    def has_all_classes(class_attr, class_combinations):
        if class_attr:
            return any(all(cls in class_attr for cls in combo) for combo in class_combinations)
        return False

    loader = AsyncChromiumLoader([url])
    html = loader.load()

    report = ""
    content = []
    last_class = []
    for html_content in html:
        soup = BeautifulSoup(html_content.page_content, 'html.parser')
        if clean_element_attrs:
            # ext_elements = soup.find_all(elements, class_=lambda x: x and has_all_classes(x), recursive = True)
            ext_elements = soup.find_all(elements, class_=lambda x: x and has_all_classes(x, class_combinations), recursive=True)
            ext_clean_elements = clean_element(ext_elements, element_attrs=clean_element_attrs)
            # soup = BeautifulSoup(cleaned_html, 'html.parser')
        else:
            ext_elements = soup.find_all(elements, recursive=True)

        if not page_element:

            for element in ext_elements:
                element_class = element.get('class')
                element_id = element.get('id')
                if class_combinations or element_ids:
                    if is_sublist(class_combinations, element_class) or (element_ids and element_id in element_ids):
                        text = element.get_text(strip=True)
                        report += text + "\n"
                        if last_class != element_class:
                            report += "\n"
                        last_class = element_class
                else:
                    content.append({
                        "text": element.get_text(strip=True),
                        "class": element_class,
                        "element_id": element_id
                    })

    return {"page_content": report, "page_element": content, "page_element": ext_clean_elements}


data = {
    "name": "oil_now",
    "prompt": "Put all the 'title' and their 'link' in a valid json list.\nReturn the full url to the href links.\nWebsite url: {url}\nhtml content:\n{content}\n",
    "url": "https://oilnow.gy/",
    "method": "web_extractor",
    "elements": ['h3'],
    "class_combinations": [['entry-title', 'td-module-title']],
    "element_ids": []
}
oo=extract_text_from_url(url=data['url'], class_combinations=data['class_combinations'], element_ids=data['element_ids'], elements=data['elements'])
print(oo)


def open_ai_call(model, messages):
    client = OpenAI()

    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return completion.choices[0].message


# Example usage
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a haiku about recursion in programming."}
]
model= "gpt-4o"
haiku = open_ai_call(model=model, messages=messages)
print(haiku)
