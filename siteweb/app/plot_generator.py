import os
from bokeh.io import save
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.plotting import figure
from bokeh.resources import Resources
import pandas as pd
import numpy as np
from math import pi  # Import pi for the rotation


def generate_marque_plot(csv_file):
    # Read the CSV file using pandas
    data = csv_file

    # Convert the 'Price' column to numeric
    data['Price'] = pd.to_numeric(data['Price'])

    # Group data by 'Name' and calculate the average 'Price'
    grouped_data = data.groupby('Name')['Price'].mean().reset_index()

    # Generate random colors for each bar and convert to hexadecimal
    random_colors = ['#' + ''.join([f"{int(c):02x}" for c in np.random.randint(0, 255, 3)]) for _ in range(len(grouped_data))]
    grouped_data['colors'] = random_colors  # Add colors as a new column

    source = ColumnDataSource(data=grouped_data)

    plot = figure(title='Moyen Prix par Marque',
                x_axis_label='Marque',
                y_axis_label='Prix Moyen',
                x_range=grouped_data['Name'])

    plot.vbar(x='Name', top='Price', width=0.8, source=source,
            fill_color='colors')

    # Rotate x-axis labels to vertical
    plot.xaxis.major_label_orientation = pi/2

    # Use NumeralTickFormatter to avoid scientific notation
    plot.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

    # Save the plot as an standalone HTML file
    plot_dir = 'app/templates'
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    plot_path = os.path.join(plot_dir, 'nameXprice_plot.html')
    resources = Resources()
    save(plot, filename=plot_path, title='Average Price by Name', resources=resources)

def generate_anne_plot(csv_file):
    # Read the CSV file using pandas
    data = csv_file

    # Ensure 'Year' is treated as a categorical value for plotting purposes
    data['Year'] = data['Year'].astype(str)

    # Convert the 'Price' column to numeric
    data['Price'] = pd.to_numeric(data['Price'])

    # Group data by 'Year' and calculate the average 'Price'
    grouped_data = data.groupby('Year')['Price'].mean().reset_index()

    # Generate random colors for each bar and convert to hexadecimal
    random_colors = ['#' + ''.join([f"{int(c):02x}" for c in np.random.randint(0, 255, 3)]) for _ in range(len(grouped_data))]
    grouped_data['colors'] = random_colors  # Add colors as a new column

    source = ColumnDataSource(data=grouped_data)

    plot = figure(title='Average Price by Year',
                  x_axis_label='Year',
                  y_axis_label='Average Price',
                  x_range=grouped_data['Year'])

    plot.vbar(x='Year', top='Price', width=0.8, source=source,
              fill_color='colors')

    # Rotate x-axis labels to vertical
    plot.xaxis.major_label_orientation = pi/2

    # Use NumeralTickFormatter to avoid scientific notation for both axes
    plot.xaxis.formatter = NumeralTickFormatter(format="0,0")  # Format for 'Year'
    plot.yaxis.formatter = NumeralTickFormatter(format="0,0")  # Format for 'Price'

    # Save the plot as an standalone HTML file
    plot_dir = 'app/templates'
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    plot_path = os.path.join(plot_dir, 'anneXprice_plot.html')
    resources = Resources()
    save(plot, filename=plot_path, title='Average Price by Year', resources=resources)


def generate_carburant_plot(csv_file):
      # Read the CSV file using pandas
    data = csv_file

    # Ensure 'Fuel_Type' is treated as a categorical value for plotting purposes
    data['Fuel_Type'] = data['Fuel_Type'].astype(str)

    # Convert the 'Price' column to numeric
    data['Price'] = pd.to_numeric(data['Price'])

    # Group data by 'Fuel_Type' and calculate the average 'Price'
    grouped_data = data.groupby('Fuel_Type')['Price'].mean().reset_index()

    # Generate random colors for each bar and convert to hexadecimal
    random_colors = ['#' + ''.join([f"{int(c):02x}" for c in np.random.randint(0, 255, 3)]) for _ in range(len(grouped_data))]
    grouped_data['colors'] = random_colors  # Add colors as a new column

    source = ColumnDataSource(data=grouped_data)

    plot = figure(title='Average Price by Fuel Type',
                x_axis_label='Fuel Type',
                y_axis_label='Average Price',
                x_range=grouped_data['Fuel_Type'])

    plot.vbar(x='Fuel_Type', top='Price', width=0.8, source=source,
            fill_color='colors')

    # Rotate x-axis labels to vertical
    plot.xaxis.major_label_orientation = pi/2

    # Removed the inappropriate formatter for the categorical x-axis
    # plot.xaxis.formatter = NumeralTickFormatter(format="0,0")  # This line is not needed for categorical x-axis

    # Use NumeralTickFormatter to avoid scientific notation for y-axis
    plot.yaxis.formatter = NumeralTickFormatter(format="0,0")  # Format for 'Price'

    # Save the plot as an standalone HTML file
    plot_dir = 'app/templates'
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    plot_path = os.path.join(plot_dir, 'fuelXprice_plot.html')
    resources = Resources()
    save(plot, filename=plot_path, title='Average Price by Fuel Type', resources=resources)

def generate_marque2_plot(csv_file):
    # Read the CSV file using pandas
    data = csv_file
    
    # Assume 'Anne' column already in the correct format, no need to convert to numeric

    # Group data by 'Name' and count the number of occurrences for each 'Name'
    grouped_data = data.groupby('Name').size().reset_index(name='Count')

    # Generate random colors for each bar and convert to hexadecimal
    random_colors = ['#' + ''.join([f"{int(c):02x}" for c in np.random.randint(0, 255, 3)]) for _ in range(len(grouped_data))]
    grouped_data['colors'] = random_colors  # Add colors as a new column

    source = ColumnDataSource(data=grouped_data)

    plot = figure(title='Nombre d\'entrées par Marque',
                x_axis_label='Marque',
                y_axis_label='Nombre d\'entrées',
                x_range=grouped_data['Name'])

    plot.vbar(x='Name', top='Count', width=0.8, source=source,
            fill_color='colors')

    # Rotate x-axis labels to vertical
    plot.xaxis.major_label_orientation = pi/2

    # Assuming 'Count' might not need NumeralTickFormatter as it's likely not to be in scientific notation
    # But if you do want to ensure it's formatted as integers:
    plot.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

    # Save the plot as an standalone HTML file
    plot_dir = 'app/templates'
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    plot_path = os.path.join(plot_dir, 'nameXanne_plot.html')
    resources = Resources()
    save(plot, filename=plot_path, title='Nombre d\'entrées par Marque', resources=resources)

def generate_carburant2_plot(csv_file):
    # Assuming csv_file_path is a path to the CSV file, correct the parameter usage
    data = csv_file

    # Ensure 'Fuel_Type' is treated as a categorical value for plotting purposes
    data['Fuel_Type'] = data['Fuel_Type'].astype(str)

    # Group data by 'Fuel_Type' and count the occurrences
    grouped_data = data.groupby('Fuel_Type').size().reset_index(name='Count')

    # Generate random colors for each bar and convert to hexadecimal
    random_colors = ['#' + ''.join([f"{int(c):02x}" for c in np.random.randint(0, 255, 3)]) for _ in range(len(grouped_data))]
    grouped_data['colors'] = random_colors  # Add colors as a new column

    source = ColumnDataSource(data=grouped_data)

    plot = figure(title='Number of Vehicles by Fuel Type',
                  x_axis_label='Fuel Type',
                  y_axis_label='Number of Vehicles',
                  x_range=grouped_data['Fuel_Type'])

    plot.vbar(x='Fuel_Type', top='Count', width=0.8, source=source,
              fill_color='colors')

    # Rotate x-axis labels to vertical
    plot.xaxis.major_label_orientation = pi/2

    # Since we're counting occurrences, NumeralTickFormatter on the y-axis makes sense to ensure no scientific notation
    plot.yaxis.formatter = NumeralTickFormatter(format="0,0")

    # Save the plot as an standalone HTML file
    plot_dir = 'app/templates'
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    plot_path = os.path.join(plot_dir, 'fuelXanne_plot.html')
    resources = Resources()
    save(plot, filename=plot_path, title='Number of Vehicles by Fuel Type', resources=resources)  
    
def init_plot():
    csv_file = 'clean_siteweb_CSV.csv'
    data = pd.read_csv(csv_file)
    
    generate_marque_plot(data)
    generate_anne_plot(data)
    generate_carburant_plot(data)
    generate_marque2_plot(data)
    generate_carburant2_plot(data)

