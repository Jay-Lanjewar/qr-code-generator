#!/usr/bin/env python3
"""
QR Code Generator CLI Tool

A robust command-line interface for generating QR codes.
Supports custom sizing, colors, error correction levels, and automatic filename generation.

Usage:
    python main.py "https://example.com"
    python main.py "Hello World" -o my_qr.png
    python main.py "Secure Data" -e H -b 20 -f blue -bg yellow
"""

import argparse
import sys
import re
import qrcode
from qrcode.exceptions import DataOverflowError

# Map CLI arguments to qrcode constants
ERROR_CORRECTION_LEVELS = {
    'L': qrcode.constants.ERROR_CORRECT_L,
    'M': qrcode.constants.ERROR_CORRECT_M,
    'Q': qrcode.constants.ERROR_CORRECT_Q,
    'H': qrcode.constants.ERROR_CORRECT_H,
}

def sanitize_filename(text):
    """
    Generate a safe filename from the input text.
    Truncates to 30 chars and removes invalid characters.
    """
    # Remove protocol/www if present for cleaner names
    text = re.sub(r'^https?://(www\.)?', '', text)
    # Replace non-alphanumeric with underscore
    safe_text = re.sub(r'[^a-zA-Z0-9]', '_', text)
    # Collapse multiple underscores
    safe_text = re.sub(r'_+', '_', safe_text).strip('_')
    # Truncate and ensure it's not empty
    name = safe_text[:30] or "qr_code"
    return f"{name}.png"

def generate_qr_code(data, filename, error_correction, box_size, border, fill_color, back_color):
    """
    Generates and saves a QR code image.
    """
    try:
        qr = qrcode.QRCode(
            version=None,  # Let qrcode determine optimal size
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(filename)
        print(f"Success: QR code saved to '{filename}'")

    except DataOverflowError:
        print("Error: The data provided is too long for the selected QR settings.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        # Often raised for invalid colors or invalid types
        print(f"Error: Usage or Value error - {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error: Could not save file to '{filename}'. {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a QR code from text or URL.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "data",
        help="The text or URL to encode."
    )
    parser.add_argument(
        "-o", "--output",
        help="Output filename (optional). Auto-generated if not provided."
    )
    parser.add_argument(
        "-e", "--error-correction",
        choices=['L', 'M', 'Q', 'H'],
        default='M',
        help="Error correction level:\n"
             "  L (7%%)  - Low\n"
             "  M (15%%) - Medium (Default)\n"
             "  Q (25%%) - Quartile\n"
             "  H (30%%) - High"
    )
    parser.add_argument(
        "-b", "--box-size",
        type=int,
        default=10,
        help="Size of each box in pixels (default: 10)."
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="Thickness of the border (boxes) (default: 4)."
    )
    parser.add_argument(
        "-f", "--fill-color",
        default="black",
        help="Fill color (default: black)."
    )
    parser.add_argument(
        "-bg", "--back-color",
        default="white",
        help="Background color (default: white)."
    )

    args = parser.parse_args()

    # Determine filename
    if args.output:
        filename = args.output
    else:
        filename = sanitize_filename(args.data)

    # Get error correction constant
    ec_level = ERROR_CORRECTION_LEVELS[args.error_correction]

    generate_qr_code(
        data=args.data,
        filename=filename,
        error_correction=ec_level,
        box_size=args.box_size,
        border=args.border,
        fill_color=args.fill_color,
        back_color=args.back_color
    )

if __name__ == "__main__":
    main()