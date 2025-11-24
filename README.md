# GitHub Organization Wrapped Generator

## Overview

A GitHub Org Data Analyzer is a tool designed to analyze GitHub activity data. It provides insights into various metrics such as total active days, longest gaps, busiest days, longest streaks, month-wise activity, time-wise activity, developer activity, and repository activity based on logs of GitHub activity.

## Features

- **Total Active Days**: Calculate the total number of active days.
- **Longest Gap**: Identify the longest gap between activities.
- **Busiest Day**: Find the day with the highest number of activities.
- **Longest Streak**: Determine the longest streak of consecutive active days.
- **Month-wise Activity**: Visualize activity on a monthly basis.
- **Time-wise Activity**: Visualize activity based on the time of day.
- **Developer Activity**: Analyze the activity of individual developers.
- **Repository Activity**: Analyze the activity of repositories.
- **Organization-Agnostic**: Works with any GitHub organization
- **Yearly Recap**: Generate organization-specific yearly summaries
- **Customizable Branding**: Configure colors, names, and descriptions
- **Comprehensive Analytics**: 
  - Activity heatmaps
  - Repository performance
  - Contributor statistics
  - Commit frequency analysis
  - And much more!

## Setup

### Prerequisites
- Get logs of your organization's using webhook created on discord through github
- use extension like Discrub to download the logs in csv format
- Setup virtual environment
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/dk-a-dev/github-org-wrapped-gen.git
    cd github-org-wrapped-gen
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure Your Organization

    Edit `config.py` to add your organization:

    ```python
    ORGANIZATIONS = {
        "YOUR_ORG": {
            "name": "Your Organization",
            "full_name": "Your Organization Full Name",
            "description": "Organization description",
            "color_primary": "#667eea",
            "color_secondary": "#764ba2",
            "year": 2025,
        },
    }
    ```

4. Prepare Data

    Export your GitHub organization's event data as CSV with columns:
    - `timestamp`: Event timestamp
    - `embeds.0.title`: Event title
    - `embeds.0.author.name`: Author name
    - `embeds.0.author.url`: Author URL

    Place the CSV file as `clean_data.csv` in the project root, or upload it through the UI.

### Warning: clean the data before uploading it to the application

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run core/ui.py
    ```
2. Open your web browser and navigate to the URL provided by Streamlit.
3. Upload a CSV file containing GitHub activity data.
4. The application will display various metrics and visualizations based on the uploaded data.

## Configuration

### Available Configuration Options

```python
{
    "name": "Organization short name",
    "full_name": "Full organization name",
    "description": "Organization description",
    "color_primary": "#HEX_COLOR",
    "color_secondary": "#HEX_COLOR",
    "year": 2025,
}
```

### Multi-Organization Support

The dashboard supports multiple organizations:
1. Add organization configs to `config.py`
2. Select organization from sidebar dropdown in the UI
3. Upload corresponding CSV data
4. View organization-specific yearly recap

## File Structure

- `core/main.py`: Contains the core functions for data analysis.
- `core/ui.py`: Contains the Streamlit UI code.
- `config.yaml`: Configuration file for authentication.
- `README.md`: Project documentation.

## Example
https://gdsc-wrapped-2024.streamlit.app/
(Required organization logs to be uploaded, with data access perms)

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact
For any questions or feedback, please contact [Dev Keshwani](mailto:dev.keshwani345@gmail.com).

## Customization

### Add Banner

Place `banner.jpeg` in project root (displayed at top of dashboard)

### Modify Metrics

Edit `core/main.py` to add custom analysis functions

### Styling

Update CSS in `core/ui.py` to match organization branding

## Output

The dashboard provides:
- 📊 Key metrics overview
- 🔥 GitHub-style activity heatmap
- 📅 Monthly activity trends
- ⏰ Hourly activity distribution
- 👥 Top contributors list
- 🏆 Repository performance
- 📂 Detailed repository statistics
- 📥 CSV export functionality
