# Scouts Data Visualization Dashboard

This repository contains a project for the course [PV251 - Visualization](https://is.muni.cz/course/fi/autumn2024/PV251) at FI MUNI (Autumn 2024).

The project is an interactive data visualization dashboard built using Dash and Python. It visualizes Scouts data provided by Junák - český skaut, allowing users to explore trends, compare regions, and analyze age group distributions using interactive controls.

## Features

- **Interactive Line Chart**: Visualize trends over selected years.
- **Year Slider**: Select specific years to filter the data.
- **Dropdowns**: Filter data by region, district, group, and troop.
- **Bar Chart**: Analyze age group distributions.
- **Treemap**: Explore hierarchical data of organizational units.
- **Reset Button**: Reset all filters to their default values.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sarkadol/scouts-data-visualization.git
    cd scouts-data-visualization
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:8050/` to view the dashboard.

## Project Structure

- `app.py`: Main application file.
- `src/`: Source code directory.
    - `callbacks.py`: Contains callback functions for interactivity.
    - `layouts.py`: Defines the layout of the dashboard.
    - `assets/`: Contains static files like CSS and images.
        - `styles.css`: Custom CSS styles for the dashboard.

## Customization

### Styling

To customize the appearance of the dashboard, modify the CSS in `src/assets/styles.css`.

### Adding New Features

To add new features or modify existing ones, update the layout in `src/layouts.py` and the callbacks in `src/callbacks.py`.

## Acknowledgements

- Data provided by [Junák - český skaut](https://opendata.skaut.cz/).
- Created by Šárka Blaško - Pizi for class PV251 Visualization, FI MUNI.
