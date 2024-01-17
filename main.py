from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Static, Header, Footer, Placeholder, Tabs, Button


airdrops = ["Jupiter", "Taiko", "Nitrogen"]


class DashboardScreen(Screen):
    CSS_PATH = "dashboard.tcss"
    
    def compose(self) -> ComposeResult:
        
        yield Header("Dashboard")
        self.title = "Portfolio Application"
        
        with Container(id="dashboard"):
            with Horizontal(id="main"):
                with VerticalScroll(id="status"):
                    yield Static("Status")
                    for i in range(50):
                        yield Static(f"Airdrop {i}: Farming")
                with Horizontal(id="tasks"):
                    for i in range(3):
                        yield Button(f"{airdrops[i]}", id=f"button{i}")    
                
            with VerticalScroll(id="wallets"):
                yield Static("Wallets Database")
                
                    
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