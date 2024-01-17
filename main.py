from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal, VerticalScroll, Vertical
from textual.widgets import Static, Header, Footer, Placeholder, Tabs, Button
from textual.widgets import Label, TabbedContent, TabPane, DataTable

import json
import pandas
from datetime import datetime

# Load from JSON
with open('airdrops.json', 'r') as f:
    airdrops_loaded = json.load(f)
    
    
# Load from CSV

df = pandas.read_csv("walletDB.csv")

columns = ["Name", "Address", "Private Key", "Chain"]
rows = len(df.index)

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
                def _test_dt( self ) -> DataTable:
                    dt = DataTable()
                    dt.zebra_stripes = True
                    dt.cursor_type   = "row"
                    dt.fixed_columns = 1
                    dt.add_column( "Index")
                    dt.add_column( "Name")
                    dt.add_column( "Address")
                    dt.add_column( "Private Key")
                    dt.add_column( "Chain")
                    for n in range( rows ):
                        dt.add_row(n, f"{df['wallet_name'][n]}", f"{df['address'][n]}", f"{df['privatekey'][n]}", f"{df['network'][n]}")
                    
                    return dt
                yield _test_dt(self)
                    
        yield Footer()


class WalletsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("Wallets Screen")
        yield Header("Wallets Database")
        yield Footer()
        
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