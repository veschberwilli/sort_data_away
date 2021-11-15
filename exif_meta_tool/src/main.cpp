// This is my first cpp stuff


#include <stdio.h>
#include <iostream>
#include <vector>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>
#include "ExifTool.h"
#include <map>
#include "Table.h"


using namespace std;
namespace po = boost::program_options;
namespace fs = boost::filesystem;


po::variables_map getProgramOptions(const int argc, const char* const* argv) {
    po::options_description program_options("Read EXIF Headers");

    program_options.add_options()
        ("help,h", "Display the help message.")
        ("name,n", po::value<string>()->default_value("Janine"), "Select Name to Search For.")
        ("dir,d", po::value<string>()->default_value("../pics"), "Select Directory to Search In.");
    
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, program_options), vm);
    po::notify(vm);    

    // output help
    if (vm.count("help")) {
        cout << program_options << "\n";
    }

    return vm;
}

void printHeader(){
    cout<<"+++++++++++++++++++++++"<<endl;
    cout<<"+++  exif meta tool +++"<<endl;
    cout<<"+++++++++++++++++++++++"<<endl;
}


int main(int argc, char *argv[]) {

    // print header
    printHeader();

    // parse cmd line params
    po::variables_map vm = getProgramOptions(argc, argv);

    // print params
    cout << "Name: " << vm["name"].as<string>() << endl;
    cout << "Dir: " << vm["dir"].as<string>() << endl;

    // loop over files and extract exif info and store in array
    fs::path p = vm["dir"].as<string>();
    vector<string> white_list = {".jpg", ".png"};
    Table tmp;
    
    if (fs::is_directory(p))
    {
        for (fs::directory_entry& entry : fs::recursive_directory_iterator(p))
        {
            if ((entry.path().has_extension()) && (find(white_list.begin(), white_list.end(), entry.path().filename()) == white_list.end()))
            {
                //cout << "Path: " << entry.path() << endl;
                //cout << "Filename: " << entry.path().filename().c_str() << endl;
                //cout << "Extension: " << entry.path().extension() << endl;
                
                // exiftool
                ExifTool *et = new ExifTool();

                string opt = "-CreateDate\n-Comment";
                int nr = et->ExtractInfo(entry.path().c_str(), opt.c_str());
                TagInfo *info = et->GetInfo(nr);
                
                string iso_tmp;
                string create_date_tmp;

                // read ALL metadata from the image into TagInfo Struct
                //TagInfo *info = et->ImageInfo(entry.path().c_str());

                if (info) 
                {
                    // print returned information
                    for (TagInfo *i=info; i; i=i->next) 
                    {
                        if (string(i->name) == "CreateDate"){
                            //cout << "Path:" << entry.path() << " --> " << i->name << " = " << i->value << endl;
                            create_date_tmp = string(i->value);
                        }
                        if (string(i->name) == "Comment"){
                            //cout << "Path:" << entry.path() << " --> " << i->name << " = " << i->value << endl;
                            iso_tmp = string(i->value);
                        }
                    }
                    // add to table
                    if (iso_tmp == vm["name"].as<string>()){
                        tmp.AddToTable(entry.path().c_str(), create_date_tmp);
                    }
                    

                    // we are responsible for deleting the information when done
                    delete info;
                }
            }
        }
    }
        
    // print files with resp. tag in table form
    // tmp.PrintTable();

    // get the latest file
    tmp.GetLatest();
    
    return 0;
}
