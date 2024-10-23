import requests
from bs4 import BeautifulSoup
from langchain.schema import Document

def extract_course_data():
    url = "https://brainlox.com/courses/category/technical"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    courses = []
    course_cards = soup.find_all('div', class_='courses-content')
    
    for card in course_cards:
        title_tag = card.find('h3')
        description_tag = card.find('p')
        link_tag = card.find('a', href=True)

        if title_tag and description_tag and link_tag:
            title = title_tag.text.strip()
            description = description_tag.text.strip()
            link = link_tag['href']

            doc = Document(page_content=description, metadata={'title': title, 'url': link})
            courses.append(doc)

    return courses

# For debugging, you can print extracted courses like this
if __name__ == "__main__":
    extracted_courses = extract_course_data()
    for course in extracted_courses:
        print(course.page_content, course.metadata)
