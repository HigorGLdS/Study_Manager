from PySide6.QtWidgets import (
    QMainWindow, QTableView, QDockWidget,
    QToolBar, QStatusBar, QMenuBar, QLineEdit,
    QWidget, QVBoxLayout, QHeaderView, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from models.material_table_model import MaterialTableModel
from models.material_filter_proxy import MaterialFilterProxy

from ui.widgets.dashboard_widget import DashboardWidget
from ui.widgets.category_donut_chart import CategoryDonutChart
from ui.widgets.category_list_widget import CategoryListWidget

from ui.delegates.progress_delegate import ProgressDelegate
from ui.dialogs.add_material_dialog import AddMaterialDialog
from ui.dialogs.category_dialog import get_new_category

from ui.styles.theme import load_theme
from database.category_dao import CategoryDAO
from database.material_dao import MaterialDAO


class MainWindow(QMainWindow):
    """
    Janela principal do Study Manager.

    Responsabilidades:
    - Orquestrar estado global (categoria selecionada)
    - Conectar UI <-> Proxy <-> Model
    - Garantir que gráficos NÃO modifiquem dados
    """

    def __init__(self):
        super().__init__()

        # ==============================
        # DATA / STATE
        # ==============================
        self.dao = MaterialDAO()
        self.category_dao = CategoryDAO()

        self.all_materials = self.dao.fetch_all()
        self.current_category_id = None

        # trava para evitar loop donut <-> lista
        self._changing_category = False

        # ==============================
        # MODEL / PROXY
        # ==============================
        self.model = MaterialTableModel(self.all_materials)

        self.proxy = MaterialFilterProxy(self)
        self.proxy.setSourceModel(self.model)

        # ==============================
        # WIDGETS
        # ==============================
        self.dashboard = DashboardWidget()

        self.chart_widget = CategoryDonutChart()
        self.chart_widget.update_chart(self.all_materials)
        self.chart_widget.categoryClicked.connect(
            lambda cid: self.apply_category_filter(cid, source="donut")
        )

        # ==============================
        # WINDOW
        # ==============================
        self.setWindowTitle("Study Manager")
        self.setMinimumSize(1200, 700)

        self._create_menu()
        self._create_toolbar()
        self._create_category_dock()
        self._create_table()
        self._create_statusbar()

        # ==============================
        # SIGNALS
        # ==============================
        self.model.dataChanged.connect(self.update_dashboard)
        self.proxy.modelReset.connect(self.update_dashboard)
        self.proxy.rowsInserted.connect(self.update_dashboard)
        self.proxy.rowsRemoved.connect(self.update_dashboard)

        # ==============================
        # INITIAL UI
        # ==============================
        self.update_dashboard()

    # =====================================================
    # MENU
    # =====================================================
    def _create_menu(self):
        menubar = QMenuBar(self)
        view_menu = menubar.addMenu("Visual")

        self.dark_action = QAction("🌙 Dark Mode", self, checkable=True)
        self.dark_action.setChecked(True)
        self.dark_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.dark_action)

        self.focus_action = QAction("🎯 Modo Foco", self, checkable=True)
        self.focus_action.triggered.connect(self.toggle_focus)
        view_menu.addAction(self.focus_action)

        self.setMenuBar(menubar)

    # =====================================================
    # TOOLBAR
    # =====================================================
    def _create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)

        toolbar.addAction("Adicionar", self.open_add_dialog)
        toolbar.addAction("+ Categoria", self.add_category)

        toolbar.addSeparator()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por título...")
        self.search_input.textChanged.connect(self.proxy.set_search_text)
        toolbar.addWidget(self.search_input)

        self.addToolBar(toolbar)

    # =====================================================
    # CATEGORY DOCK
    # =====================================================
    def _create_category_dock(self):
        categories = self.category_dao.fetch_all()
        self.category_widget = CategoryListWidget(categories)

        self.category_widget.itemSelectionChanged.connect(
            self._on_category_list_changed
        )

        self.category_dock = QDockWidget("Categorias", self)
        self.category_dock.setWidget(self.category_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.category_dock)

    # =====================================================
    # TABLE
    # =====================================================
    def _create_table(self):
        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.setItemDelegateForColumn(4, ProgressDelegate(self.table))
        self.table.setSortingEnabled(True)

        header = self.table.horizontalHeader()
        header.setDefaultSectionSize(160)
        header.setMinimumHeight(48)
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Interactive)

        central = QWidget()
        layout = QVBoxLayout(central)

        layout.addWidget(self.dashboard)
        layout.addWidget(self.chart_widget)
        layout.addWidget(self.table)

        self.setCentralWidget(central)

    # =====================================================
    # STATUS BAR
    # =====================================================
    def _create_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    # =====================================================
    # CATEGORY CORE LOGIC (PONTO ÚNICO)
    # =====================================================
    def apply_category_filter(self, category_id, source):
        """
        ÚNICO ponto que altera categoria ativa.
        source: 'donut' | 'list'
        """
        if self._changing_category:
            return

        self._changing_category = True
        self.current_category_id = category_id

        # aplica filtro
        self.proxy.set_category(category_id)

        # sincroniza apenas VISUAL
        if source == "donut":
            self.category_widget.sync_selection(category_id)
        elif source == "list":
            self.chart_widget.highlight_category(category_id)

        self.update_dashboard()
        self._changing_category = False

    def _on_category_list_changed(self):
        item = self.category_widget.currentItem()
        cid = item.data(Qt.UserRole) if item else None
        self.apply_category_filter(cid, source="list")

    # =====================================================
    # DASHBOARD
    # =====================================================
    def update_dashboard(self):
        """
        Atualiza SOMENTE:
        - cards
        - gráfico de barras
        Donut NÃO é recriado aqui.
        """
        filtered = self.proxy.get_filtered_materials()
        self.dashboard.update_stats(filtered)

        # 🔑 donut e barras SEMPRE globais
        self.chart_widget.update_chart(self.all_materials)
        self.dashboard.category_chart.update_chart(self.all_materials)

    # =====================================================
    # ACTIONS
    # =====================================================
    def toggle_theme(self, checked):
        load_theme(QApplication.instance(), "dark" if checked else "light")

    def toggle_focus(self, checked):
        self.category_dock.setVisible(not checked)
        self.dashboard.setVisible(not checked)
        self.chart_widget.setVisible(not checked)

    # =====================================================
    # CRUD
    # =====================================================
    def open_add_dialog(self):
        categories = self.category_dao.fetch_all()
        dialog = AddMaterialDialog(categories, self)

        if dialog.exec():
            material = dialog.get_data()

            # 1️⃣ persiste
            self.dao.insert(material)

            # 2️⃣ fonte da verdade = banco
            self.all_materials = self.dao.fetch_all()

            # 3️⃣ atualiza model
            self.model.beginResetModel()
            self.model._materials = self.all_materials
            self.model.endResetModel()

            # 4️⃣ atualiza UI
            self.update_dashboard()

    def add_category(self):
        name = get_new_category(self)
        if name:
            self.category_dao.insert(name)
            self.category_widget.reload(self.category_dao.fetch_all())