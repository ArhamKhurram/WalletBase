from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal, VerticalScroll, Vertical
from textual.widgets import Static, Header, Footer, Placeholder, Tabs, Button
from textual.widgets import Label, TabbedContent, TabPane, DataTable, Collapsible
from textual.widgets import OptionList, SelectionList
from rich.text import Text

import json
import pandas
from datetime import datetime

# Load from JSON
with open('airdrops.json', 'r') as f:
    airdrops_loaded = json.load(f)
    
    
# Load from CSV

df = pandas.read_csv("walletDB.csv")

columns = len(df.columns)
rows = len(df.index)

# Chain Data

selection_list = SelectionList[int](  
    ("Solana", 0, True),
    ("Ethereum", 1),
    ("Ordinals", 2),
    ("Nitrogen", 3),
    ("Teiko", 4),
    classes="option"
)


# Load DataTable For Wallets 

def _test_dt( self ) -> DataTable:
                    dt = DataTable()
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
    
    def compose(self) -> ComposeResult:
        
        yield Header("Dashboard")
        self.title = "Portfolio Application"
        
        with Container(id="dashboard"):
            
            with Horizontal(id="main"):
                
                with VerticalScroll(id="tasks"):  
                    yield Static("Status")
                    for i in range(50):
                        yield Button(f"Airdrop {i}: Farming")
                        
                with Container(id="status"):
                    with TabbedContent(id="tabbed"):
                        for key, airdrop in airdrops_loaded['airdrops'].items():
                            with TabPane(f"{airdrop['name']}"):
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
    def compose(self) -> ComposeResult:
        with Vertical(id="WalletScreen"):
            with Horizontal(id="Taskbar"):
                yield Label("Total Wallets", classes="test")
                with Collapsible(title="Sort By Chain"):
                    yield selection_list
            yield _test_dt(self)
        
        
        
        
        
        
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