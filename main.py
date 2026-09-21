from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import threading
import os

try:
    import yt_dlp
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False

class YouTubeDownloaderApp(App):
    def build(self):
        self.title = "YouTube Pro Downloader - Android"
        
        # Main Layout
        layout = BoxLayout(orientation='vertical', padding=25, spacing=15)

        # Header Title
        layout.add_widget(Label(
            text="[b]📥 YOUTUBE PRO DOWNLOADER[/b]",
            markup=True,
            font_size='20sp',
            color=(0.22, 0.74, 0.96, 1),
            size_hint_y=None,
            height=50
        ))

        if not HAS_YTDLP:
            layout.add_widget(Label(
                text="⚠️ Warning: yt-dlp library not found in build environment!",
                color=(0.93, 0.26, 0.26, 1),
                size_hint_y=None,
                height=40
            ))

        # URL Input
        layout.add_widget(Label(text="Paste YouTube Video URL:", font_size='14sp', color=(1, 1, 1, 1), size_hint_y=None, height=30))
        
        self.url_input = TextInput(
            text='',
            hint_text='https://www.youtube.com/watch?v=...',
            multiline=False,
            size_hint_y=None,
            height=45,
            background_color=(0.11, 0.16, 0.25, 1),
            foreground_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.url_input)

        # Download Button
        self.download_btn = Button(
            text="START DOWNLOAD 🚀",
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=55,
            background_color=(0.14, 0.38, 0.92, 1)
        )
        self.download_btn.bind(on_press=self.start_download)
        layout.add_widget(self.download_btn)

        # Status Label
        self.status_label = Label(
            text="Status: Ready",
            font_size='14sp',
            color=(0.13, 0.77, 0.36, 1),
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.status_label)

        # Footer Branding (Strictly Maintained)
        layout.add_widget(Label(
            text="Created by Chishti Bro Computer & Developers\nFounder: Moinuddin Chishti",
            font_size='11sp',
            italic=True,
            color=(0.58, 0.63, 0.72, 1),
            size_hint_y=None,
            height=50
        ))

        return layout

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "Error: Please enter a valid URL!"
            self.status_label.color = (0.93, 0.26, 0.26, 1)
            return

        self.download_btn.disabled = True
        self.status_label.text = "Status: Downloading..."
        self.status_label.color = (0.98, 0.74, 0.14, 1)

        threading.Thread(target=self.download_thread, args=(url,), daemon=True).start()

    def download_thread(self, url):
        try:
            # Save to standard Android download path or app storage
            save_path = "/storage/emulated/0/Download"
            if not os.path.exists(save_path):
                save_path = os.getcwd()

            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'format': 'best'
            }
            
            if HAS_YTDLP:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                Clock.schedule_once(lambda dt: self.update_ui(True, "Download Completed Successfully! 🎉"))
            else:
                Clock.schedule_once(lambda dt: self.update_ui(False, "Error: yt-dlp missing"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_ui(False, f"Error: {str(e)}"))

    def update_ui(self, success, message):
        self.download_btn.disabled = False
        self.status_label.text = message
        self.status_label.color = (0.13, 0.77, 0.36, 1) if success else (0.93, 0.26, 0.26, 1)

if __name__ == '__main__':
    YouTubeDownloaderApp().run()
      
