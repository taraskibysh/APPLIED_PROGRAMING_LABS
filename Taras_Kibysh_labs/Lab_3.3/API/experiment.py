from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
from django.db import connection
import time
import pandas as pd
import plotly.express as px
from plotly.offline import plot

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

# Функція для вимірювання ефективності
def measure_performance(queries, mode='thread', params_range=[2, 4, 6, 8, 10]):
    results = []
    for param in params_range:
        start_time = time.time()
        if mode == 'thread':
            threaded_query_execution(queries, max_threads=param)
        end_time = time.time()
        results.append({
            'mode': mode,
            'parameter': param,
            'execution_time': end_time - start_time
        })
    return results

# Функція для побудови графіка з результатами вимірювання
def performance_chart(request):
    queries = [get_customer_query() for _ in range(200)]  # Створення списку запитів

    # Виконання тесту з використанням потоків
    thread_results = measure_performance(queries, mode='thread')

    # Конвертація результатів у DataFrame
    results_df = pd.DataFrame(thread_results)

    # Побудова графіка
    fig = px.line(
        results_df,
        x='parameter',
        y='execution_time',
        title='Performance of Threading for Queries',
        labels={'parameter': 'Number of Threads', 'execution_time': 'Execution Time (s)'}
    )

    # Генерація HTML для графіка
    graph_html = plot(fig, output_type='div')

    return render(request, 'experment.html', {'graph_html': graph_html})
