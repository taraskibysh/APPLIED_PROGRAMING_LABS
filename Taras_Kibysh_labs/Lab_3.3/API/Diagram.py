from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .repositories import AggregatetedRepository


class Diagrams:
    def __init__(self, repo):
        self.repo = repo

    def get_filters(self, request, data):
        selected_genders = request.GET.getlist('genders', ['Male Count', 'Female Count'])
        selected_age_groups = request.GET.getlist('age_groups', data['Age Group'].unique().tolist())
        return selected_genders, selected_age_groups

    def first_chart(self, request):
        # Отримання даних для першої діаграми (середня зарплата)
        salary_data = pd.DataFrame(self.repo.get_avarage_salary())
        all_positions = salary_data['position'].tolist()
        averages = salary_data['average'].tolist()

        # Отримання фільтрів від користувача (якщо є)
        selected_positions = request.GET.getlist('positions')
        if selected_positions:
            filtered_data = salary_data[salary_data['position'].isin(selected_positions)]
            filtered_positions = filtered_data['position'].tolist()
            filtered_averages = filtered_data['average'].tolist()
        else:
            filtered_positions, filtered_averages = all_positions, averages

        # Побудова першої діаграми (середня зарплата)
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=filtered_positions,
            y=filtered_averages,
            name='Середня зарплата',
            marker=dict(color='rgba(55, 128, 191, 0.7)', line=dict(color='rgba(55, 128, 191, 1.0)', width=2))
        ))
        fig1.update_layout(
            title='Середня зарплата за професією',
            xaxis=dict(title='Позиція'),
            yaxis=dict(title='Середня зарплата'),
        )
        return fig1.to_html(full_html=False)

    def second_chart(self, request):
        # Отримання даних для другої діаграми (кількість страхувань)
        insurance_data = pd.DataFrame(self.repo.capacity_of_insurance_by_year())

        # Використання DataFrame для отримання списків
        years = insurance_data['year'].tolist()
        insurance_counts = insurance_data['total_count'].tolist()

        # Побудова другої діаграми (кількість страхувань)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=years,
            y=insurance_counts,
            mode='lines+markers',
            name='Кількість страхувань'
        ))
        fig2.update_layout(
            title='Кількість страхувань за роками',
            xaxis=dict(
                title='Рік',
                rangeslider=dict(visible=True),
                tick0=min(years),
                dtick=1,
            ),
            yaxis=dict(title='Кількість страхувань'),
        )
        return fig2.to_html(full_html=False)

    def third_chart(self, request):
        # Отримання даних для третьої діаграми (Інформація про вік)
        age_data = pd.DataFrame(self.repo.get_age_information())

        # Перевірка, чи є дані
        if not age_data.empty:
            age_data = age_data.rename(columns={
                'age_group': 'Age Group',
                'male_count': 'Male Count',
                'female_count': 'Female Count'
            })
            # Перетворення таблиці у формат, зручний для побудови діаграми
            age_data = age_data.melt(
                id_vars=['Age Group'],
                value_vars=['Male Count', 'Female Count'],
                var_name='Gender',
                value_name='Count'
            )

            # Створюємо комбіновану колонку для розбиття на діаграмі
            age_data['Age and Gender'] = age_data['Age Group'] + ' - ' + age_data['Gender']

        # Отримання фільтрів від користувача
        selected_genders, selected_age_groups = self.get_filters(request, age_data)

        # Фільтрація даних
        filtered_data = age_data[
            (age_data['Gender'].isin(selected_genders)) &
            (age_data['Age Group'].isin(selected_age_groups))
        ]

        # Побудова третьої діаграми
        fig3 = px.pie(
            filtered_data,
            names="Age and Gender",  # Використовуємо комбіновану колонку
            values="Count",
            title="Розподіл віку та статі",
            hole=0.3  # Якщо хочете донат-подібну кругову діаграму
        )

        # Оновлення легенди для правильного відображення кольорів
        fig3.update_layout(
            legend_title="Стать",
            legend=dict(x=0.85, y=0.5, traceorder='normal', orientation='h', font=dict(size=12))
        )

        return fig3.to_html(full_html=False)

    def fourth_chart(self, request):
        # Отримуємо дані зі статистикою по статусах
        status_data = pd.DataFrame(self.repo.get_status_statistics())

        # Перевіряємо наявність даних
        if not status_data.empty:
            statuses = status_data['status__status'].tolist()
            counts = status_data['count'].tolist()

            # Отримання фільтрів від користувача (статуси)
            selected_statuses = request.GET.getlist('statuses', statuses)

            # Фільтрація даних за вибраними статусами
            filtered_data = status_data[status_data['status__status'].isin(selected_statuses)]

            # Побудова діаграми
            fig = go.Figure()
            fig.add_trace(go.Pie(
                labels=filtered_data['status__status'],  # Стовпець зі статусами
                values=filtered_data['count'],  # Стовпець з кількістю клієнтів
                name='Кількість за статусом',
                marker=dict(colors=['rgba(55, 128, 191, 0.7)', 'rgba(55, 128, 191, 1.0)'])  # Можна змінити кольори
            ))
            fig.update_layout(
                title='Статистика за статусом клієнтів',
                plot_bgcolor='rgb(240, 240, 240)',  # Зміна кольору фону діаграми
                paper_bgcolor='rgb(255, 255, 255)',  # Зміна кольору фону сторінки
                font=dict(family='Arial, sans-serif', size=12, color='rgb(0, 0, 0)')  # Зміна шрифтів
            )
            return fig.to_html(full_html=False)

    def fifth_chart(self, request):
        # Fetch data from the repository
        worker_data = pd.DataFrame(self.repo.served_people_capacity_by_worker())
        print(worker_data)

        # Rename columns for easier access
        worker_data = worker_data.rename(columns={
            'worker_name': 'Worker Name',
            'count': 'People Count'
        })

        # Get user-selected filters (if any)
        selected_workers = request.GET.getlist('workers', worker_data['Worker Name'].unique().tolist())

        # Filter data based on selected workers
        filtered_data = worker_data[worker_data['Worker Name'].isin(selected_workers)]

        # Build chart for worker served people capacity
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=filtered_data['Worker Name'],
            y=filtered_data['People Count'],
            name='People Served',
            marker=dict(color='rgba(55, 128, 191, 0.7)', line=dict(color='rgba(55, 128, 191, 1.0)', width=2))
        ))
        fig.update_layout(
            title='People Served by Workers',
            xaxis=dict(title='Worker Name'),
            yaxis=dict(title='People Count'),
            plot_bgcolor='rgb(240, 240, 240)',  # Background color of the plot area
            paper_bgcolor='rgb(255, 255, 255)',  # Background color of the whole page
            font=dict(family='Arial, sans-serif', size=12, color='rgb(0, 0, 0)')  # Font settings
        )
        return fig.to_html(full_html=False)

    def sixth_chart(self, request):
        # Fetch data from the repository
        price_data = pd.DataFrame(self.repo.get_price_of_item_and_price_of_insurance())
        print(price_data)

        # Rename columns for easier access
        price_data = price_data.rename(columns={
            'price_of_item_insurance': 'Item Insurance Price',
            'item_insurance__item_price': 'Item Price'
        })

        # Get user-selected filters (if any)
        selected_items = request.GET.getlist('items', price_data['Item Insurance Price'].unique().tolist())

        # Filter data based on selected items
        filtered_data = price_data[price_data['Item Insurance Price'].isin(selected_items)]

        # Build chart for item and insurance prices
        fig = go.Figure()

        # Create two bar traces for item price and insurance price
        fig.add_trace(go.Bar(
            x=filtered_data['Item Insurance Price'],
            y=filtered_data['Item Price'],
            name='Item Price',
            marker=dict(color='rgba(55, 128, 191, 0.7)', line=dict(color='rgba(55, 128, 191, 1.0)', width=2))
        ))

        # Add another bar trace for insurance price
        fig.add_trace(go.Bar(
            x=filtered_data['Item Insurance Price'],
            y=filtered_data['Item Insurance Price'],
            name='Insurance Price',
            marker=dict(color='rgba(255, 99, 132, 0.7)', line=dict(color='rgba(255, 99, 132, 1.0)', width=2))
        ))

        # Update layout for the chart
        fig.update_layout(
            title='Item Insurance vs Item Price',
            xaxis=dict(title='Item Insurance Price'),
            yaxis=dict(title='Price'),
            barmode='group',  # Bars will be grouped
            plot_bgcolor='rgb(240, 240, 240)',  # Background color of the plot area
            paper_bgcolor='rgb(255, 255, 255)',  # Background color of the whole page
            font=dict(family='Arial, sans-serif', size=12, color='rgb(0, 0, 0)')  # Font settings
        )

        # Return the graph in HTML format
        return fig.to_html(full_html=False)


def combined_charts(request):
    repo = AggregatetedRepository()
    diagrams = Diagrams(repo)

    # Create all the charts
    graph_html1 = diagrams.first_chart(request)
    graph_html2 = diagrams.second_chart(request)
    graph_html3 = diagrams.third_chart(request)
    graph_html4 = diagrams.fourth_chart(request)
    graph_html5 = diagrams.fifth_chart(request)
    graph_html6 = diagrams.sixth_chart(request)

    # Get filters for positions and age groups
    salary_data = pd.DataFrame(repo.get_avarage_salary())
    all_positions = salary_data['position'].tolist()

    age_data = pd.DataFrame(repo.get_age_information())
    age_groups = age_data['age_group'].tolist()

    selected_positions = request.GET.getlist('positions')
    selected_genders = request.GET.getlist('genders', ['Male Count', 'Female Count'])
    selected_age_groups = request.GET.getlist('age_groups', age_groups)

    status_statiscic = pd.DataFrame(repo.get_status_statistics())
    all_status = status_statiscic['status__status'].tolist()
    selected_statuses = request.GET.getlist('statuses', all_status)  # Default to all statuses
    print("Selected statuses:", selected_statuses)

    worker_data = pd.DataFrame(repo.served_people_capacity_by_worker())
    all_workers = worker_data['worker_name'].tolist()

    selected_workers = request.GET.getlist('workers', all_workers)

    # Pass the selected statuses to the template
    return render(request, 'dashboard/v1.html', {
        'graph_html1': graph_html1,
        'graph_html2': graph_html2,
        'graph_html3': graph_html3,
        'graph_html4': graph_html4,
        'graph_html5': graph_html5,
        'graph_html6': graph_html6,
        'positions': all_positions,
        'selected_positions': selected_positions,
        'age_groups': age_groups,
        'genders': ['Male Count', 'Female Count'],
        'selected_genders': selected_genders,
        'selected_age_groups': selected_age_groups,
        'statuses': all_status,  # List of all possible statuses
        'selected_statuses': selected_statuses,
        'workers': all_workers,
        'selected_workers': selected_workers
        # List of selected statuses
    })
