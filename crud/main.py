
import os
from supabase import create_client, Client
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv


# --- CONFIGURATION ---
# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize Supabase and Rich Console
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
console = Console()

# --- SCHEMA DEFINITION ---
# This dictionary maps tables to their editable columns for the CLI
TABLE_SCHEMAS = {
    "estructuras": ["nombre", "tipo", "ubicacion", "fecha_construccion", "vida_util_estimada", "estado_actual"],
    "inspecciones": ["estructura_id", "fecha", "inspector", "tipo_inspeccion", "observaciones"],
    "evaluaciones": ["inspeccion_id", "nivel_deterioro", "clasificacion_urgencia", "recomendaciones"],
    "sensores": ["estructura_id", "tipo_sensor", "fecha_instalacion", "estado"],
    "lecturas_sensores": ["sensor_id", "fecha", "valor"],
    "mantenimientos": ["estructura_id", "tipo_mantenimiento", "fecha_programada", "fecha_ejecucion", "descripcion", "estado"]
}

class CivilCRUDApp:
    def __init__(self):
        self.current_table = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def select_table(self):
        """Menu to select which table to work on"""
        self.clear_screen()
        console.print("[bold cyan]Civil Engineering DB Manager[/bold cyan]")
        
        tables = list(TABLE_SCHEMAS.keys())
        for idx, name in enumerate(tables):
            console.print(f"{idx + 1}. [green]{name}[/green]")
        
        console.print("0. [red]Exit[/red]")
        
        choice = Prompt.ask("Select a table", choices=[str(i) for i in range(len(tables) + 1)])
        
        if choice == "0":
            exit()
        
        self.current_table = tables[int(choice) - 1]

    def view_data(self):
        """Fetches and displays data using Rich Tables"""
        try:
            response = supabase.table(self.current_table).select("*").execute()
            data = response.data

            if not data:
                console.print(f"[yellow]No records found in {self.current_table}.[/yellow]")
                return

            # Create a dynamic table
            table = Table(title=f"Table: {self.current_table}")
            
            # Get headers from the first record keys
            headers = list(data[0].keys())
            for h in headers:
                table.add_column(h, style="magenta")

            # Add rows
            for row in data:
                # Convert all values to string for display
                table.add_row(*[str(val) for val in row.values()])

            console.print(table)
            return data # Return data for use in other functions
        except Exception as e:
            console.print(f"[bold red]Error fetching data:[/bold red] {e}")

    def create_record(self):
        """Dynamic input form based on schema"""
        console.print(f"\n[bold]Creating new record for: {self.current_table}[/bold]")
        columns = TABLE_SCHEMAS[self.current_table]
        payload = {}

        for col in columns:
            # Add hint for Foreign Keys
            hint = ""
            if "_id" in col:
                hint = " (Copy UUID from parent table)"
            elif "fecha" in col:
                hint = " (YYYY-MM-DD)"
            
            val = Prompt.ask(f"Enter {col}{hint}")
            
            # Basic validation: If empty, don't send it (let DB default handle it or fail)
            if val.strip():
                payload[col] = val

        if Confirm.ask("Save this record?"):
            try:
                supabase.table(self.current_table).insert(payload).execute()
                console.print("[bold green]Success! Record created.[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

    def update_record(self):
        """Update a specific record by ID"""
        self.view_data() # Show data first so user can see IDs
        target_id = Prompt.ask("\n[bold]Enter UUID of the record to update[/bold]")
        
        col_to_edit = Prompt.ask("Which column do you want to edit?", choices=TABLE_SCHEMAS[self.current_table])
        new_value = Prompt.ask(f"Enter new value for {col_to_edit}")

        try:
            supabase.table(self.current_table).update({col_to_edit: new_value}).eq("id", target_id).execute()
            console.print("[bold green]Record updated successfully.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Update failed:[/bold red] {e}")

    def delete_record(self):
        """Delete a record by ID"""
        self.view_data()
        target_id = Prompt.ask("\n[bold red]Enter UUID of the record to DELETE[/bold red]")

        if Confirm.ask(f"Are you sure you want to delete {target_id}? This cannot be undone."):
            try:
                supabase.table(self.current_table).delete().eq("id", target_id).execute()
                console.print("[bold green]Record deleted.[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Delete failed:[/bold red] {e}")

    def run(self):
        while True:
            self.select_table()
            while True:
                console.print(f"\nManaging: [bold cyan]{self.current_table}[/bold cyan]")
                console.print("[1] View All  [2] Create New  [3] Update  [4] Delete  [0] Back to Menu")
                
                action = Prompt.ask("Choose action", choices=["1", "2", "3", "4", "0"])

                if action == "1":
                    self.view_data()
                elif action == "2":
                    self.create_record()
                elif action == "3":
                    self.update_record()
                elif action == "4":
                    self.delete_record()
                elif action == "0":
                    break
                
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = CivilCRUDApp()
    app.run()