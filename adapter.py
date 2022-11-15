#By importing specific classes from moudles, we isolating our project from whole library. It is Facade pattern
import csv
from datetime import datetime
from turtle import clear
import xml.etree.ElementTree as ET
import os

#main class, which implements Adapter pattern
class ClientAdapter:
    client_data_list = []
    updated_client_data_list = []
    def __init__(self, file_path, csv_format, xml_format):
        #Information about client code is saved here
        self.file_path = file_path
        self.csv_format = csv_format
        self.xml_format = xml_format

        print(f"Path to file: {self.file_path.strip()}")
        print(f"Is csv enabled: {self.csv_format}")
        print(f"Is xml enabled: {self.xml_format}")    
    #adaptee data, which is read from client file
    def adapter(self):
        with open(self.file_path) as client_file:
            csv_file = csv.reader(client_file, delimiter = '\t')
            for row in csv_file:
                self.client_data_list.append(row)
                self.updated_client_data_list.append(row)
        self.formatter()

    #main adapter method. Recreates and reorganizes the data for the new system
    def formatter(self):
        for row in range(len(self.client_data_list)):
            self.updated_client_data_list[row][0] = datetime.strptime(self.client_data_list[row][0], "%Y/%d/%m").strftime("%d.%m.%Y")
            self.updated_client_data_list[row][1] = datetime.strptime(self.client_data_list[row][1], '%I:%M %p').strftime("%H:%M")
            self.updated_client_data_list[row][2] = str(float(self.client_data_list[row][2]) * 1.943844)
            self.updated_client_data_list[row][3] = str(float(self.client_data_list[row][3]) / 1.852)
        
        if self.csv_format == 1 and self.xml_format == 1:
            self.to_csv()
            self.to_xml()
        elif self.csv_format == 1 and self.xml_format == 0:
            self.to_csv()
        elif self.csv_format == 0 and self.xml_format == 1:
            self.to_xml()
        else:
            print("Error")
    #Creates CSV file from adapted data
    def to_csv(self):
        new_csv = self.file_path[0:(len(self.file_path)-4)] + "_adapted.csv"
        with open(new_csv, 'w', newline='') as csv_file:
            write = csv.writer(csv_file, delimiter='\t')
            write.writerows(self.updated_client_data_list)
        self.client_data_list.clear()
        self.updated_client_data_list.clear()
    #Creates XML file from adapted data
    def to_xml(self):
        #file_xml = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'adapted_xml.xml')
        file_xml = self.file_path[0:(len(self.file_path)-4)] + "_adapted.xml"
        file = open(file_xml,'wb')
        file.write(b'<?xml version="1.0" encoding="UTF-8" ?>')
        file.write(b'<points>')
        for row in range(len(self.updated_client_data_list)):
            point = ET.Element('point')
            ET.SubElement(point, 'date').text = self.client_data_list[row][0]
            ET.SubElement(point, 'time').text = self.client_data_list[row][1]
            ET.SubElement(point, 'speed').text = self.client_data_list[row][2]
            ET.SubElement(point, 'distance').text = self.client_data_list[row][3]
            ET.SubElement(point, 'description').text = self.client_data_list[row][4]
            file.write(ET.tostring(point))
        file.write(b'</points>')
        file.close()
        self.client_data_list.clear()
        self.updated_client_data_list.clear()






