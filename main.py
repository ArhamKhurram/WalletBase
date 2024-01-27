from textual import on, events
from textual.events import Mount
from textual.reactive import reactive
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal, VerticalScroll, Vertical
from textual.widgets import Static, Header, Footer, DataTable, Collapsible, Input, Label, SelectionList, TabbedContent, TabPane
from rich.text import Text

import json
import pandas
import time
import logging

# Configure logging
logging.basicConfig(filename='main.log', level=logging.DEBUG)


# Load from JSON
with open('airdrops_info.json', 'r') as f:
    airdrops_loaded = json.load(f)
    
# Load from CSV

df = pandas.read_csv("walletDB.csv")
ROWS = df.to_dict(orient="records")

columns = len(df.columns)
rows = len(df.index)

# Chain Data

selection_list = SelectionList[str]( 
    ("Solana", "Solana"),
    ("Ethereum", "Ethereum"),
    ("Ordinals", "Ordinals"),
    ("Nitrogen", "Nitrogen"),
    ("Teiko", "Teiko"),
    ("Berachain", "Berachain"),
    classes="option"
)

# Load DataTable For Wallets 

def _test_dt( self ) -> DataTable:
                    dt = DataTable(id="database")
                    dt.zebra_stripes = True
                    dt.cursor_type   = "cell"
                    dt.fixed_columns = 1
                    dt.add_column( "Index")
                    dt.add_column( "Name")
                    dt.add_column( "Address")
                    dt.add_column( "Private Key")
                    dt.add_column( "Chain")
                    
                    # Add rows and apply styling to each cell
                    for n in range(rows):
                        dt.add_row(
                            Text(str(n+1), style="italic black"),
                            Text(str(df['wallet_name'][n]), style="italic #03AC13"),
                            Text(str(df['address'][n]), style="italic #03AC13"),
                            Text(str(df['privatekey'][n]), style="italic #03AC13"),
                            Text(str(df['network'][n]), style="italic #03AC13")
                        )  
                                               
                    return dt

# Dashboard Screen

class DashboardScreen(Screen):
    CSS_PATH = "dashboard.tcss"

    @on(TabbedContent.TabActivated)
    def on_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        activated_pane = event.pane.id
        logging.debug(f"Tab pane activated: {activated_pane}")

        # Clear existing tasks
        tasks_containers = self.query(VerticalScroll)

        for tasks_container in tasks_containers:
            if tasks_container.id == "tasks":
                logging.debug(f"Found tasks container: {tasks_container}")
                logging.debug(f"Tasks container children:{tasks_container.children}")
                tasks_container.remove_children()
                
                logging.debug(f"Tasks container exists still?: {tasks_container}")
                
                tasks_container.mount(Static(f"{activated_pane} Tasks", id="taskstatic"))


                # Add new tasks dynamically
                for key, airdrop in airdrops_loaded['airdrops'].items():
                    if activated_pane == airdrop['name']:
                        logging.debug(f"Matching airdrop found: {airdrop}")
                        for n, task in enumerate(airdrop['tasks']):
                            collapsible = Collapsible(title=f"Task {n + 1}")
                            collapsible.compose_add_child(Label(task))
                            tasks_container.mount(collapsible)

                # Explicitly trigger a redraw of the screen
                self.refresh()
                break

    def compose(self) -> ComposeResult:
        yield Header("Dashboard")
        self.title = "Portfolio Application"

        with Container(id="dashboard"):
            with Horizontal(id="main"):
                with VerticalScroll(id="tasks"):  
                    yield Static("Tasks", id="taskstatic")
                    

                with Container(id="status"):
                    with TabbedContent(id="tabbed"):
                        for key, airdrop in airdrops_loaded['airdrops'].items():
                            with TabPane(f"{airdrop['name']}", id=f"{airdrop['name']}"):
                                with Horizontal():
                                    with Vertical(classes="left-tab"):
                                        yield Label(f"Name: {airdrop['name']}")
                                        yield Label(f"Address: {airdrop['address']}")
                                    with Container(classes="right-tab"):
                                        yield Label(f"Status: {airdrop['status']}")

            with VerticalScroll(id="wallets"):
                yield _test_dt(self)

        yield Footer()

class WalletsScreen(Screen):
    
    selected_chain = reactive("")
    
    def compose(self) -> ComposeResult:
        with Vertical(id="WalletScreen"):
            with Horizontal(id="Taskbar"):
                yield Label("Total Wallets", classes="test")
                with VerticalScroll(id="Sorting"):
                    with Collapsible(title="Sort By Chain"):
                        yield selection_list

            yield _test_dt(self)

    @on(SelectionList.SelectedChanged)
    async def on_selected_chain_change(self, event: SelectionList.SelectedChanged) -> None:
        selection_list = event.selection_list
        selected_values = selection_list.selected  # Access the selected values directly
        self.selected_chain = selected_values
        datatable = self.query_one(DataTable)
        datatable.clear()
        await self.update_datatable()

    async def update_datatable(self) -> None:
        datatable = self.query_one(DataTable)
        if datatable is None:
            logging.error("DataTable not found.")
            return

        datatable.clear()
        selected_chain = self.selected_chain or ""
        filtered_rows = [row for row in ROWS if row["network"] in selected_chain]
        
        if not filtered_rows:
            logging.warning("No rows found for the selected chain.")
            return

        for n, row_data in enumerate(filtered_rows, start=1):
            logging.debug(f"Adding row {n}: {row_data}")
            datatable.add_row(
                Text(str(n), style="italic black"),
                Text(str(row_data['wallet_name']), style="italic #03AC13"),
                Text(str(row_data['address']), style="italic #03AC13"),
                Text(str(row_data['privatekey']), style="italic #03AC13"),
                Text(str(row_data['network']), style="italic #03AC13"),
            )

        # Explicitly trigger a redraw of the screen
        self.refresh()
        logging.debug("DataTable updated successfully.")
        
class PortfolioApp(App):
    BINDINGS = [
        ("d", "switch_mode('dashboard')", "Dashboard"),  
        ("w", "switch_mode('wallets')", "Wallets"),
    ]
    MODES = {
        "dashboard": DashboardScreen,  
        "wallets": WalletsScreen,
    }

    def on_mount(self) -> None:
        self.switch_mode("dashboard")  
    

if __name__ == "__main__":
    app = PortfolioApp()
    app.run()