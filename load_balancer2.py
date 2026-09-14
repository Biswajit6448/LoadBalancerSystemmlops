
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.image import Image, AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty, BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.carousel import Carousel
from kivy.uix.stacklayout import StackLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.widget import Widget
import os
import json
import bcrypt
import shutil
import datetime
import calendar
from functools import partial
from PIL import Image as PILImage
import io
import base64
import random
import re
import time
from pathlib import Path

# Set mobile-friendly window size for testing
Window.size = (400, 700)

# Load KV file for UI
Builder.load_string('''
#:import utils kivy.utils
#:import Factory kivy.factory.Factory

<RoundedButton@Button>:
    background_color: 0, 0, 0, 0
    background_normal: ''
    canvas.before:
        Color:
            rgba: (0.2, 0.6, 0.8, 1) if self.state == 'normal' else (0.1, 0.5, 0.7, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15]

<CustomSpinner@Spinner>:
    background_color: 0, 0, 0, 0
    background_normal: ''
    canvas.before:
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10]

<CustomTextInput@TextInput>:
    background_color: 0.95, 0.95, 0.95, 1
    foreground_color: 0.2, 0.2, 0.2, 1
    padding: [10, 10]
    font_size: '16sp'
    multiline: False
    cursor_color: 0.2, 0.6, 0.8, 1
    canvas.before:
        Color:
            rgba: 0.8, 0.8, 0.8, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 5)
            width: 1.5

<HeaderLabel@Label>:
    font_size: '20sp'
    bold: True
    color: 0.2, 0.6, 0.8, 1
    size_hint_y: None
    height: dp(40)

<SubHeaderLabel@Label>:
    font_size: '18sp'
    color: 0.3, 0.3, 0.3, 1
    size_hint_y: None
    height: dp(30)

<TransactionItem>:
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.95, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10]
        Color:
            rgba: utils.get_color_from_hex('#2196F3') if root.trans_type == 'Income' else utils.get_color_from_hex('#F44336')
        RoundedRectangle:
            pos: self.x + dp(5), self.y + dp(5)
            size: dp(8), self.height - dp(10)
            radius: [5]
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(5)
    size_hint_y: None
    height: dp(80)

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(25)

        Label:
            text: root.category
            font_size: '16sp'
            bold: True
            halign: 'left'
            text_size: self.size
            valign: 'middle'

        Label:
            text: f"₹{root.amount}"
            font_size: '16sp'
            bold: True
            color: utils.get_color_from_hex('#2196F3') if root.trans_type == 'Income' else utils.get_color_from_hex('#F44336')
            halign: 'right'
            text_size: self.size
            valign: 'middle'

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(20)

        Label:
            text: root.description
            font_size: '14sp'
            halign: 'left'
            text_size: self.size
            valign: 'middle'
            shorten: True
            shorten_from: 'right'

        Label:
            text: root.date
            font_size: '14sp'
            color: 0.5, 0.5, 0.5, 1
            halign: 'right'
            text_size: self.size
            valign: 'middle'

<DocumentItem>:
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.95, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10]
    orientation: 'horizontal'
    padding: dp(10)
    spacing: dp(10)
    size_hint_y: None
    height: dp(90)

    AsyncImage:
        source: 'atlas://data/images/defaulttheme/filechooser_file' if not root.thumbnail else root.thumbnail
        size_hint: None, None
        size: dp(60), dp(60)

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(2)

        Label:
            text: root.name
            font_size: '16sp'
            bold: True
            halign: 'left'
            text_size: self.size
            valign: 'middle'

        Label:
            text: f"Type: {root.doc_type}"
            font_size: '14sp'
            halign: 'left'
            text_size: self.size
            valign: 'middle'

        Label:
            text: f"Added: {root.date}"
            font_size: '14sp'
            color: 0.5, 0.5, 0.5, 1
            halign: 'left'
            text_size: self.size
            valign: 'middle'

    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.3
        spacing: dp(5)

        RoundedButton:
            text: 'View'
            font_size: '14sp'
            size_hint_y: 0.5
            on_release: root.view_document()

        RoundedButton:
            text: 'Delete'
            font_size: '14sp'
            size_hint_y: 0.5
            background_color: 0, 0, 0, 0
            canvas.before:
                Color:
                    rgba: (0.9, 0.3, 0.3, 1) if self.state == 'normal' else (0.8, 0.2, 0.2, 1)
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [15]
            on_release: root.delete_document()

<StatCard>:
    canvas.before:
        Color:
            rgba: root.card_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15]
    orientation: 'vertical'
    padding: dp(15)
    spacing: dp(5)
    size_hint: 1, None
    height: dp(100)

    Label:
        text: root.title
        font_size: '16sp'
        bold: True
        color: 1, 1, 1, 1
        halign: 'left'
        text_size: self.size
        valign: 'bottom'
        size_hint_y: 0.4

    Label:
        text: root.value
        font_size: '24sp'
        bold: True
        color: 1, 1, 1, 1
        halign: 'left'
        text_size: self.size
        valign: 'top'
        size_hint_y: 0.6

<MenuButton@Button>:
    background_color: 0, 0, 0, 0
    background_normal: ''
    size_hint_y: None
    height: dp(50)
    canvas.before:
        Color:
            rgba: 0.2, 0.6, 0.8, 0.1 if self.state == 'normal' else 0.2, 0.6, 0.8, 0.2
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10]

<ConfirmPopup>:
    size_hint: 0.8, 0.3
    auto_dismiss: False
    title: ''

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)

        Label:
            text: root.message
            font_size: '16sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.size

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint_y: None
            height: dp(50)

            RoundedButton:
                text: 'Cancel'
                on_release: root.dispatch('on_cancel')

            RoundedButton:
                text: 'Confirm'
                on_release: root.dispatch('on_confirm')
                canvas.before:
                    Color:
                        rgba: (0.9, 0.3, 0.3, 1) if self.state == 'normal' else (0.8, 0.2, 0.2, 1)
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [15]
''')

class TransactionItem(BoxLayout):
    """Custom widget for displaying transaction items."""
    category = StringProperty('')
    amount = StringProperty('')
    description = StringProperty('')
    date = StringProperty('')
    trans_type = StringProperty('')
    trans_id = StringProperty('')

    def __init__(self, **kwargs):
        self.trans_id = kwargs.pop('trans_id', '')
        self.category = kwargs.pop('category', '')
        self.amount = kwargs.pop('amount', '')
        self.description = kwargs.pop('description', '')
        self.date = kwargs.pop('date', '')
        self.trans_type = kwargs.pop('trans_type', '')
        super(TransactionItem, self).__init__(**kwargs)

class DocumentItem(BoxLayout):
    """Custom widget for displaying document items."""
    name = StringProperty('')
    doc_type = StringProperty('')
    date = StringProperty('')
    path = StringProperty('')
    thumbnail = StringProperty('')
    doc_id = StringProperty('')

    def __init__(self, **kwargs):
        self.doc_id = kwargs.pop('doc_id', '')
        self.name = kwargs.pop('name', '')
        self.doc_type = kwargs.pop('doc_type', '')
        self.date = kwargs.pop('date', '')
        self.path = kwargs.pop('path', '')
        self.thumbnail = kwargs.pop('thumbnail', '')
        super(DocumentItem, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def view_document(self):
        """Open document for viewing."""
        if self.app:
            self.app.view_document(self.doc_id)

    def delete_document(self):
        """Delete document after confirmation."""
        if self.app:
            self.app.confirm_delete_document(self.doc_id, self.name)

class StatCard(BoxLayout):
    """Custom widget for displaying statistics."""
    title = StringProperty('')
    value = StringProperty('')
    card_color = ListProperty([0.2, 0.6, 0.8, 1])

    def __init__(self, **kwargs):
        self.title = kwargs.pop('title', '')
        self.value = kwargs.pop('value', '')
        self.card_color = kwargs.pop('color', [0.2, 0.6, 0.8, 1])
        super(StatCard, self).__init__(**kwargs)

class ConfirmPopup(Popup):
    """Confirmation popup for sensitive actions."""
    message = StringProperty('')

    def __init__(self, message, **kwargs):
        self.message = message
        self.register_event_type('on_confirm')
        self.register_event_type('on_cancel')
        super(ConfirmPopup, self).__init__(**kwargs)

    def on_confirm(self, *args):
        """Event handler for confirmation."""
        self.dismiss()

    def on_cancel(self, *args):
        """Event handler for cancellation."""
        self.dismiss()

class LoginScreen(Screen):
    """Screen for user login."""
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.name = 'login'

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Logo area
        logo_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        logo = Image(source='atlas://data/images/defaulttheme/filechooser_selected')
        app_name = Label(text='FIN-DOC MANAGER', font_size='28sp', bold=True, color=(0.2, 0.6, 0.8, 1))
        logo_layout.add_widget(logo)
        logo_layout.add_widget(app_name)
        layout.add_widget(logo_layout)

        # Form
        form_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(1, 0.5))

        self.username = TextInput(hint_text='Username', multiline=False,
                                  size_hint=(1, None), height=dp(50),
                                  padding=[dp(15), dp(15)], font_size='16sp')

        self.password = TextInput(hint_text='Password', password=True, multiline=False,
                                 size_hint=(1, None), height=dp(50),
                                 padding=[dp(15), dp(15)], font_size='16sp')

        form_layout.add_widget(Label(text='Welcome Back!', font_size='22sp', color=(0.3, 0.3, 0.3, 1),
                                     size_hint=(1, None), height=dp(40)))
        form_layout.add_widget(Label(text='Username', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.username)
        form_layout.add_widget(Label(text='Password', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.password)

        # Remember me and forgot password
        options_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))

        forgot_pwd = Button(text='Forgot Password?', background_color=(0, 0, 0, 0), color=(0.2, 0.6, 0.8, 1),
                            size_hint=(0.5, 1), halign='right', font_size='14sp')
        options_layout.add_widget(Widget(size_hint=(0.5, 1)))  # Spacer
        options_layout.add_widget(forgot_pwd)
        form_layout.add_widget(options_layout)

        layout.add_widget(form_layout)

        # Buttons
        btn_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(1, 0.2))

        login_btn = Button(text='LOGIN', background_color=(0.2, 0.6, 0.8, 1),
                          size_hint=(1, None), height=dp(50), font_size='18sp')
        login_btn.bind(on_press=self.login)

        register_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        register_layout.add_widget(Label(text="Don't have an account?", font_size='14sp', color=(0.5, 0.5, 0.5, 1)))

        register_btn = Button(text='Register Now', background_color=(0, 0, 0, 0), color=(0.2, 0.6, 0.8, 1),
                             size_hint=(0.4, 1), font_size='14sp')
        register_btn.bind(on_press=self.switch_to_register)
        register_layout.add_widget(register_btn)

        btn_layout.add_widget(login_btn)
        btn_layout.add_widget(register_layout)

        layout.add_widget(btn_layout)

        self.add_widget(layout)

    def login(self, instance):
        """Handle user login."""
        username = self.username.text
        password = self.password.text

        if not username or not password:
            self.show_error_popup('Please enter both username and password')
            return

        user_data = load_user_data(username)
        if user_data and check_password(user_data['password'].encode('utf-8'), password):
            app = App.get_running_app()
            app.current_user = username
            app.load_user_data(username)

            # Transition to main screen
            self.parent.transition = SlideTransition(direction='left')
            self.parent.current = 'main'
        else:
            self.show_error_popup('Invalid username or password')

    def switch_to_register(self, instance):
        """Switch to the registration screen."""
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current = 'register'

    def show_error_popup(self, message):
        """Display an error popup with the given message."""
        popup = Popup(title='Error', size_hint=(0.8, 0.3))
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        layout.add_widget(Label(text=message, font_size='16sp'))

        close_btn = Button(text='OK', size_hint=(None, None), size=(dp(100), dp(40)))
        close_btn.bind(on_press=popup.dismiss)

        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        btn_layout.add_widget(Widget())  # Spacer
        btn_layout.add_widget(close_btn)
        btn_layout.add_widget(Widget())  # Spacer

        layout.add_widget(btn_layout)
        popup.content = layout
        popup.open()

class RegisterScreen(Screen):
    """Screen for user registration."""
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.name = 'register'

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Header
        header = Label(text='Create New Account', font_size='24sp', bold=True, color=(0.2, 0.6, 0.8, 1),
                       size_hint=(1, 0.15))
        layout.add_widget(header)

        # Form
        form_layout = GridLayout(cols=1, spacing=dp(10), size_hint=(1, 0.65))

        self.reg_username = TextInput(hint_text='Username', multiline=False,
                                     size_hint=(1, None), height=dp(50),
                                     padding=[dp(15), dp(15)], font_size='16sp')

        self.reg_email = TextInput(hint_text='Email', multiline=False,
                                  size_hint=(1, None), height=dp(50),
                                  padding=[dp(15), dp(15)], font_size='16sp')

        self.reg_password = TextInput(hint_text='Password', password=True, multiline=False,
                                     size_hint=(1, None), height=dp(50),
                                     padding=[dp(15), dp(15)], font_size='16sp')

        self.reg_confirm = TextInput(hint_text='Confirm Password', password=True, multiline=False,
                                    size_hint=(1, None), height=dp(50),
                                    padding=[dp(15), dp(15)], font_size='16sp')

        form_layout.add_widget(Label(text='Username', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.reg_username)

        form_layout.add_widget(Label(text='Email', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.reg_email)

        form_layout.add_widget(Label(text='Password', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.reg_password)

        form_layout.add_widget(Label(text='Confirm Password', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.reg_confirm)

        layout.add_widget(form_layout)

        # Buttons
        btn_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(1, 0.2))

        register_btn = Button(text='REGISTER', background_color=(0.2, 0.6, 0.8, 1),
                             size_hint=(1, None), height=dp(50), font_size='18sp')
        register_btn.bind(on_press=self.register)

        login_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        login_layout.add_widget(Label(text="Already have an account?", font_size='14sp', color=(0.5, 0.5, 0.5, 1)))

        login_btn = Button(text='Login Now', background_color=(0, 0, 0, 0), color=(0.2, 0.6, 0.8, 1),
                          size_hint=(0.3, 1), font_size='14sp')
        login_btn.bind(on_press=self.switch_to_login)
        login_layout.add_widget(login_btn)

        btn_layout.add_widget(register_btn)
        btn_layout.add_widget(login_layout)

        layout.add_widget(btn_layout)

        self.add_widget(layout)

    def register(self, instance):
        """Handle user registration."""
        username = self.reg_username.text
        email = self.reg_email.text
        password = self.reg_password.text
        confirm = self.reg_confirm.text

        if not all([username, email, password, confirm]):
            self.show_error_popup('Please fill all fields')
            return

        if password != confirm:
            self.show_error_popup('Passwords do not match')
            return

        if not validate_email(email):
            self.show_error_popup('Please enter a valid email address')
            return

        app = App.get_running_app()
        app.register_user(username, email, password)

        self.show_success_popup('Account created successfully')
        self.switch_to_login(instance)

    def validate_email(self, email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    def switch_to_login(self, instance):
        """Switch to the login screen."""
        self.parent.transition = SlideTransition(direction='right')
        self.parent.current = 'login'

    def show_error_popup(self, message):
        """Display an error popup with the given message."""
        popup = Popup(title='Error', size_hint=(0.8, 0.3))
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        layout.add_widget(Label(text=message, font_size='16sp'))

        close_btn = Button(text='OK', size_hint=(None, None), size=(dp(100), dp(40)))
        close_btn.bind(on_press=popup.dismiss)

        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        btn_layout.add_widget(Widget())  # Spacer
        btn_layout.add_widget(close_btn)
        btn_layout.add_widget(Widget())  # Spacer

        layout.add_widget(btn_layout)
        popup.content = layout
        popup.open()

    def show_success_popup(self, message):
        """Display a success popup with the given message."""
        popup = Popup(title='Success', size_hint=(0.8, 0.3))
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        layout.add_widget(Label(text=message, font_size='16sp'))

        close_btn = Button(text='OK', size_hint=(None, None), size=(dp(100), dp(40)))
        close_btn.bind(on_press=popup.dismiss)

        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        btn_layout.add_widget(Widget())  # Spacer
        btn_layout.add_widget(close_btn)
        btn_layout.add_widget(Widget())  # Spacer

        layout.add_widget(btn_layout)
        popup.content = layout
        popup.open()

class MainScreen(Screen):
    """Main screen of the application with a dashboard."""
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.name = 'main'

        # Main layout
        main_layout = BoxLayout(orientation='vertical')

        # Top bar with user info
        self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), padding=[dp(15), dp(5)])
        self.profile_button = Button(text='', background_color=(0, 0, 0, 0), halign='right')
        self.profile_button.bind(on_press=self.show_profile_popup)
        self.top_bar.add_widget(Label(text='Dashboard', font_size='18sp', bold=True, halign='left',
                                      size_hint=(0.7, 1)))
        self.top_bar.add_widget(self.profile_button)
        main_layout.add_widget(self.top_bar)

        # Content area with dashboard
        self.content_area = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))

        # Stats cards
        stats_layout = GridLayout(cols=2, spacing=dp(15), size_hint=(1, None), height=dp(220))

        self.balance_card = StatCard(title='Total Balance', value='₹0.00', color=[0.2, 0.6, 0.8, 1])
        self.income_card = StatCard(title='Income', value='₹0.00', color=[0.2, 0.8, 0.4, 1])
        self.expense_card = StatCard(title='Expenses', value='₹0.00', color=[0.8, 0.3, 0.3, 1])
        self.doc_card = StatCard(title='Documents', value='0', color=[0.5, 0.5, 0.8, 1])

        stats_layout.add_widget(self.balance_card)
        stats_layout.add_widget(self.income_card)
        stats_layout.add_widget(self.expense_card)
        stats_layout.add_widget(self.doc_card)

        self.content_area.add_widget(stats_layout)

        # Navigation buttons
        nav_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, None), height=dp(50))

        trans_btn = Button(text='Transactions', background_color=(0.2, 0.6, 0.8, 1),
                          size_hint=(0.5, 1), font_size='18sp')
        trans_btn.bind(on_press=self.view_transactions)

        doc_btn = Button(text='Documents', background_color=(0.2, 0.6, 0.8, 1),
                        size_hint=(0.5, 1), font_size='18sp')
        doc_btn.bind(on_press=self.view_documents)

        nav_layout.add_widget(trans_btn)
        nav_layout.add_widget(doc_btn)

        self.content_area.add_widget(nav_layout)

        main_layout.add_widget(self.content_area)

        self.add_widget(main_layout)

    def show_profile_popup(self, instance):
        """Show a popup with user profile information."""
        popup = Popup(title='User Profile', size_hint=(0.8, 0.5))
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        layout.add_widget(Label(text='User Profile', font_size='18sp', bold=True))
        layout.add_widget(Label(text='Username: ' + App.get_running_app().current_user, font_size='16sp'))
        layout.add_widget(Label(text='Email: user@example.com', font_size='16sp'))

        close_btn = Button(text='Close', size_hint=(None, None), size=(dp(100), dp(40)))
        close_btn.bind(on_press=popup.dismiss)

        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        btn_layout.add_widget(Widget())  # Spacer
        btn_layout.add_widget(close_btn)
        btn_layout.add_widget(Widget())  # Spacer

        layout.add_widget(btn_layout)
        popup.content = layout
        popup.open()

    def view_transactions(self, instance):
        """Navigate to the transactions screen."""
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current = 'transactions'

    def view_documents(self, instance):
        """Navigate to the documents screen."""
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current = 'documents'

    def update_stats(self, balance, income, expense, doc_count):
        """Update the statistics cards with new values."""
        self.balance_card.value = f'₹{balance:.2f}'
        self.income_card.value = f'₹{income:.2f}'
        self.expense_card.value = f'₹{expense:.2f}'
        self.doc_card.value = str(doc_count)

    def add_transaction_item(self, trans_id, category, amount, description, date, trans_type):
        """Add a transaction item to the recent transactions list."""
        self.trans_list.add_widget(TransactionItem(
            trans_id=trans_id,
            category=category,
            amount=amount,
            description=description,
            date=date,
            trans_type=trans_type
        ))

class TransactionScreen(Screen):
    """Screen for managing transactions."""
    def __init__(self, **kwargs):
        super(TransactionScreen, self).__init__(**kwargs)
        self.name = 'transactions'

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Header
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        back_btn = Button(text='Back', size_hint=(None, None), size=(dp(60), dp(40)))
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        header.add_widget(Label(text='Transactions', font_size='24sp', bold=True, color=(0.2, 0.6, 0.8, 1)))
        layout.add_widget(header)

        # Transaction list
        self.trans_list = BoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, 0.8))
        self.trans_list.bind(minimum_height=self.trans_list.setter('height'))
        self.trans_scroll = ScrollView(size_hint=(1, 1))
        self.trans_scroll.add_widget(self.trans_list)
        layout.add_widget(self.trans_scroll)

        # Add transaction button
        add_trans_btn = Button(text='Add Transaction', background_color=(0.2, 0.6, 0.8, 1),
                              size_hint=(1, 0.1), font_size='18sp')
        add_trans_btn.bind(on_press=self.add_transaction)
        layout.add_widget(add_trans_btn)

        self.add_widget(layout)

    def go_back(self, instance):
        """Return to the main screen."""
        self.parent.transition = SlideTransition(direction='right')
        self.parent.current = 'main'

    def add_transaction(self, instance):
        """Navigate to the add transaction screen."""
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current = 'add_transaction'

    def add_transaction_item(self, trans_id, category, amount, description, date, trans_type):
        """Add a transaction item to the list."""
        self.trans_list.add_widget(TransactionItem(
            trans_id=trans_id,
            category=category,
            amount=amount,
            description=description,
            date=date,
            trans_type=trans_type
        ))

class AddTransactionScreen(Screen):
    """Screen for adding new transactions."""
    def __init__(self, **kwargs):
        super(AddTransactionScreen, self).__init__(**kwargs)
        self.name = 'add_transaction'

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Header
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        back_btn = Button(text='Back', size_hint=(None, None), size=(dp(60), dp(40)))
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        header.add_widget(Label(text='Add Transaction', font_size='24sp', bold=True, color=(0.2, 0.6, 0.8, 1)))
        layout.add_widget(header)

        # Form
        form_layout = GridLayout(cols=1, spacing=dp(10), size_hint=(1, 0.8))

        self.trans_type = Spinner(values=['Income', 'Expense'], size_hint=(1, None), height=dp(50))
        self.category = TextInput(hint_text='Category', size_hint=(1, None), height=dp(50))
        self.amount = TextInput(hint_text='Amount', input_type='number', size_hint=(1, None), height=dp(50))
        self.description = TextInput(hint_text='Description', size_hint=(1, None), height=dp(50))
        self.date = TextInput(hint_text='Date (YYYY-MM-DD)', size_hint=(1, None), height=dp(50))

        form_layout.add_widget(Label(text='Transaction Type', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.trans_type)

        form_layout.add_widget(Label(text='Category', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.category)

        form_layout.add_widget(Label(text='Amount', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.amount)

        form_layout.add_widget(Label(text='Description', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.description)

        form_layout.add_widget(Label(text='Date', font_size='16sp', color=(0.5, 0.5, 0.5, 1),
                                    size_hint=(1, None), height=dp(30), halign='left'))
        form_layout.add_widget(self.date)

        layout.add_widget(form_layout)

        # Submit button
        submit_btn = Button(text='Add Transaction', background_color=(0.2, 0.6, 0.8, 1),
                           size_hint=(1, 0.1), font_size='18sp')
        submit_btn.bind(on_press=self.submit_transaction)
        layout.add_widget(submit_btn)

        self.add_widget(layout)

    def go_back(self, instance):
        """Return to the transactions screen."""
        self.parent.transition = SlideTransition(direction='right')
        self.parent.current = 'transactions'

    def submit_transaction(self, instance):
        """Handle the submission of a new transaction."""
        trans_type = self.trans_type.text
        category = self.category.text
        amount = self.amount.text
        description = self.description.text
        date = self.date.text

        if not all([trans_type, category, amount, description, date]):
            self.show_error_popup('Please fill all fields')
            return

        try:
            amount = float(amount)
        except ValueError:
            self.show_error_popup('Please enter a valid amount')
            return

        # Validate date format
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            self.show_error_popup('Please enter a valid date in YYYY-MM-DD format')
            return

        app = App.get_running_app()
        app.add_transaction(trans_type, category, amount, description, date)

        self.show_success_popup('Transaction added successfully')
        self.go_back(instance)

    def show_error_popup(self, message):
        """Display an error popup with the given message."""
        popup = Popup(title='Error', size_hint=(0.8, 0.3))
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        layout.add_widget(Label(text=message, font_size='16sp'))

        close_btn = Button(text='OK', size_hint=(None, None), size=(dp(100), dp(40)))
        close_btn.bind(on_press=popup.dismiss)

        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        btn_layout.add_widget(Widget())  # Spacer
        btn_layout.add_widget(close_btn)
        btn_layout.add_widget(Widget())  # Spacer

        layout.add_widget(btn_layout)
        popup.content = layout
        popup.open()

    def show_success_popup(self, message):
        """Display a success popup with the given message."""
        popup = Popup(title='Success', size_hint=(0.8, 0.3))
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        layout.add_widget(Label(text=message, font_size='16sp'))

        close_btn = Button(text='OK', size_hint=(None, None), size=(dp(100), dp(40)))
        close_btn.bind(on_press=popup.dismiss)

        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        btn_layout.add_widget(Widget())  # Spacer
        btn_layout.add_widget(close_btn)
        btn_layout.add_widget(Widget())  # Spacer

        layout.add_widget(btn_layout)
        popup.content = layout
        popup.open()

class FinDocApp(App):
    """Main application class."""
    current_user = StringProperty('')

    def build(self):
        """Build the application."""
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen())
        self.sm.add_widget(RegisterScreen())
        self.sm.add_widget(MainScreen())
        self.sm.add_widget(TransactionScreen())
        self.sm.add_widget(AddTransactionScreen())
        return self.sm

    def register_user(self, username, email, password):
        """Register a new user."""
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save user data
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password.decode('utf-8')
        }

        # Save to JSON store
        store = JsonStore('users.json')
        store.put(username, **user_data)

    def load_user_data(self, username):
        """Load user data."""
        store = JsonStore('users.json')
        user_data = store.get(username)
        return user_data

    def add_transaction(self, trans_type, category, amount, description, date):
        """Add a new transaction."""
        # Save transaction data
        transaction_data = {
            'trans_type': trans_type,
            'category': category,
            'amount': amount,
            'description': description,
            'date': date
        }

        # Save to JSON store
        store = JsonStore(f'transactions_{self.current_user}.json')
        store.put(str(int(time.time())), **transaction_data)

    def view_document(self, doc_id):
        """View a document."""
        # Implement document viewing logic
        pass

    def confirm_delete_document(self, doc_id, doc_name):
        """Confirm deletion of a document."""
        # Implement document deletion logic
        pass

def load_user_data(username):
    """Load user data from JSON store."""
    store = JsonStore('users.json')
    return store.get(username)

def check_password(hashed_password, user_password):
    """Check if the provided password matches the hashed password."""
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

if __name__ == '__main__':
    FinDocApp().run()




