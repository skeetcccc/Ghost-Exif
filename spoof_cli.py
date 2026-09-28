import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image
import piexif

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from rich.prompt import Prompt

console = Console()


BANNER = r"""
  ██████  ██████   ██████  ███████  ███████ ██████  
 ██      ██  ████ ██    ██ ██    ██ ██      ██   ██ 
 ███████ ██ ██ ██ ██    ██ ███████ █████    ██████  
      ██ ████  ██ ██    ██ ██      ██       ██   ██ 
 ███████  ██████   ██████  ██      ███████  ██   ██ 
"""

CAMERAS = [
    ("Canon", "Canon EOS 5D Mark IV"),
    ("Nikon", "Nikon D850"),
    ("Sony", "ILCE-7RM4"),
    ("Apple", "iPhone 15 Pro"),
    ("Google", "Pixel 8 Pro"),
    ("Fujifilm", "X-T5")
]

def generate_random_gps():
    """Generates fake GPS coordinates."""
    lat_deg, lat_min = random.randint(10, 80), random.randint(0, 59)
    lat_sec = int(random.uniform(0, 59) * 100)
    lon_deg, lon_min = random.randint(10, 180), random.randint(0, 59)
    lon_sec = int(random.uniform(0, 59) * 100)

    return {
        piexif.GPSIFD.GPSLatitudeRef: random.choice([b'N', b'S']),
        piexif.GPSIFD.GPSLatitude: ((lat_deg, 1), (lat_min, 1), (lat_sec, 100)),
        piexif.GPSIFD.GPSLongitudeRef: random.choice([b'E', b'W']),
        piexif.GPSIFD.GPSLongitude: ((lon_deg, 1), (lon_min, 1), (lon_sec, 100)),
    }

def spoof_metadata(image_path: Path, output_path: Path):
    """Spoofs EXIF metadata for the given image."""
    make, model = random.choice(CAMERAS)
    random_days = random.randint(10, 1500)
    fake_date = (datetime.now() - timedelta(days=random_days)).strftime("%Y:%m:%d %H:%M:%S").encode('utf-8')

    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: make.encode('utf-8'),
            piexif.ImageIFD.Model: model.encode('utf-8'),
            piexif.ImageIFD.Software: b"Adobe Photoshop 2026",
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: fake_date,
            piexif.ExifIFD.DateTimeDigitized: fake_date,
        },
        "GPS": generate_random_gps()
    }

    exif_bytes = piexif.dump(exif_dict)
    
    with Image.open(image_path) as img:
        img.save(output_path, exif=exif_bytes)

def print_header():
    """Displays ASCII banner and header status."""
    console.clear()
    banner_text = Text(BANNER, style="bold cyan")
    console.print(Panel(banner_text, subtitle="[bold green]Anti-OSINT EXIF Metadata Spoofer v1.0[/bold green]", expand=False))
    console.print("[dim italic]Protecting digital footprint via false metadata injection[/dim italic]\n")

def main():
    print_header()


    raw_input = Prompt.ask("[bold yellow]Enter file or directory path[/bold yellow]")
    

    cleaned_input = raw_input.strip().strip("'\"").strip()
    target_path = Path(cleaned_input).expanduser().resolve()

    if not target_path.exists():
        console.print(f"\n[bold red][-] Error:[/bold red] Path '{target_path}' does not exist.")
        sys.exit(1)

    files_to_process = []
    if target_path.is_file() and target_path.suffix.lower() in ['.jpg', '.jpeg']:
        files_to_process.append(target_path)
    elif target_path.is_dir():
        files_to_process = [p for p in target_path.glob('*') if p.suffix.lower() in ['.jpg', '.jpeg']]

    if not files_to_process:
        console.print("\n[bold red][-] Error:[/bold red] No JPG/JPEG files found.")
        sys.exit(1)

    console.print(f"\n[bold green][+] Found files to process:[/bold green] {len(files_to_process)}\n")

    out_dir = target_path.parent / "spoofed_output" if target_path.is_file() else target_path / "spoofed_output"
    out_dir.mkdir(exist_ok=True)


    for file in track(files_to_process, description="[cyan]Spoofing EXIF data...[/cyan]"):
        out_file = out_dir / f"spoofed_{file.name}"
        try:
            spoof_metadata(file, out_file)
        except Exception as e:
            console.print(f"\n[red]Error processing {file.name}: {e}[/red]")

    console.print("\n[bold green]✔ Done![/bold green] Processed files saved to:")
    console.print(f"[bold cyan]{out_dir}[/bold cyan]\n")

if __name__ == "__main__":
    main()
