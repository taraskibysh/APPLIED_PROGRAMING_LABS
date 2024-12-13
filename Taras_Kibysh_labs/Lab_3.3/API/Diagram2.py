from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, Legend
from bokeh.palettes import Category10, Category20, bokeh
from bokeh.transform import cumsum
import pandas as pd
from .repositories import AggregatetedRepository
import numpy as np
from django.shortcuts import render
from bokeh.embed import components
from bokeh.models import Slider, CustomJS
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.io import output_file, show


class Diagrams:
    def __init__(self, repo):
        self.repo = repo

    def get_filters(self, request, data):
        selected_genders = request.GET.getlist('genders', ['Male Count', 'Female Count'])
        selected_age_groups = request.GET.getlist('age_groups', data['Age Group'].unique().tolist())
        return selected_genders, selected_age_groups

    def first_chart(self, request):
        salary_data = pd.DataFrame(self.repo.get_avarage_salary())
        salary_data['average'] = salary_data['average'].astype('float')
        all_positions = salary_data['position'].tolist()
        averages = salary_data['average'].tolist()


        selected_positions = request.GET.getlist('positions')
        if selected_positions:
            filtered_data = salary_data[salary_data['position'].isin(selected_positions)]
            filtered_positions = filtered_data['position'].tolist()
            filtered_averages = filtered_data['average'].tolist()
        else:
            filtered_positions, filtered_averages = all_positions, averages

        # Map colors dynamically for filtered positions
        colors = Category10[len(filtered_positions)] if len(filtered_positions) <= 10 else Category20[20]

        source = ColumnDataSource(data=dict(position=filtered_positions, average_salary=filtered_averages, color=colors))

        p = figure(x_range=filtered_positions, height=350, title="Average Salary by Position", toolbar_location=None)
        p.vbar(x='position', top='average_salary', width=0.9, source=source, legend_field="position", fill_color='color')

        p.xaxis.axis_label = "Position"
        p.yaxis.axis_label = "Average Salary"
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        p.grid.grid_line_color = None

        return p

    def second_chart(self, request):
        insurance_data = pd.DataFrame(self.repo.capacity_of_insurance_by_year())
        years = insurance_data['year'].tolist()
        insurance_counts = insurance_data['total_count'].tolist()

        source = ColumnDataSource(data=dict(years=years, insurance_counts=insurance_counts))

        p = figure(title="Insurance Count by Year", x_axis_label='Year', y_axis_label='Insurance Count', height=350)
        p.line('years', 'insurance_counts', source=source, line_width=2)
        p.circle('years', 'insurance_counts', size=6, source=source, color="red", legend_label="Insurance Count")
        p.legend.location = "top_left"

        slider = Slider(start=min(years), end=max(years), value=min(years), step=1, title="Year Range")

        def update(attr, old, new):
            selected_year = slider.value
            filtered_data = insurance_data[insurance_data['year'] <= selected_year]
            source.data = dict(
                years=filtered_data['year'].tolist(),
                insurance_counts=filtered_data['total_count'].tolist()
            )

        slider.on_change('value', update)


        return p

    def third_chart(self, request):
        age_data = pd.DataFrame(self.repo.get_age_information())

        if not age_data.empty:
            age_data = age_data.rename(columns={
                'age_group': 'Age Group',
                'male_count': 'Male Count',
                'female_count': 'Female Count'
            })
            age_data = age_data.melt(id_vars=['Age Group'], value_vars=['Male Count', 'Female Count'],
                                     var_name='Gender', value_name='Count')
            age_data['Age and Gender'] = age_data['Age Group'] + ' - ' + age_data['Gender']

        selected_genders, selected_age_groups = self.get_filters(request, age_data)

        filtered_data = age_data[
            (age_data['Gender'].isin(selected_genders)) &
            (age_data['Age Group'].isin(selected_age_groups))
            ]

        counts = filtered_data.groupby('Age and Gender')['Count'].sum().reset_index()
        counts['angle'] = counts['Count'] / counts['Count'].sum() * 2 * np.pi
        num_colors = len(counts)

        # Handle more than 20 colors by repeating the list (if needed)
        colors = [Category10[10][i % 10] for i in range(num_colors)]
        counts['color'] = colors  # Assign colors to the counts DataFrame

        # Debug: Check the 'counts' DataFrame for issues with 'Age and Gender'
        print(counts.head())  # Print the first few rows to ensure correctness

        p = figure(title="Age and Gender Distribution", height=350, toolbar_location=None, tools="hover",
                   tooltips="@Age and Gender: @Count", x_range=(-1, 1))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='Age and Gender', source=counts)

        # Add the center circle
        p.circle(x=0, y=1, radius=0.1, fill_color='white', line_color='white', alpha=0.5)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"

        return p

    from bokeh.palettes import Category10, Category20

    def fourth_chart(self, request):
        # Get status data
        status_data = pd.DataFrame(self.repo.get_status_statistics())

        if not status_data.empty:
            # Rename columns for better readability
            status_data = status_data.rename(columns={
                'status__status': 'Status',
                'count': 'Count'
            })

            # Filter the data based on the selected statuses
            selected_statuses = request.GET.getlist('statuses', status_data['Status'].tolist())
            filtered_data = status_data[status_data['Status'].isin(selected_statuses)]

            if not filtered_data.empty:
                # Group the data by 'Status' and sum the 'Count' for each group
                counts = filtered_data.groupby('Status')['Count'].sum().reset_index()
                counts['angle'] = counts['Count'] / counts['Count'].sum() * 2 * np.pi

                # Determine the number of colors needed and choose an appropriate palette
                num_colors = len(counts)

                # Handle more than 20 colors by repeating the list (if needed)
                colors = [Category10[10][i % 10] for i in range(num_colors)] if num_colors <= 10 else [
                    Category20[20][i % 20] for i in range(num_colors)]
                counts['color'] = colors  # Assign colors to the counts DataFrame

                # Debug: Print the 'counts' DataFrame to ensure correctness
                print(counts.head())  # Print the first few rows

                # Create the Bokeh plot
                p = figure(title="Client Status Distribution", height=350, toolbar_location=None, tools="hover",
                           tooltips="@Status: @Count", x_range=(-1, 1))

                # Create the wedge chart
                p.wedge(x=0, y=1, radius=0.4,
                        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                        line_color="white", fill_color='color', legend_field='Status', source=counts)

                # Add the center circle (for a donut chart effect)
                p.circle(x=0, y=1, radius=0.1, fill_color='white', line_color='white', alpha=0.5)

                # Customize the plot appearance
                p.axis.axis_label = None
                p.axis.visible = False
                p.grid.grid_line_color = None
                p.legend.location = "top_left"
                p.legend.orientation = "horizontal"

                return p
            else:
                print("No filtered data available.")
                return None
        else:
            print("Status data is empty.")
            return None

    def fifth_chart(self, request):
        worker_data = pd.DataFrame(self.repo.served_people_capacity_by_worker())
        worker_data = worker_data.rename(columns={'worker_name': 'Worker Name', 'count': 'People Count'})

        selected_workers = request.GET.getlist('workers', worker_data['Worker Name'].unique().tolist())
        filtered_data = worker_data[worker_data['Worker Name'].isin(selected_workers)]

        # Assign colors as a column in the ColumnDataSource
        colors = Category10[len(filtered_data)] if len(filtered_data) <= 10 else Category20[20]
        filtered_data['color'] = colors[:len(filtered_data)]  # Ensure the color list matches the data length

        source = ColumnDataSource(filtered_data)

        p = figure(x_range=filtered_data['Worker Name'].tolist(), height=350, title="People Served by Workers")
        p.vbar(x='Worker Name', top='People Count', width=0.9, source=source, legend_field="Worker Name", color='color')

        p.xaxis.axis_label = "Worker Name"
        p.yaxis.axis_label = "People Count"
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        p.grid.grid_line_color = None

        return p

    def sixth_chart(self, request):
        # Fetch data from the repository
        price_data = pd.DataFrame(self.repo.get_price_of_item_and_price_of_insurance())
        print(f"Initial price data:\n{price_data}")  # Перевірка початкових даних

        # Rename columns for easier access
        price_data = price_data.rename(columns={
            'price_of_item_insurance': 'Item Insurance Price',
            'item_insurance__item_price': 'Item Price'
        })

        # Перевірка після перейменування стовпців
        print(f"Renamed price data:\n{price_data}")

        # Convert columns to float
        price_data['Item Insurance Price'] = price_data['Item Insurance Price'].astype(float)
        price_data['Item Price'] = price_data['Item Price'].astype(float)

        # Перевірка після конвертації в float
        print(f"Price data after conversion to float:\n{price_data}")

        # Get user-selected filters (if any)
        selected_items = request.GET.getlist('items', price_data['Item Insurance Price'].unique().tolist())
        print(f"Selected items: {selected_items}")  # Перевірка вибраних елементів

        # Filter data based on selected items
        filtered_data = price_data[price_data['Item Insurance Price'].isin(selected_items)]
        print(f"Filtered data:\n{filtered_data}")  # Перевірка після фільтрації

        if filtered_data.empty:
            print("No data available after filtering")  # Перевірка на порожні дані

        # Assign colors to the bars using Category10 palette
        colors = Category10[len(filtered_data)] if len(filtered_data) <= 10 else Category10[20]
        filtered_data['color'] = colors[:len(filtered_data)]  # Ensure the color list matches the data length

        # Create a ColumnDataSource from the filtered data
        source = ColumnDataSource(filtered_data)

        # Set x_range using FactorRange for better categorical handling
        x_range = list(map(str, filtered_data['Item Insurance Price'].unique()))
        print(f"x_range: {x_range}")  # Перевірка діапазону осі X

        # Create the Bokeh plot
        p = figure(x_range=FactorRange(*x_range), height=350, title="Item Insurance vs Item Price")

        # Add bars for Item Price
        p.vbar(x='Item Insurance Price', top='Item Price', width=0.4, source=source,
               legend_field="Item Insurance Price",
               color='color', alpha=0.6)

        # Add bars for Insurance Price (shifted slightly to the right)
        offset = 0.2  # Adjust the offset as needed
        filtered_data['offset_x'] = filtered_data['Item Insurance Price'] + offset

        # Create a new ColumnDataSource with the offset (use the same source here)
        source_with_offset = ColumnDataSource(filtered_data)

        p.vbar(x='offset_x', top='Item Insurance Price', width=0.4, source=source_with_offset,
               legend_field="Item Insurance Price", color='color', alpha=0.6)

        # Customize the axes labels and title
        p.xaxis.axis_label = "Item Insurance Price"
        p.yaxis.axis_label = "Price"
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"

        # Remove grid lines for a cleaner look
        p.grid.grid_line_color = None

        # Ensure the legend correctly matches the data
        p.legend.items = [i for i in p.legend.items if i.renderers[0].glyph is not None]

        # Return the Bokeh plot as HTML (for use with Django)
        script, div = components(p)
        data = {
            'Item Insurance Price': [2000.0, 250.0, 3000.0, 500.0, 1000.0, 400.0],
            'Item Price': [15000.0, 5000.0, 250000.0, 1500.0, 700.0, 5000.0]
        }

        # Creating a DataFrame for easier manipulation
        df = pd.DataFrame(data)

        # Add an 'index' column to use as x-axis values
        df['index'] = df.index

        # Create ColumnDataSource for Bokeh
        source = ColumnDataSource(df)

        # Create the figure
        p1 = figure(title="Item Insurance Price vs Item Price",
                    x_axis_label='Index',
                    y_axis_label='Price',
                    height=400, width=600)

        # Adding bars for Item Insurance Price
        p1.vbar(x='index', top='Item Insurance Price', width=0.4, source=source, color="blue",
                legend_label="Item Insurance Price", bottom=0)

        # Adding bars for Item Price (shifted slightly to avoid overlap by adjusting x values)
        df['offset_x'] = df['index'] + 0.2  # Shift "Item Price" bars by 0.2 along the x-axis

        # Create a new ColumnDataSource with the offset_x
        source_with_offset = ColumnDataSource(df)

        # Add the bars for Item Price
        p1.vbar(x='offset_x', top='Item Price', width=0.4, source=source_with_offset, color="green",
                legend_label="Item Price", bottom=0)

        # Customize the plot for better clarity
        p1.legend.location = "top_left"
        p1.xaxis.axis_label = 'Index'
        p1.yaxis.axis_label = 'Price'
        p1.xgrid.grid_line_color = None
        # Add scatter plot

        return p1


def combined_charts_bokeh(request):
    repo = AggregatetedRepository()
    diagrams = Diagrams(repo)

    # Create all charts with components
    graph_html1, script1 = components(diagrams.first_chart(request))
    graph_html2, script2 = components(diagrams.second_chart(request))
    graph_html3, script3 = components(diagrams.third_chart(request))
    graph_html4, script4 = components(diagrams.fourth_chart(request))
    graph_html5, script5 = components(diagrams.fifth_chart(request))
    graph_html6, script6 = components(diagrams.sixth_chart(request))

    # Assuming `salary_data`, `insurance_data`, etc. are DataFrames

    # Get filters and necessary data
    salary_data = pd.DataFrame(repo.get_avarage_salary())
    all_positions = salary_data['position'].tolist()

    age_data = pd.DataFrame(repo.get_age_information())
    age_groups = age_data['age_group'].tolist()

    selected_positions = request.GET.getlist('positions', all_positions)
    selected_genders = request.GET.getlist('genders', ['Male Count', 'Female Count'])
    selected_age_groups = request.GET.getlist('age_groups', age_groups)

    status_statiscic = pd.DataFrame(repo.get_status_statistics())
    all_status = status_statiscic['status__status'].tolist()
    selected_statuses = request.GET.getlist('statuses', all_status)

    worker_data = pd.DataFrame(repo.served_people_capacity_by_worker())
    all_workers = worker_data['worker_name'].tolist()
    selected_workers = request.GET.getlist('workers', all_workers)

    # Assuming `salary_data`, `insurance_data`, etc. are DataFrames
    salary_data['average'] = salary_data['average'].astype('float')


    return render(request, 'dashboard/v2.html', {
        'bokeh_script1': script1,
        'bokeh_div1': graph_html1,
        'bokeh_script2': script2,
        'bokeh_div2': graph_html2,
        'bokeh_script3': script3,
        'bokeh_div3': graph_html3,
        'bokeh_script4': script4,
        'bokeh_div4': graph_html4,
        'bokeh_script5': script5,
        'bokeh_div5': graph_html5,
        'positions': all_positions,
        'bokeh_div6': graph_html6,
        'bokeh_script6': script6,
        'selected_positions': selected_positions,
        'age_groups': age_groups,
        'genders': ['Male Count', 'Female Count'],
        'selected_genders': selected_genders,
        'selected_age_groups': selected_age_groups,
        'statuses': all_status,
        'selected_statuses': selected_statuses,
        'workers': all_workers,
        'selected_workers': selected_workers
    })


