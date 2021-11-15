
#include <stdio.h>
#include <iostream>
#include <vector>
#include "Table.h"
#include <algorithm>

void Table::AddToTable(std::string filename, std::string timestamp){
    // std::cout << "add timestamp: " << timestamp << std::endl;

    // parse timestmp string and convert to double
    row tmp_row;
    tmp_row.timestamp_orig = timestamp;
    tmp_row.filename = filename;
    
    size_t start = 0;
    size_t end = 4;
    std::string timestamp_year = timestamp.substr(start, end);
    start = 5;
    end = 2;
    std::string timestamp_month = timestamp.substr(start, end);
    start = 8;
    end = 2;
    std::string timestamp_day = timestamp.substr(start, end);
    start = 11;
    end = 2;
    std::string timestamp_hour = timestamp.substr(start, end);
    start = 14;
    end = 2;
    std::string timestamp_min = timestamp.substr(start, end);
    start = 17;
    end = 2;
    std::string timestamp_sec = timestamp.substr(start, end);

    // debug
    /*
    std::cout << timestamp_year << std::endl;
    std::cout << timestamp_month << std::endl;
    std::cout << timestamp_day << std::endl;
    std::cout << timestamp_hour << std::endl;
    std::cout << timestamp_min << std::endl;
    std::cout << timestamp_sec << std::endl;
    */

    // debug
    //std::cout << "debug: " << (timestamp_year + timestamp_month + timestamp_day + timestamp_hour + timestamp_min + timestamp_sec) << std::endl;
    //std::cout << "debug: " << std::stod(timestamp_year + timestamp_month + timestamp_day + timestamp_hour + timestamp_min + timestamp_sec) << std::endl;

    tmp_row.timestamp_double = std::stod(timestamp_year + timestamp_month + timestamp_day + timestamp_hour + timestamp_min + timestamp_sec);

    // pushback
    table_vec.push_back(tmp_row);
}

void Table::PrintTable(){
    for (int i; i<table_vec.size(); i++){
        std::cout << "row " << i << " --> " << table_vec.at(i).filename << ", " << 
                                               table_vec.at(i).timestamp_orig << ", " << 
                                               table_vec.at(i).timestamp_double << std::endl;
    }
}

void Table::GetLatest(){
    std::vector<double> v;

    for (int i; i<table_vec.size(); i++){
        //dates.push_back(table_vec.at(i).timestamp_int);
        v.push_back(table_vec.at(i).timestamp_double);
    }

    int maxElementIndex = std::max_element(v.begin(),v.end()) - v.begin();
    // std::cout << "index_max: " << maxElementIndex << std::endl;
    
    std::cout << "Latest File: " << table_vec.at(maxElementIndex).filename << std::endl;
}