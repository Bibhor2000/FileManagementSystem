import toga
from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

connection = MySQLdb.connect(
  host= os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd= os.getenv("DB_PASSWORD"),
  db= os.getenv("DB_NAME"),
  autocommit = True,
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "/etc/ssl/cert.pem"
  }
)
  
# finally:
#     # Close the cursor and connection
#     cursor.close()
#     connection.close()


class IntroScreen(toga.App):
    def startup(self):
        # Create a label with a welcome message
        welcome_label = toga.Label(
            'Welcome to Your App!',
            style=Pack(
                font_size=30,
                color='#33cc99'  # Dark green text color
            )
        )

        # Create another label with additional information
        info_label = toga.Label(
            'This is a basic introductory page.',
            style=Pack(
                font_size=20,
                color='#6666cc'  # Purple text color
            )
        )

        # Create a button
        button = toga.Button(
            'Click Me!',
            on_press=self.button_pressed,
            style=Pack(
                font_size=18,
                background_color='#33cc99'  # Dark green button color
            )
        )

        # Create a box layout
        box = toga.Box(
            children=[welcome_label, info_label, button],
            style=Pack(
                direction='column',
                padding=10
            )
        )

        # Set the main window
        self.main_window = toga.MainWindow(title='Intro Screen', content=box)

    def button_pressed(self, widget):
        print('Button Clicked!')

if __name__ == '__main__':
    IntroScreen().main_loop()

