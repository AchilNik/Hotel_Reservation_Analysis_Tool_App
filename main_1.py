from PyQt5.QtWidgets import *
from opening import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import DB_connection
import pandas as pd

class PlotCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 7, height = 4, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes =fig.add_subplot(111)
        self.axes.margins(0,0)
        super(PlotCanvas, self).__init__(fig)
        self.setParent(parent)
        fig.tight_layout()


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.continue_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.canvas = PlotCanvas(self.plot_frame)
        self.plot_frame.setLayout(QVBoxLayout())
        self.plot_frame.layout().addWidget(self.canvas)
        self.stayin_btn.clicked.connect(self.avg_stayin_btn_plot)
        self.canc_btn.clicked.connect(self.canc_prec_plot)
        self.people_distribution_btn.clicked.connect(self.people_per_room_dis_plot)
        self.reservations_in_time_btn.clicked.connect(self.res_in_time_plot)
        self.room_type_distribution_btn.clicked.connect(self.room_type_plot)
        self.monthly_reservation_distribution_btn.clicked.connect(self.seasonal_res_plot)
        self.seasonal_btn.clicked.connect(self.seasonal_reservations)
        self.cancelations_in_time_btn.clicked.connect(self.canc_in_time_plot)
        self.close_app_btn.clicked.connect(self.end)
        self.show()

    def room_type_plot(self):
        my_connection = DB_connection.db_connection()
        my_cursor = my_connection.cursor()

        selection_query = 'SELECT room_type, reservations FROM project2023.room_type_distribution WHERE hotel_name = "City Hotel"'
        my_cursor.execute(selection_query)
        df1 = pd.DataFrame(my_cursor.fetchall(), columns=['Room Type', 'Reservations'])
        selection_query = 'SELECT room_type, reservations FROM project2023.room_type_distribution WHERE hotel_name = "Resort Hotel"'
        my_cursor.execute(selection_query)
        df2 = pd.DataFrame(my_cursor.fetchall(), columns=['Room Type', 'Reservations'])
        my_cursor.close()
        my_connection.close()

        self.canvas.axes.clear()
        self.canvas.axes.plot(df1['Room Type'], df1['Reservations'], color='green', label='City Hotel Reservations', marker='.')
        self.canvas.axes.plot(df2['Room Type'], df2['Reservations'], color='red', label='Resort Hotel Reservations', marker='.')
        self.canvas.axes.set_title('Room type Reservations')
        self.canvas.axes.set_xlabel('Room Type')
        self.canvas.axes.set_ylabel('Reservations')
        self.canvas.axes.legend(frameon=True)
        self.canvas.draw()

    def avg_stayin_btn_plot(self):
        my_connection = DB_connection.db_connection()
        my_cursor = my_connection.cursor()

        selection_query = 'SELECT hotel_name, nights_in_percentage FROM project2023.hotel_stays'
        my_cursor.execute(selection_query)
        df1 = pd.DataFrame(my_cursor.fetchall(), columns=['Hotel name', 'Average stay in nights'])
        my_cursor.close()
        my_connection.close()

        self.canvas.axes.clear()
        self.canvas.axes.bar(df1['Hotel name'], df1['Average stay in nights'], color=['green', 'red'])
        self.canvas.axes.set_xlabel('Hotel')
        self.canvas.axes.set_ylabel('Average stay in nights')
        self.canvas.axes.set_title('Stay in average data')
        self.canvas.draw()

    def seasonal_res_plot(self):
        my_connection = DB_connection.db_connection()
        my_cursor = my_connection.cursor()

        query = 'SELECT month, reservations FROM project2023.monthly_booking_distribution WHERE hotel_name = "City Hotel"'
        my_cursor.execute(query)
        df1 = pd.DataFrame(my_cursor.fetchall(), columns=['month', 'reservations'])
        query = 'SELECT month, reservations FROM project2023.monthly_booking_distribution WHERE hotel_name = "Resort Hotel"'
        my_cursor.execute(query)
        df2 = pd.DataFrame(my_cursor.fetchall(), columns=['month', 'reservations'])
        my_cursor.close()
        my_connection.close()

        self.canvas.axes.clear()
        self.canvas.axes.plot(df1['month'], df1['reservations'], color='green', marker='.', label='City Hotel')
        self.canvas.axes.plot(df2['month'], df2['reservations'], marker='.', label='Resort Hotel')
        self.canvas.axes.set_title('Monthly reservations')
        self.canvas.axes.set_ylabel('Reservations')
        self.canvas.axes.set_xlabel('Month')
        self.canvas.axes.legend(frameon=True)
        self.canvas.draw()

    def people_per_room_dis_plot(self):
        my_connection = DB_connection.db_connection()
        my_cursor = my_connection.cursor()

        query = 'SELECT single, families, couples, group_of_people FROM project2023.people_per_room_distribution WHERE hotel_name = "City Hotel"'
        my_cursor.execute(query)
        df1 = pd.DataFrame(my_cursor.fetchall(), columns=['single', 'families', 'couples', 'group_of_people'])
        query = 'SELECT single, families, couples, group_of_people FROM project2023.people_per_room_distribution WHERE hotel_name = "Resort Hotel"'
        my_cursor.execute(query)
        df2 = pd.DataFrame(my_cursor.fetchall(), columns=['single', 'families', 'couples', 'group_of_people'])
        my_cursor.close()
        my_connection.close()

        self.canvas.axes.clear()
        categories = ['Singles', 'Families', 'Couples', 'Groups']
        xticks = range(len(categories))
        self.canvas.axes.plot(xticks,
                   (df1['single'], df1['families'], df1['couples'], df1['group_of_people']),
                   color='green', marker = '.', label='City Hotel reservations')
        self.canvas.axes.plot(xticks,
                   (df2['single'], df2['families'], df2['couples'], df2['group_of_people']),
                   color='red', marker = '.', label='Resort Hotel reservations')
        self.canvas.axes.set_title('People per room distribution')
        self.canvas.axes.set_xticks(xticks)
        self.canvas.axes.set_xticklabels(categories)
        self.canvas.axes.set_xlabel('Type of reservation')
        self.canvas.axes.set_ylabel('Reservations')
        self.canvas.axes.legend(frameon=True)
        self.canvas.draw()


    def res_in_time_plot(self):
        my_connection = DB_connection.db_connection()
        my_cursor = my_connection.cursor()

        query = 'SELECT month, reservations, cancellations FROM project2023.reservations_in_time WHERE hotel_name ="City Hotel"'
        my_cursor.execute(query)
        df1 = pd.DataFrame(my_cursor.fetchall(), columns=['month', 'reservations', 'cancellations'])
        query = 'SELECT month, reservations, cancellations FROM project2023.reservations_in_time WHERE hotel_name ="Resort Hotel"'
        my_cursor.execute(query)
        df2 = pd.DataFrame(my_cursor.fetchall(), columns=['month', 'reservations', 'cancellations'])
        my_cursor.close()
        my_connection.close()

        self.canvas.axes.clear()
        self.canvas.axes.set_title('Reservations plot', fontsize=15)
        self.canvas.axes.plot(df1['month'], df1['reservations'], color='blue', marker='.', label='City reservations')
        self.canvas.axes.plot(df2['month'], df2['reservations'], color='green', marker='.', label='Resort reservations')
        self.canvas.axes.set_xlabel('Month')
        self.canvas.axes.set_ylabel('Reservations')
        self.canvas.axes.legend(frameon=True)
        self.canvas.draw()

    def canc_in_time_plot(self):
        my_connection = DB_connection.db_connection()
        my_cursor = my_connection.cursor()

        query = 'SELECT month, reservations, cancellations FROM project2023.reservations_in_time WHERE hotel_name ="City Hotel"'
        my_cursor.execute(query)
        df1 = pd.DataFrame(my_cursor.fetchall(), columns=['month', 'reservations', 'cancellations'])
        query = 'SELECT month, reservations, cancellations FROM project2023.reservations_in_time WHERE hotel_name ="Resort Hotel"'
        my_cursor.execute(query)
        df2 = pd.DataFrame(my_cursor.fetchall(), columns=['month', 'reservations', 'cancellations'])
        my_cursor.close()
        my_connection.close()
        self.canvas.axes.clear()
        self.canvas.axes.set_title('Cancellations plot', fontsize=15)
        self.canvas.axes.plot(df1['month'], df1['cancellations'], color='red', marker='.', label='City cancellations')
        self.canvas.axes.plot(df2['month'], df2['cancellations'], color='yellow', marker='.', label='Resort cancellations')
        self.canvas.axes.set_xlabel('Month')
        self.canvas.axes.set_ylabel('Cancellations')
        self.canvas.axes.legend(frameon = True)
        self.canvas.draw()


    def seasonal_reservations(self):
        my_connection = DB_connection.db_connection()
        my_cursor = my_connection.cursor()

        query = 'SELECT season, reservations FROM project2023.seasonal_booking_distribution WHERE hotel_name = "City Hotel"'
        my_cursor.execute(query)
        df3 = pd.DataFrame(my_cursor.fetchall(), columns=['season', 'reservations'])
        query = 'SELECT season, reservations FROM project2023.seasonal_booking_distribution WHERE hotel_name = "Resort Hotel"'
        my_cursor.execute(query)
        df4 = pd.DataFrame(my_cursor.fetchall(), columns=['season', 'reservations'])
        my_cursor.close()
        my_connection.close()

        self.canvas.axes.clear()
        self.canvas.axes.plot(df3['season'], df3['reservations'], color='green', marker='.', label='City Hotel')
        self.canvas.axes.plot(df4['season'], df4['reservations'], marker='.', label='Resort Hotel')
        self.canvas.axes.set_title('Seasonal reservations')
        self.canvas.axes.set_ylabel('Reservations')
        self.canvas.axes.set_xlabel('Season')
        self.canvas.axes.legend(frameon=True)
        self.canvas.draw()

    def canc_prec_plot(self):
        my_connection = DB_connection.db_connection()
        my_cursor = my_connection.cursor()

        selection_query = 'SELECT hotel_name, cancellation_percentage FROM project2023.hotel_stays'
        my_cursor.execute(selection_query)
        df2 = pd.DataFrame(my_cursor.fetchall(), columns=['Hotel name', 'Cancellation percentage'])
        my_cursor.close()
        my_connection.close()

        self.canvas.axes.clear()
        self.canvas.axes.bar(df2['Hotel name'], df2['Cancellation percentage'], color=['green', 'red'])
        self.canvas.axes.set_xlabel('Hotel')
        self.canvas.axes.set_ylabel('Cancellation percentage')
        self.canvas.axes.set_title('Cancellation percentage data')
        self.canvas.draw()

    def end(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText('Are you sure you want to exit?')
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        resp = msg.exec_()
        if resp == QMessageBox.Ok:
            self.close()
        else:
            msg.close()