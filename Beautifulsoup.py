from bs4 import BeautifulSoup
import requests


# Specify the correct encoding when opening the file
# with open("Current event.html", "r", encoding="utf-8") as htmlFile:
#     content = htmlFile.read()
url = "https://en.wikipedia.org/wiki/Portal:Current_events"

# Define the custom User-Agent header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

# Send a GET request with the custom User-Agent
response = requests.get(url, headers=headers)

# Ensure the request was successful
if response.status_code == 200:
    content = response.content
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'lxml')
    soup.prettify()


   
    # Create a dictionary to store the events
    events_data = {}

    # Find all the sections corresponding to each date
    sections = soup.find_all('div', class_='current-events-main vevent')

    for section in sections:
        # Extract the date
        date_heading = section.find('span', class_='summary')
        if date_heading:
            date = date_heading.text.strip()
            events = []
            
            # Find all the event categories (e.g., Armed conflicts and attacks, Disasters and accidents)
            categories = section.find_all('p')
            for category in categories:
                category_name = category.find('b')
                if category_name:
                    category_name = category_name.text.strip()
                    
                    # Extract the event details under this category
                    category_events = category.find_next('ul').find_all('li')
                    for event in category_events:
                        event_details = {}
                        
                        # Extract the main event text safely
                        main_event = event.get_text(strip=True) if event.get_text(strip=True) else "No main event text available"
                        event_details['main_event'] = main_event
                        
                        # Extract sub-events if present
                        sub_events = event.find_all('ul')
                        sub_event_list = []
                        for sub_event in sub_events:
                            for sub_event_item in sub_event.find_all('li'):
                                sub_event_list.append(sub_event_item.get_text(strip=True))
                        
                        event_details['sub_events'] = sub_event_list
                        
                        # Append event details to the events list
                        events.append({
                            'category': category_name,
                            'event_details': event_details
                        })
            
            # Add the date and its events to the events_data dictionary
            events_data[date] = events

    # Printing the result
    for date, events in events_data.items():
        print(f"Date: {date}")
        for event in events:
            print(f"  Category: {event['category']}")
            print(f"    Main Event: {event['event_details']['main_event']}")
            if event['event_details']['sub_events']:
                print("    Sub Events:")
                for sub_event in event['event_details']['sub_events']:
                    print(f"      - {sub_event}")
        print("\n\t\t--------------------------------------------------------------\n")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")