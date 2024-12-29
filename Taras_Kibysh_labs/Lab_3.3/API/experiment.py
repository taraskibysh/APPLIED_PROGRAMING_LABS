import time
import psutil
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
from django.db import connection


# SQL запит для отримання даних з бази
def get_customer_query():
    return """
        SELECT
            customer_profile.Name AS Name,
            Customer_profile.surname AS CustomerSurname,
            worker.name AS WorkerName,
            worker.position AS WorkerPosition,
            worker.salary AS WorkerSalary
        FROM customer_profile
        JOIN worker_has_customer_profile ON customer_profile.ID = worker_has_customer_profile.fk_customer_id
        JOIN worker ON worker_has_customer_profile.fk_worker_id = Worker.ID
    """


# Функція для виконання запиту
def execute_query(query=None, params=None):
    query = query or get_customer_query()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


# Функція для паралельного виконання кількох запитів
def threaded_query_execution(queries, max_threads=12):
    results = []
    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(execute_query, query) for query in queries]
        for future in futures:
            results.append(future.result())
    return results


# Функція для вимірювання ефективності з додаванням загруженості процесора і пам'яті
def measure_performance(queries, mode='thread', params_range=[2, 4, 6, 8, 10, 20]):
    results = []
    for param in params_range:
        start_time = time.time()

        # Отримання початкової інформації про ресурси системи
        initial_cpu = psutil.cpu_percent(interval=0.1)
        initial_memory = psutil.virtual_memory().percent

        if mode == 'thread':
            threaded_query_execution(queries, max_threads=param)

        end_time = time.time()

        # Отримання інформації після виконання запитів
        final_cpu = psutil.cpu_percent(interval=0.1)
        final_memory = psutil.virtual_memory().percent

        results.append({
            'mode': mode,
            'parameter': param,
            'execution_time': end_time - start_time,
            'cpu_usage_initial': initial_cpu,
            'cpu_usage_final': final_cpu,
            'memory_usage_initial': initial_memory,
            'memory_usage_final': final_memory
        })
    return results


# Функція для побудови графіка з результатами вимірювання
def performance_chart(request):
    queries = [get_customer_query() for _ in range(200)]  # Створення списку запитів


    thread_results = measure_performance(queries, mode='thread')


    results_df = pd.DataFrame(thread_results)


    fig_time = px.line(
        results_df,
        x='parameter',
        y='execution_time',
        title='Performance of Threading for Queries',
        labels={'parameter': 'Number of Threads', 'execution_time': 'Execution Time (s)'}
    )


    fig_cpu = px.line(
        results_df,
        x='parameter',
        y='cpu_usage_final',
        title='CPU Usage During Query Execution',
        labels={'parameter': 'Number of Threads', 'cpu_usage_final': 'CPU Usage (%)'}
    )


    fig_memory = px.line(
        results_df,
        x='parameter',
        y='memory_usage_final',
        title='Memory Usage During Query Execution',
        labels={'parameter': 'Number of Threads', 'memory_usage_final': 'Memory Usage (%)'}
    )

    graph_html_time = plot(fig_time, output_type='div')
    graph_html_cpu = plot(fig_cpu, output_type='div')
    graph_html_memory = plot(fig_memory, output_type='div')


    return render(request, 'experment.html', {
        'graph_html_time': graph_html_time,
        'graph_html_cpu': graph_html_cpu,
        'graph_html_memory': graph_html_memory
    })
