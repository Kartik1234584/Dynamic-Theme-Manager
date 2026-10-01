from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QScrollArea, QFileDialog, 
                             QLabel, QMessageBox, QMenu, QLineEdit, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QPixmap
from core.thumbnail_manager import ThumbnailGeneratorThread
from ui.fullscreen_preview import FullscreenPreview
from ui.components.flow_layout import FlowLayout
from ui.components.wallpaper_card import WallpaperCard
import os

class WallpapersTab(QWidget):
    def __init__(self, app_core):
        super().__init__()
        self.core = app_core
        self.setAcceptDrops(True)
        self.threads = [] 
        self.cards = {} # Mapping db_id to WallpaperCard
        self.setup_ui()
        self.load_wallpapers()
        
    def setup_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Left side: Grid
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0,0,0,0)
        
        header = QLabel("Manage Wallpapers")
        header.setObjectName("title")
        left_layout.addWidget(header)
        
        subtitle = QLabel("Drag and drop folders anywhere here to import original wallpapers.")
        subtitle.setObjectName("subtitle")
        left_layout.addWidget(subtitle)
        
        # Tools row: Search and Add Folder
        tools_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search wallpapers...")
        self.search_bar.textChanged.connect(self.filter_wallpapers)
        
        add_btn = QPushButton("Add Folder")
        add_btn.setObjectName("primary")
        add_btn.clicked.connect(self.add_folder)
        
        tools_layout.addWidget(self.search_bar)
        tools_layout.addWidget(add_btn)
        
        left_layout.addLayout(tools_layout)
        
        # Responsive Grid Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet("background-color: transparent;")
        self.grid_layout = FlowLayout(self.grid_widget, margin=0, hSpacing=20, vSpacing=20)
        
        self.scroll.setWidget(self.grid_widget)
        left_layout.addWidget(self.scroll)
        
        # Right side: Details Panel
        self.details_panel = QFrame()
        self.details_panel.setFixedWidth(280)
        self.details_panel.setStyleSheet("QFrame { background-color: rgba(30, 41, 59, 0.5); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); }")
        d_layout = QVBoxLayout(self.details_panel)
        d_layout.setContentsMargins(20, 20, 20, 20)
        
        d_title = QLabel("Wallpaper Details")
        d_title.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        
        self.d_preview = QLabel()
        self.d_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.d_preview.setFixedSize(240, 160)
        self.d_preview.setStyleSheet("background-color: #0f172a; border-radius: 8px;")
        
        self.d_info = QLabel("Select a wallpaper to view details.")
        self.d_info.setWordWrap(True)
        self.d_info.setStyleSheet("color: #94a3b8; font-size: 13px; line-height: 1.5;")
        
        self.d_btn_set = QPushButton("Set as Wallpaper")
        self.d_btn_set.setObjectName("primary")
        self.d_btn_set.clicked.connect(self.set_active_from_details)
        self.d_btn_set.setVisible(False)
        
        self.d_btn_full = QPushButton("Fullscreen Preview")
        self.d_btn_full.clicked.connect(self.show_fullscreen_from_details)
        self.d_btn_full.setVisible(False)

        self.d_btn_fav = QPushButton("☆ Favorite")
        self.d_btn_fav.clicked.connect(self.toggle_favorite_from_details)
        self.d_btn_fav.setVisible(False)
        
        d_layout.addWidget(d_title)
        d_layout.addWidget(self.d_preview)
        d_layout.addWidget(self.d_info)
        d_layout.addStretch()
        d_layout.addWidget(self.d_btn_full)
        d_layout.addWidget(self.d_btn_fav)
        d_layout.addWidget(self.d_btn_set)
        
        main_layout.addWidget(left_widget, stretch=3)
        main_layout.addWidget(self.details_panel)
        
        self.setLayout(main_layout)
        
    def load_wallpapers(self):
        # Clear layout
        for i in reversed(range(self.grid_layout.count())): 
            w = self.grid_layout.itemAt(i).widget()
            if w: w.setParent(None)
            
        self.threads.clear()
        self.cards.clear()
        wallpapers = self.core.db.get_all_wallpapers()
        
        for w in wallpapers:
            path = w['path']
            db_id = w['id']
            if os.path.exists(path):
                card = WallpaperCard(db_id, path)
                card.clicked.connect(self.on_item_selected)
                card.doubleClicked.connect(self.show_fullscreen)
                
                # Setup context menu on card
                card.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                card.customContextMenuRequested.connect(lambda pos, c=card: self.show_context_menu(c, pos))
                
                self.grid_layout.addWidget(card)
                self.cards[db_id] = card
                
                # Start thread to generate thumbnail
                thread = ThumbnailGeneratorThread(path, db_id)
                thread.finished.connect(self.on_thumbnail_ready)
                self.threads.append(thread)
                thread.start()
                
    def on_thumbnail_ready(self, original_path, thumb_path, db_id):
        if db_id in self.cards:
            self.cards[db_id].set_thumbnail(thumb_path)
                
    def on_item_selected(self, path):
        if not path or not os.path.exists(path):
            self.d_info.setText("Select a wallpaper to view details.")
            self.d_preview.clear()
            self.d_btn_set.setVisible(False)
            self.d_btn_full.setVisible(False)
            self.d_btn_fav.setVisible(False)
            return
            
        self.current_selected_path = path
        
        # Update Details Panel
        size_mb = os.path.getsize(path) / (1024 * 1024)
        ext = os.path.splitext(path)[1].upper()[1:]
        
        # Find thumbnail path
        import hashlib
        thumb_hash = hashlib.md5(path.encode('utf-8')).hexdigest()
        thumb_path = os.path.join("cache", "thumbnails", f"{thumb_hash}.jpg")
        
        from PIL import Image
        try:
            with Image.open(path) as img:
                res = f"{img.width} x {img.height}"
        except:
            res = "Unknown"
            
        details_text = (
            f"<b>File:</b> {os.path.basename(path)}<br><br>"
            f"<b>Resolution:</b> {res}<br>"
            f"<b>Format:</b> {ext}<br>"
            f"<b>Size:</b> {size_mb:.2f} MB<br>"
        )
        self.d_info.setText(details_text)
        self.d_btn_set.setVisible(True)
        self.d_btn_full.setVisible(True)
        self.d_btn_fav.setVisible(True)
        
        if self.core.db.is_favorite(path):
            self.d_btn_fav.setText("★ Unfavorite")
        else:
            self.d_btn_fav.setText("☆ Favorite")
        
        # Set preview to thumbnail icon
        if os.path.exists(thumb_path):
            pixmap = QPixmap(thumb_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(240, 160, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                self.d_preview.setPixmap(pixmap)
            
    def set_active_from_details(self):
        if hasattr(self, 'current_selected_path'):
            success = self.core.wallpaper_manager.set_specific_wallpaper(self.current_selected_path)
            if success:
                self.d_btn_set.setText("Applied \u2713")
                self.d_btn_set.setStyleSheet("background-color: #10b981; color: white;")
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(2000, self.reset_set_btn)
                
    def reset_set_btn(self):
        self.d_btn_set.setText("Set as Wallpaper")
        self.d_btn_set.setStyleSheet("")
            
    def show_fullscreen_from_details(self):
        if hasattr(self, 'current_selected_path'):
            self.fs_window = FullscreenPreview(self.current_selected_path, self.core)
            self.fs_window.showFullScreen()
            
    def toggle_favorite_from_details(self):
        if hasattr(self, 'current_selected_path'):
            path = self.current_selected_path
            is_fav = self.core.db.is_favorite(path)
            if is_fav:
                self.core.db.remove_favorite(path)
                self.d_btn_fav.setText("☆ Favorite")
            else:
                self.core.db.add_favorite(path)
                self.d_btn_fav.setText("★ Unfavorite")
            
    def show_fullscreen(self, path):
        self.fs_window = FullscreenPreview(path, self.core)
        self.fs_window.showFullScreen()

    def filter_wallpapers(self, text):
        query = text.lower()
        for db_id, card in self.cards.items():
            card.setHidden(query not in os.path.basename(card.original_path).lower())
                
    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Wallpaper Folder")
        if folder:
            count = self.core.wallpaper_manager.add_folder(folder)
            QMessageBox.information(self, "Success", f"Added {count} wallpapers from folder in original quality.")
            self.load_wallpapers()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        added = 0
        for url in urls:
            path = url.toLocalFile()
            if os.path.isdir(path):
                added += self.core.wallpaper_manager.add_folder(path)
        if added > 0:
            self.load_wallpapers()
            QMessageBox.information(self, "Success", f"Added {added} wallpapers via Drag & Drop.")

    def show_context_menu(self, card, position):
        menu = QMenu()
        
        set_action = QAction("Set as Wallpaper Now", self)
        set_action.triggered.connect(lambda: self.core.wallpaper_manager.set_specific_wallpaper(card.original_path))
        menu.addAction(set_action)
        
        menu.addSeparator()
        
        categories = self.core.db.get_all_categories()
        cat_menu = menu.addMenu("Assign Category")
        for cat in categories:
            action = QAction(cat['name'], self)
            action.setData((card.db_id, cat['id']))
            action.triggered.connect(self.assign_category)
            cat_menu.addAction(action)
            
        menu.exec(card.mapToGlobal(position))
        
    def assign_category(self):
        action = self.sender()
        if action:
            wallpaper_id, category_id = action.data()
            self.core.db.update_wallpaper_category(wallpaper_id, category_id)
            QMessageBox.information(self, "Success", "Category assigned successfully.")
