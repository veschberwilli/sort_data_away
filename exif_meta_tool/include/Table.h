
#include <string>
#include <vector>


struct row {
        std::string timestamp_orig="";
        double timestamp_double=0;
        std::string filename="";
    };

class Table {
    public:
        std::vector<row> table_vec;

        void AddToTable(std::string filename, std::string timestamp);
        void GetLatest();
        void PrintTable();
};