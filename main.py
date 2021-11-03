from markdown import markdown
import pdfkit
import requests

from os import rename


class Joplin:
    def __init__(self, token):
        self.token = token

    # This solution was discarded due to the Event api not returning changes as expected
    # # Get the id of the most recently edited note
    # def __get_recently_edited_id(self):
    #     response = requests.get("http://localhost:41184/events", params={'token': self.token, 'fields': ''})
    #     return response.json
    #
    # # Get the markdown source of a note given its id
    # def __get_note_by_id(self, note_id):
    #     response = requests.get(f"http://localhost:41184/notes/{note_id}", params={'token': self.token, 'fields': 'body'})
    #     return response.json()['body']

    # Get the markdown source of the most recently edited note
    def get_most_recent_note(self):
        parameters = {
            'token': self.token,
            'fields': 'body,user_updated_time,title',
            'limit': 1,
            'order_by': 'user_updated_time',
            'order_dir': 'DESC'
        }
        response = requests.get('http://localhost:41184/notes', params=parameters)
        # Returns the first item returned, which will be the most recently updated
        note = response.json()['items'][0]
        body = note['body']
        title = note['title']
        return body, title


if __name__ == '__main__':
    filepath = ''  # The filepath where the pdf should be stored
    token = ''  # The Joplin Clipper service authorization token
    # Get the markdown source of the most recently edited note
    joplin = Joplin(token)
    markdown_note, title = joplin.get_most_recent_note()
    # Convert the markdown to html
    html = markdown(markdown_note)
    # Convert the html to a pdf
    config = pdfkit.configuration(wkhtmltopdf='<path/to/wkhtmltopdf.exe>')
    pdfkit.from_string(html, f'{title}.pdf', configuration=config)
    # Save the pdf with the correct name in the Stream Net Meetings folder
    rename(f'{title}.pdf', f'{filepath}\\{title}.pdf')
